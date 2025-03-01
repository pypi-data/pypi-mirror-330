import asyncio
import json
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate
from aiortc.rtcconfiguration import RTCConfiguration, RTCIceServer
import socketio
from datetime import datetime
from typing import Optional, Callable, Dict, Any
from lzstring import LZString  # Add this import

class RoboticsClient:
    def __init__(self):
        self._pc: Optional[RTCPeerConnection] = None
        self._channel = None
        self._sio = None
        self._connected = False
        self._callback = None
        self._robot_id = None
        self._token = None
        self._pending_messages = []
        self.lzstring = LZString()
        self.messages = {}

    def _decompress_message(self, message_str: str) -> Optional[Dict]:
        """Decompress incoming message if needed"""
        try:
            # First try parsing as regular JSON
            data = json.loads(message_str)
            
            # Check if it's a chunked message
            if all(k in data for k in ['chunk', 'index', 'total', 'messageId']):
                message_id = data['messageId']
                if message_id not in self.messages:
                    self.messages[message_id] = {
                        'chunks': [None] * data['total'],
                        'total': data['total']
                    }
                
                # Store this chunk
                self.messages[message_id]['chunks'][data['index']] = data['chunk']
                
                # Check if we have all chunks
                if all(chunk is not None for chunk in self.messages[message_id]['chunks']):
                    # Combine and decompress
                    combined = ''.join(self.messages[message_id]['chunks'])
                    try:
                        decompressed = self.lzstring.decompressFromBase64(combined)
                        if decompressed:
                            return json.loads(decompressed)
                    except:
                        # If decompression fails, return the combined chunks as is
                        return json.loads(combined)
                    finally:
                        del self.messages[message_id]
                return None
            
            return data
        except:
            # If any parsing fails, return the original message
            return message_str

    async def connect(self, options: Dict[str, str], callback: Callable[[Dict], None]) -> None:
        """Connect to robotics.dev and establish P2P connection"""
        self._callback = callback
        self._robot_id = options.get('robot')
        self._token = options.get('token')
        
        # Ensure server URL is properly handled
        server = options.get('server')
        if not server:
            server = 'wss://robotics.dev'
        elif server.startswith('http://'):
            server = server.replace('http://', 'ws://')
        elif server.startswith('https://'):
            server = server.replace('https://', 'wss://')
        elif not server.startswith(('ws://', 'wss://')):
            server = f"ws://{server}"
            
        self._server = server
        print(f"Using signaling server: {self._server}")

        if not self._robot_id or not self._token:
            raise ValueError("Both robot ID and token are required")

        # Initialize socket.io with debugging
        self._sio = socketio.AsyncClient(logger=True, engineio_logger=True)
        self._client_id = f'remote-{hex(int(datetime.now().timestamp()))[2:]}'

        @self._sio.event
        async def connect():
            print(f"Connected to signaling server: {self._server}")
            print(f"Client ID: {self._client_id}")
            # Emit initial signal after connection
            await self._sio.emit('signal', {
                'type': 'join',
                'robot': self._robot_id,
                'token': self._token,
                'targetPeer': self._robot_id,
                'sourcePeer': self._client_id
            })
            await self._setup_peer_connection()

        @self._sio.event
        async def disconnect():
            print("Disconnected from signaling server")

        @self._sio.event
        async def error(data):
            print(f"Socket.IO error: {data}")

        @self._sio.event
        async def signal(data):
            print(f"Received signal: {data.get('type')}")
            if data.get('type') in ['answer', 'candidate']:
                await self._handle_peer_reply(data)

        # Connect with proper URL parameters
        connection_url = (
            f"{self._server}?"
            f"id={self._client_id}&"
            f"robot={self._robot_id}&"
            f"token={self._token}"
        )
        
        print(f"Connecting to: {connection_url}")
        await self._sio.connect(
            connection_url,
            transports=["websocket"]
        )

    async def _setup_peer_connection(self):
        """Set up WebRTC peer connection"""
        print("Setting up peer connection...")
        
        config = RTCConfiguration([
            RTCIceServer(urls=["stun:stun.l.google.com:19302"])
        ])
        
        self._pc = RTCPeerConnection(configuration=config)

        @self._pc.on("connectionstatechange")
        async def on_connectionstatechange():
            print(f"Connection state: {self._pc.connectionState}")
            if self._pc.connectionState == "connected":
                self._connected = True

        @self._pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            print(f"ICE connection state: {self._pc.iceConnectionState}")

        @self._pc.on("icegatheringstatechange")
        async def on_icegatheringstatechange():
            print(f"ICE gathering state: {self._pc.iceGatheringState}")

        # Create data channel first
        self._channel = self._pc.createDataChannel(
            'chat',
            ordered=True,
            protocol='chat',
            negotiated=True,
            id=1
        )

        self._setup_data_channel()

        # Create and send offer
        offer = await self._pc.createOffer()
        await self._pc.setLocalDescription(offer)

        # Format SDP for compatibility
        sdp_lines = []
        ice_lines = []
        fingerprint = None

        # Extract components from original SDP
        for line in offer.sdp.split('\r\n'):
            if line.startswith('a=ice-ufrag:'):
                ice_lines.append(line)
            elif line.startswith('a=ice-pwd:'):
                ice_lines.append(line)
            elif line.startswith('a=fingerprint:sha-256'):
                fingerprint = line

        # Build SDP with exact format
        sdp_lines = [
            'v=0',
            f'o=- {int(datetime.now().timestamp())} 1 IN IP4 0.0.0.0',
            's=-',
            't=0 0',
            'm=application 9 UDP/DTLS/SCTP webrtc-datachannel',
            'c=IN IP4 0.0.0.0',
            'a=mid:0'
        ]

        # Add ICE and fingerprint in correct order
        sdp_lines.extend(ice_lines)
        if fingerprint:
            sdp_lines.append(fingerprint)

        # Add required attributes
        sdp_lines.extend([
            'a=sctp-port:5000',
            'a=max-message-size:262144',
            'a=setup:actpass'
        ])

        modified_sdp = '\r\n'.join(sdp_lines) + '\r\n'

        # Send offer
        await self._sio.emit('signal', {
            'type': 'offer',
            'robot': self._robot_id,
            'token': self._token,
            'targetPeer': self._robot_id,
            'sourcePeer': self._client_id,
            'sdp': modified_sdp
        })
        print("Sent offer to peer")

        @self._pc.on("icecandidate")
        async def on_icecandidate(candidate):
            if candidate:
                await self._sio.emit('signal', {
                    'type': 'candidate',
                    'robot': self._robot_id,
                    'token': self._token,
                    'targetPeer': self._robot_id,
                    'sourcePeer': self._client_id,
                    'candidate': candidate.candidate,
                    'mid': candidate.sdpMid
                })

    async def _handle_peer_reply(self, data):
        """Handle peer connection signaling"""
        try:
            print(f"Handling peer reply: {data.get('type')}")
            if data['type'] == 'answer':
                # Convert answer SDP for aiortc
                sdp = data['sdp'].replace(
                    'UDP/DTLS/SCTP webrtc-datachannel',
                    'DTLS/SCTP 5000'
                )
                answer = RTCSessionDescription(sdp=sdp, type='answer')
                await self._pc.setRemoteDescription(answer)
                print("Set remote description")
            
            elif data['type'] == 'candidate':
                try:
                    # Handle candidate string directly
                    raw = data.get('candidate', '')
                    if raw.startswith('a='):
                        raw = raw[2:]
                    if raw.startswith('candidate:'):
                        raw = raw[10:]
                    
                    # Parse the candidate string
                    parts = raw.split()
                    if len(parts) >= 8:
                        # Create candidate with parsed components
                        candidate = RTCIceCandidate(
                            component=1,
                            foundation=parts[0],
                            protocol=parts[2].lower(),
                            priority=int(parts[3]),
                            ip=parts[4],
                            port=int(parts[5]),
                            type=parts[7],
                            sdpMid=data.get('mid', '0'),
                            sdpMLineIndex=0
                        )
                        
                        await self._pc.addIceCandidate(candidate)
                        print(f"Added ICE candidate: {raw}")
                except Exception as e:
                    print(f"ICE candidate error: {str(e)}")
                    print(f"Raw candidate data: {data}")

        except Exception as e:
            print(f"Peer reply error: {str(e)}")
            print(f"Full data: {data}")

    async def _handle_message(self, data):
        """Process incoming messages and route to callback"""
        if self._callback:
            await asyncio.get_event_loop().run_in_executor(
                None, self._callback, data
            )

    def _flush_pending_messages(self):
        """Send any pending messages once connected"""
        if self._connected and self._channel:
            for msg in self._pending_messages:
                self._channel.send(json.dumps(msg))
            self._pending_messages.clear()

    async def twist(self, robot: str, twist_msg: Dict[str, Any]) -> None:
        """Send twist command to robot"""
        message = {
            'topic': 'twist',
            'robot': robot,
            'twist': twist_msg
        }
        await self._send_message(message)

    async def speak(self, robot: str, text: str) -> None:
        """Send speak command to robot"""
        message = {
            'topic': 'speak',
            'robot': robot,
            'text': text
        }
        await self._send_message(message)

    async def _send_message(self, message: Dict[str, Any]) -> None:
        """Send message through data channel or queue if not connected"""
        try:
            if self._channel and self._channel.readyState == "open":
                # Send message in exact format expected by robot
                self._channel.send(json.dumps(message))
                print(f"Message sent successfully: {message}")
            else:
                print(f"Channel not ready (state: {getattr(self._channel, 'readyState', 'none')})")
                self._pending_messages.append(message)

        except Exception as e:
            print(f"Error sending message: {e}")
            self._pending_messages.append(message)

    async def disconnect(self) -> None:
        """Clean shutdown of connections"""
        if self._channel:
            self._channel.close()
        if self._pc:
            await self._pc.close()
        if self._sio:
            await self._sio.disconnect()
        self._connected = False

    def _setup_data_channel(self):
        """Set up data channel handlers"""
        if not self._channel:
            return

        @self._channel.on("open")
        def on_open():
            print("Data channel opened")
            self._connected = True
            # Send ready signal
            ready_msg = json.dumps({"type": "ready"})
            print(f"Sending ready signal: {ready_msg}")
            self._channel.send(ready_msg)
            # Execute callback
            if self._callback:
                asyncio.create_task(self._callback({"type": "connected"}))

        @self._channel.on("message")
        def on_message(message):
            if not self._callback or not isinstance(message, str):
                return

            try:
                # Decompress and parse message
                data = self._decompress_message(message)
                if data:
                    print(f"Received message: {data}")
                    asyncio.create_task(self._callback(data))
            except Exception as e:
                print(f"Message handling error: {e}")

# Create singleton instance
robotics = RoboticsClient()

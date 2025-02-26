from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    async def send(self, websocket: WebSocket, success: bool, message: str, data: dict, status: int = 200,
                   error: dict = None) -> None:
        await websocket.send_json({
            'status': status,
            'success': success,
            'message': message,
            'data': data,
            'error': error
        })

    async def broadcast(self, message: str = None, from_client: str = 'Server'):
        for connection in self.active_connections:
            await connection.send_json({
                'status': 200,
                'success': True,
                'message': f'Active connections: {len(self.active_connections)}',
                'data': {
                    'from_client': from_client,
                    'message': message
                },
                'error': None
            })


manager = ConnectionManager()

import magma_indonesia
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from magma_indonesia.routers.v1.seismic_router import SeismicRouter
from magma_indonesia.routers.websocket import manager
from importlib_resources import files

app = FastAPI()
static_dir = str(files("magma_indonesia.static"))


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return None


@app.get("/")
def read_root():
    return {
        "status": 200,
        "message": "It works!",
        "data": {
            'app': 'MAGMA Indonesia Python package',
            'version': magma_indonesia.__version__,
            'author': magma_indonesia.__author__,
            'author_email': magma_indonesia.__author_email__,
            'url': magma_indonesia.__url__,
        },
        "error": None
    }


app.mount('/static', StaticFiles(directory=static_dir), name="static")


@app.websocket('/websocket/client/{client}')
async def websocket_client(websocket: WebSocket, client: int):
    await manager.connect(websocket)

    await manager.broadcast(
        message=f'Client #{client} connected.',
        from_client=client
    )

    try:
        while True:
            data = await websocket.receive_json()
            await manager.send(
                websocket=websocket,
                status=200,
                success=True,
                message="Message Received",
                data=data
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(
            message=f"Client #{client} disconnected.",
            from_client=client
        )


app.include_router(SeismicRouter)

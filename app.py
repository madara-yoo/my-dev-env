import asyncio
import os
import pty
import shlex
import struct
import fcntl
import termios
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# تشغيل الباش كعملية ترمينال
master, slave = pty.openpty()

async def terminal_reader(websocket: WebSocket):
    while True:
        try:
            # قراءة المخرجات من الـ PTY
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, os.read, master, 1024)
            if data:
                await websocket.send_text(data.decode('utf-8', 'ignore'))
        except Exception:
            break

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # تشغيل عملية القراءة في الخلفية
    reader_task = asyncio.create_task(terminal_reader(websocket))
    
    try:
        while True:
            data = await websocket.receive_text()
            os.write(master, data.encode())
    except WebSocketDisconnect:
        reader_task.cancel()

# تقديم الواجهة
app.mount("/webos", StaticFiles(directory="webos"), name="webos")

@app.get("/")
async def get():
    return FileResponse("webos/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

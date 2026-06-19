import asyncio
import os
import pty
import subprocess
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# إعداد الـ PTY
master, slave = pty.openpty()

# تشغيل الـ Bash في الخلفية
subprocess.Popen(
    ['/bin/bash', '-i'],
    preexec_fn=os.setsid,
    stdin=slave,
    stdout=slave,
    stderr=slave,
    env={**os.environ, 'TERM': 'xterm'}
)

async def terminal_reader(websocket: WebSocket):
    while True:
        try:
            # قراءة المخرجات من الترمينال
            data = os.read(master, 1024)
            if data:
                await websocket.send_text(data.decode('utf-8', 'ignore'))
            await asyncio.sleep(0.01) # تقليل استهلاك المعالج
        except Exception:
            break

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    reader_task = asyncio.create_task(terminal_reader(websocket))
    try:
        while True:
            data = await websocket.receive_text()
            os.write(master, data.encode())
    except WebSocketDisconnect:
        reader_task.cancel()

# تقديم الملفات
app.mount("/webos", StaticFiles(directory="webos"), name="webos")

@app.get("/")
async def get():
    return FileResponse("webos/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

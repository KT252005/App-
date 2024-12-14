from fastapi import FastAPI , WebSocket,WebSocketDisconnect,Request
from typing import List
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import websockets
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from fastapi.templating import Jinja2Templates

app = FastAPI()
 # Replace with your actual key
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; you can specify domains for more security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)



templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_homepage(request: Request):
    return templates.TemplateResponse("chat_app.html", {"request": request, "title": "Home Page"})



# Websocket connection for listing 
class Connection:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
            
    async def connect(self,websocket:WebSocket):    
        await websocket.accept()
        self.active_connections.append(websocket)
        
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        
    async def broadcast(self, message:str,sender: WebSocket):
        for connection in self.active_connections:
            if connection!=sender:
                await connection.send_text(message) 
            
manager = Connection()

# encryption algorithem



@app.websocket("/ws")
async def websocket_endpoint(websocket:WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            
            data = await websocket.receive_text()
            print(data)
            await manager.broadcast(data,sender=websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)                            
        
        
   
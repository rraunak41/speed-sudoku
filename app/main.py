from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Dict, List
from app.sudoku import Sudoku6x6

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class RoomManager:
    def __init__(self):
        self.active_rooms: Dict[str, List[WebSocket]] = {}
        self.game_states: Dict[str, dict] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.active_rooms:
            self.active_rooms[room_id] = []
        self.active_rooms[room_id].append(websocket)

    def disconnect(self, room_id: str, websocket: WebSocket):
        if room_id in self.active_rooms:
            if websocket in self.active_rooms[room_id]:
                self.active_rooms[room_id].remove(websocket)
            if len(self.active_rooms[room_id]) == 0:
                del self.active_rooms[room_id]
                if room_id in self.game_states:
                    del self.game_states[room_id]

    async def broadcast(self, room_id: str, message: dict):
        if room_id in self.active_rooms:
            for connection in self.active_rooms[room_id]:
                await connection.send_json(message)

manager = RoomManager()

@app.get("/")
async def get_index():
    return FileResponse("static/index.html")

@app.websocket("/ws/{room_id}/{player_name}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, player_name: str):
    await manager.connect(room_id, websocket)
    
    await manager.broadcast(room_id, {
        "event": "PLAYER_JOINED",
        "player": player_name,
        "count": len(manager.active_rooms[room_id])
    })

    if len(manager.active_rooms[room_id]) == 2:
        engine = Sudoku6x6()
        puzzle, solution = engine.generate_puzzle(clues=18)
        
        manager.game_states[room_id] = {
            "solution": solution,
            "status": "PLAYING"
        }
        
        await manager.broadcast(room_id, {
            "event": "GAME_START",
            "puzzle": puzzle,
            "solution": solution
        })

    try:
        while True:
            data = await websocket.receive_json()
            event = data.get("event")

            if event == "PROGRESS_UPDATE":
                await manager.broadcast(room_id, {
                    "event": "OPPONENT_PROGRESS",
                    "player": player_name,
                    "progress": data.get("progress")
                })

            elif event == "SUBMIT_WIN":
                user_board = data.get("board")
                solution = manager.game_states[room_id]["solution"]
                
                if user_board == solution:
                    await manager.broadcast(room_id, {
                        "event": "GAME_OVER",
                        "winner": player_name
                    })

            elif event == "REMATCH":
                # Generate new puzzle for rematch
                engine = Sudoku6x6()
                puzzle, solution = engine.generate_puzzle(clues=18)
                manager.game_states[room_id]["solution"] = solution
                
                await manager.broadcast(room_id, {
                    "event": "GAME_START",
                    "puzzle": puzzle,
                    "solution": solution
                })

    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
        await manager.broadcast(room_id, {
            "event": "PLAYER_DISCONNECTED",
            "player": player_name
        })
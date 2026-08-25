from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

current_command = {
    "command": "OFF",
    "r": 0,
    "g": 0,
    "b": 0
}


class NeoPixelCommand(BaseModel):
    command: str
    r: int = 0
    g: int = 0
    b: int = 0


@app.get("/")
def home():
    return FileResponse("index.html")


@app.post("/neopixel")
def set_neopixel(data: NeoPixelCommand):
    global current_command

    current_command = {
        "command": data.command.upper(),
        "r": max(0, min(255, data.r)),
        "g": max(0, min(255, data.g)),
        "b": max(0, min(255, data.b))
    }

    return {
        "status": "success",
        "neopixel": current_command
    }


@app.get("/neopixel")
def get_neopixel():
    return current_command

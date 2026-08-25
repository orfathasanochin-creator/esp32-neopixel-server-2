from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Templates(directory="templates")

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
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


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

from syrius.commands.LoopInputCommand import loopType
from syrius.commands.abstract import AbstractCommand, Command


class ReplicateImageSDXLCommand(Command):
    id: int = 50
    prompt: str | AbstractCommand | loopType
    width: int | AbstractCommand | loopType = 1024
    height: int | AbstractCommand | loopType = 1024
    scheduler: str | AbstractCommand | loopType = "K_EULER"
    guidance_scale: int | AbstractCommand | loopType = 0
    negative_prompt: str | AbstractCommand | loopType = "worst quality, low quality"
    num_inference_steps: int | AbstractCommand | loopType = 4
    api_key: str | AbstractCommand | loopType
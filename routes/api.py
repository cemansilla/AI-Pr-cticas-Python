from fastapi import APIRouter,Request,UploadFile,Form
from controllers.api.openai.chatgpt_controller import ChatGPTController
from controllers.api.openai.whisper_controller import WhisperController
from controllers.api.telegram.telegram_controller import TelegramController
from controllers.api.stable_diffusion.stable_diffusion_controller import StableDiffusionController
from controllers.api.custom.custom_controller import CustomController
from controllers.web import *

router = APIRouter()

@router.get("/")
def home():
  return dashboard_controller.get_dashboard()

@router.post("/api/test/ocr")
async def do_parse_ocr(file: UploadFile, file_name: str = Form(...)):
  custom_controller = CustomController()
  file_contents = await file.read()

  return custom_controller.ocr(file_contents, file_name)

@router.post("/api/telegram/set-webhook")
async def do_telegram_set_webhook(request: Request):
  telegram_controller = TelegramController()
  body = await request.json()

  return telegram_controller.set_webhook(body)

@router.post("/api/telegram/delete-webhook")
def do_telegram_delete_webhook():
  telegram_controller = TelegramController()

  return telegram_controller.delete_webhook()

@router.post("/api/telegram/send")
async def do_telegram_send(request: Request):
  telegram_controller = TelegramController()
  body = await request.json()

  return telegram_controller.send(body)

@router.post("/api/telegram/updates")
async def do_telegram_get_updates(request: Request):
  telegram_controller = TelegramController()
  body = await request.json()

  return telegram_controller.updates(body)

@router.get("/api/openai/chatgpt/chat")
async def do_chatgpt_chat(request: Request):
  chatgpt_controller = ChatGPTController()
  body = await request.json()

  return chatgpt_controller.chat(body)

@router.post("/pyapi/chat")
async def do_pyapi_chat(request: Request):
  chatgpt_controller = ChatGPTController()
  body = await request.json()

  return chatgpt_controller.chat(body)

@router.post("/pyapi/audio")
async def do_speech_to_text(file: UploadFile, file_name: str = Form(...)):
  whisper_controller = WhisperController()
  file_contents = await file.read()

  return await whisper_controller.speech_to_text(file_contents, file_name)

@router.post("/pyapi/image")
async def do_image_generate(request: Request):
  stable_diffusion_controller = StableDiffusionController()
  body = await request.json()

  return stable_diffusion_controller.generate_from_prompt(body)

@router.get("/pyapi/sd/models")
async def do_image_generate():
  stable_diffusion_controller = StableDiffusionController()

  return stable_diffusion_controller.get_models()

@router.post("/pyapi/post-rrss")
async def do_postrrss_generate(request: Request):
  custom_controller = CustomController()
  body = await request.json()

  return custom_controller.generate_post_rrss(body)

@router.post("/pyapi/sentiment")
async def do_parse_sentiment(request: Request):
  custom_controller = CustomController()
  body = await request.json()

  return custom_controller.sentiment(body)
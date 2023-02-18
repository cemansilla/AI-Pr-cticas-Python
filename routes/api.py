from fastapi import APIRouter,Request,UploadFile,Form
from controllers.api.openai.chatgpt_controller import ChatGPTController
from controllers.api.openai.whisper_controller import WhisperController
from controllers.api.telegram.telegram_controller import TelegramController
from controllers.web import *

router = APIRouter()

telegram_controller = TelegramController()
chatgpt_controller = ChatGPTController()
whisper_controller = WhisperController()

@router.get("/")
def home():
  return dashboard_controller.get_dashboard()

@router.post("/api/telegram/set-webhook")
async def do_telegram_set_webhook(request: Request):
  body = await request.json()
  return telegram_controller.set_webhook(body)

@router.post("/api/telegram/delete-webhook")
def do_telegram_delete_webhook():
  return telegram_controller.delete_webhook()

@router.post("/api/telegram/send")
async def do_telegram_send(request: Request):
  body = await request.json()
  return telegram_controller.send(body)

@router.post("/api/telegram/updates")
async def do_telegram_get_updates(request: Request):
  print("telegram updates routes", request)
  body = await request.json()
  return telegram_controller.updates(body)

@router.get("/api/openai/chatgpt/chat")
async def do_chatgpt_chat(request: Request):
  body = await request.json()
  return chatgpt_controller.chat(body)

@router.post("/pyapi/chat")
async def do_pyapi_chat(request: Request):
  body = await request.json()
  return chatgpt_controller.chat(body)

@router.post("/pyapi/audio")
async def do_speech_to_text(file: UploadFile, file_name: str = Form(...)):
  file_contents = await file.read()
  return await whisper_controller.speech_to_text(file_contents, file_name)
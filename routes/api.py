from fastapi import APIRouter
from controllers.api.openai.chatgpt_controller import ChatGPTController
from controllers.api.telegram.telegram_controller import TelegramController
from controllers.web.placeholder_controller import *

router = APIRouter()

@router.get("/")
async def home():
  return get_home()

@router.post("/telegram/set-webhook")
def do_telegram_set_webhook():
  return TelegramController.set_webhook()

@router.post("/telegram/send")
def do_telegram_send():
  return TelegramController.send()

@router.get("/telegram/updates")
def do_telegram_get_updates():
  return TelegramController.updates()

@router.get("/openai/chatgpt/chat")
def do_chatgpt_chat():
  return ChatGPTController.chat()
import os

from services.openai_service import OpenAIService

class WhisperController:
  def __init__(self):
    self.openai = OpenAIService()

  async def speech_to_text(self, file_contents: bytes, file_name: str):
    try:
      directory = 'data/audios/api'
      path = os.path.join(directory, file_name)

      if not os.path.exists(directory):
        os.makedirs(directory)

      with open(path, 'wb') as f:
        f.write(file_contents)
      
      speech_to_text = self.openai.transcribe(path)

      prompt = speech_to_text['text']
      return self.openai.completion(prompt)
    except Exception as e:
      return {"success": False, "error_message": str(e)}
import requests
import logging
#import whisper
from config.settings import *

class OpenAIService:
  def __init__():
    logging.basicConfig(filename='openai_service.log', level=logging.DEBUG)

  def completition(self, prompt):
    response = requests.post(OPENAI_API_BASE_URL + "completions", json={
      'model': "text-davinci-003",
      'prompt': prompt,
      'max_tokens': 128,
      'temperature': 0.5,
    }, headers={
      'Authorization': 'Bearer ' + OPENAI_API_KEY,
      'Content-Type': 'application/json',
    })

    gpt_response = response.json()
    gpt_response_text = gpt_response['choices'][0]['text'].lstrip("\r\n")

    logging.debug("Respuesta GPT-3", extra={'gpt_response': gpt_response})
    return gpt_response_text

  def transcribe(audio):
    return {"fake":"respuesta fake desde transcribe"}
    """
    # Cargo modelo
    model = whisper.load_model("base")
    model.device

    # Forma básica
    #result = model.transcribe("/content/openai-whisper-webapp/mary.mp3")
    #print(result["text"])

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    language = max(probs, key=probs.get)

    # decode the audio
    options = whisper.DecodingOptions(fp16 = False)
    result = whisper.decode(model, mel, options)
    return {"language": language, "text": result.text}
    """
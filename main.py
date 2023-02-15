import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api import router
from config.settings import *

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

app.include_router(router)

if __name__ == "__main__":
  if USE_NGROK:
    # pyngrok should only ever be installed or initialized in a dev environment when this flag is set
    from pyngrok import ngrok

    # Open a ngrok tunnel to the dev server
    ngrok.set_auth_token("2LbDfCormSj2F476pcyn7qWKgzV_7V3JJ1aA6fCrsLGB1WhT1")
    public_url = ngrok.connect(PORT).public_url
    print("ngrok tunnel \"{}\" -> \"{}:{}\"".format(public_url, BASE_URL, PORT))
  
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, log_level="info")
  else:
    uvicorn.run("main:app", host="localhost", port=PORT, log_level="info")
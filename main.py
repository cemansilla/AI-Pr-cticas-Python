import sys
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.example_routes import router
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
  def init_webhooks(base_url):
    # Update inbound traffic via APIs to use the public-facing ngrok URL
    pass

  if USE_NGROK:
    # pyngrok should only ever be installed or initialized in a dev environment when this flag is set
    from pyngrok import ngrok

    ngrok.set_auth_token("2LbDfCormSj2F476pcyn7qWKgzV_7V3JJ1aA6fCrsLGB1WhT1")

    # Get the dev server port (defaults to 8000 for Uvicorn, can be overridden with `--port`
    # when starting the server
    port = PORT

    # Open a ngrok tunnel to the dev server
    public_url = ngrok.connect(port).public_url
    print("ngrok tunnel \"{}\" -> \"{}:{}\"".format(public_url, BASE_URL, port))

    # Update any base URLs or webhooks to use the public ngrok URL
    BASE_URL = public_url
    init_webhooks(public_url)
  
  #public_url = ngrok.connect(port=5000)
  #print(f"La URL pública de tu aplicación es: {public_url}")
  config = uvicorn.Config("main:app", port=port, log_level="info", reload=True)
  server = uvicorn.Server(config)
  server.run()
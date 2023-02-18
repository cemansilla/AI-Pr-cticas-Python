# AI Prácticas Python

## Entorno virtual
### Activar entorno virtual
Mac: `source .venv/bin/activate`
Win: `.\.venv\Scripts\activate`

### Volcar paquetes a archivo requirements.txt
`pip freeze > requirements.txt`

### Instalar dependencias
`pip install -r requirements.txt`

## requerimientos
Para que funcione `whisper` se necesita tener instalado `ffmpeg`.

### Notas ffmpeg
Tuve varios errores en el proceso de utiliazar Whisper porque no reconocía ffmpeg dentro del entorno virtual.

Lo solucioné copiando en el root del entorno virtual los archivos ffmpeg.exe el resto que se instalaron con Scoop en mi PC.

Luego, una mejor alternativa fué especificar dentro del archivo "activate"del entorno virual el path a ffmpeg, agregar después de la inicialización de PATH lo siguiente en una nueva línea:
`set PATH=C:\Users\ceman\scoop\apps\ffmpeg\current\bin;%PATH%`

### on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

### on Arch Linux
sudo pacman -S ffmpeg

### on MacOS using Homebrew (https://brew.sh/)
brew install ffmpeg

### on Windows using Chocolatey (https://chocolatey.org/)
choco install ffmpeg

### on Windows using Scoop (https://scoop.sh/)
scoop install ffmpeg
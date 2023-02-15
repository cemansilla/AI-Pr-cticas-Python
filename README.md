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
Para corregirlo ejecuté: `setx PATH "%PATH%;C:\Users\ceman\scoop\apps\ffmpeg\5.1.2\bin\ffmpeg.exe"`, solo tener en cuenta modificar el path que corresponda a ffmpeg. De todas formas no me funcionó.

Lo solucioné copiando en el root del entorno virtual los archivos ffmpeg.exe el resto que se instalaron con Scoop en mi PC.

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
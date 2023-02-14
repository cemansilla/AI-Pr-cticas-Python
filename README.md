# AI Prácticas Python

## Entorno virtual
### Activar entorno virtual
`source .venv/bin/activate`

### Volcar paquetes a archivo requirements.txt
`pip freeze > requirements.txt`

### Instalar dependencias
`pip install -r requirements.txt`

Suponiendo que tengo esta estructura
```
app/
    config/
        __init__.py
        settings.py
    controllers/
        __init__.py
        example_controller.py
    models/
        __init__.py
        example_model.py
    routes/
        __init__.py
        example_route.py
    main.py
```

¿como incluyo dentro de example_controler.py a settings.py?
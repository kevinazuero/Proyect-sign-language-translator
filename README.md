# Detección de Señales de Mano con IA

Este proyecto consiste en una página web sencilla que permite **entrenar y utilizar un modelo de inteligencia artificial** capaz de detectar y clasificar señales hechas con la mano. Está pensado como una herramienta básica de reconocimiento de señas para futuras aplicaciones en accesibilidad o comunicación inclusiva.

## Características

- Entrenamiento de modelos de IA desde la misma interfaz web.
- Clasificación de señales de mano en tiempo real.
- Proyecto fácilmente extensible y personalizable.

## Puesta en marcha

1. Asegúrate de tener Python instalado.
2. Clona el repositorio:

3. Instala los requisitos (si aplica):

```
pip install -r requirements.txt
```

4. Crea una nueva base de datos y realiza las migraciones:

```
python manage.py makemigrations
```
```
python manage.py migrate
```
5. Inicia el servidor de desarrollo:
```
python manage.py runserver
```
Abre tu navegador en http://localhost:8000/.

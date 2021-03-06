from os import environ, path, getcwd, urandom
import logging
from pathlib import Path

from .auth import *
from .telemetry import *
from .services import *
from .github import *

LOG_LEVEL = environ.get('LOG', environ.get('LOGLEVEL', 'INFO')).upper()
if not LOG_LEVEL:
    LOG_LEVEL = 'INFO'
print(f"Setting log level to {LOG_LEVEL}")
LOG_LEVEL = getattr(logging, LOG_LEVEL)
logging.basicConfig(level=LOG_LEVEL)

DOMAIN = environ.get('domain', 'pointillism.io')
HOST = environ.get('HOST', 'https://raw.githubusercontent.com')
ENV = environ.get('ENV', "PROD")

STATIC_DIR = getcwd()
THEME_DIR = environ.get("THEME_DIR", path.join(STATIC_DIR, "themes"))

if not STATIC_DIR or STATIC_DIR == '/':
    STATIC_DIR = '/srv/vhosts/pointillism'
else:
    STATIC_DIR += '/public'

SECRET_KEY = urandom(12)

# TODO fail if missing
PLANT_JAR = environ.get("PLANT_JAR", "/opt/plantuml.jar")
logging.info(f"Using {PLANT_JAR}")

WILL_BRAND = environ.get('WILL_BRAND', "1").lower() in ["1", "true"]
if not WILL_BRAND:
    logging.info(f"WILL_BRAND {WILL_BRAND}")

GA_TRACKING_ID = 'UA-165967713-1'

PROJECT_ROOT = str(Path(__file__).parent.parent)

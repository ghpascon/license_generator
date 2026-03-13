from .config import Settings
from smartx_rfid.utils.logger_manager import LoggerManager
import os
from .build_templates import TemplateManager
from .indicator import Indicator
from smartx_rfid.utils.path import get_frozen_path
from smartx_rfid.utils import AlertsManager
from app.db import setup_database

# DEFAULT VARS
FILES_PATH = get_frozen_path('config')
DOCS_PATH = get_frozen_path('docs')
SWAGGER_PATH = f'{DOCS_PATH}/SWAGGER.md'
CONFIG_PATH = f'{FILES_PATH}/config.json'
TEMPLATES_PATH = get_frozen_path('app/templates')
DEVICES_PATH = f'{FILES_PATH}/devices'
ICON_PATH = get_frozen_path('app/static/icons/logo.ico')
EXAMPLE_PATH = get_frozen_path('examples')

##CONFIG APLICATION
# settings
settings = Settings(CONFIG_PATH)

# logging
logger = LoggerManager(
	log_path=settings.LOG_PATH,
	storage_days=settings.STORAGE_DAYS,
	base_filename=os.path.basename(os.getcwd()),
)

# templates
templates = TemplateManager(TEMPLATES_PATH).templates

# alerts
alerts_manager = AlertsManager()

# db
db_manager = setup_database(database_url=settings.DATABASE_URL)

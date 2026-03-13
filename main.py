"""
SMARTX Connector - RFID Device Management Application
To run the application using Poetry:
	poetry run python main.py
"""

# ruff: noqa: E402

# LIBS
import sys

sys.coinit_flags = 0
import asyncio

if hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
import logging
import webbrowser
import uvicorn
from app.core import settings, SWAGGER_PATH

# APP
from app.core.build_app import create_application

# SMARTX-RFID
from smartx_rfid.utils.path import get_frozen_path

# db to create tables
import app.db

logging.info('Application starting...')

# Create the FastAPI application instance
app = create_application(title=settings.TITLE, swagger_path=SWAGGER_PATH)

# Server startup code
if __name__ == '__main__':
	# Get port and host from settings or use defaults
	port = settings.PORT
	host = '0.0.0.0'

	logging.info(f'Starting server on {host}:{port}')

	# Start uvicorn server
	try:
		uvicorn.run(
			app, host=host, port=port, access_log=False, log_level='critical', log_config=None
		)
	except SystemExit as e:
		logging.error(f'Server exited with SystemExit: {e}')
		error_html = get_frozen_path('app/templates/start_error.html')
		url = f'file://{error_html}'
		webbrowser.open_new(url)

	except Exception as e:
		logging.error(f'Failed to start server: {e}')

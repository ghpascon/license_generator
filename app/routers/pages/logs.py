from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
import json
import os
from datetime import datetime
from typing import Dict, Any
from app.core import templates
from app.core import logger

router = APIRouter(prefix='', tags=['Logs'])


async def get_log_content() -> Dict[str, Any]:
	"""
	Function to fetch log content and file information.

	Returns:
		Dict containing log content and file metadata
	"""
	# Get today's log file
	file_path = logger._get_filename_for_date(datetime.now().date())

	# Read file content safely
	try:
		with open(file_path, 'r', encoding='utf-8') as f:
			log_lines = f.readlines()
		# Remove empty lines but DON'T reverse order (frontend handles this)
		log_content = [line.strip() for line in log_lines if line.strip()]
	except FileNotFoundError:
		log_content = [
			json.dumps(
				{
					'level': 'ERROR',
					'message': 'Log file not found.',
					'timestamp': datetime.now().isoformat(),
				}
			)
		]
	except Exception as e:
		log_content = [
			json.dumps(
				{
					'level': 'ERROR',
					'message': f'Error reading log file: {str(e)}',
					'timestamp': datetime.now().isoformat(),
				}
			)
		]

	# Additional information about the log file
	log_info = {
		'file_path': file_path,
		'file_exists': os.path.exists(file_path),
		'file_size': os.path.getsize(file_path) if os.path.exists(file_path) else 0,
		'last_modified': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime(
			'%Y-%m-%d %H:%M:%S'
		)
		if os.path.exists(file_path)
		else 'N/A',
		'total_lines': len(log_content),
		'timestamp': datetime.now().isoformat(),
	}

	return {'content': log_content, 'info': log_info}


@router.get('/logs', response_class=HTMLResponse)
async def logs(request: Request):
	return templates.TemplateResponse(
		'pages/logs/main.html',
		{'request': request, 'title': 'Logs', 'alerts': []},
		media_type='text/html; charset=utf-8',
	)


@router.get('/logs/get_content')
async def get_logs_content():
	log_data = await get_log_content()
	return JSONResponse(
		content=log_data, headers={'Cache-Control': 'no-cache, no-store, must-revalidate'}
	)

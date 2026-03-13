from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.core import templates

router = APIRouter(prefix='', tags=['Pages'])


@router.get('/settings/application', response_class=HTMLResponse)
async def settings_page(request: Request):
	return templates.TemplateResponse(
		'pages/application_settings/main.html',
		{'request': request, 'title': 'Settings', 'alerts': []},
		media_type='text/html; charset=utf-8',
	)

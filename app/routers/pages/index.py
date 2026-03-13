from fastapi import APIRouter, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

from app.core import settings, templates

router = APIRouter(prefix='', tags=['Pages'])


@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
	return templates.TemplateResponse(
		'pages/index/main.html',
		{'request': request, 'title': settings.TITLE},
		media_type='text/html; charset=utf-8',
	)


@router.get('/docs', response_class=HTMLResponse)
async def docs(request: Request):
	return get_swagger_ui_html(
		openapi_url='/openapi.json',
		title=settings.TITLE + ' - Docs',
		swagger_js_url='/static/docs/swagger-ui-bundle.js',
		swagger_css_url='/static/docs/swagger-ui.css',
		swagger_favicon_url='/static/images/logo.png',
	)

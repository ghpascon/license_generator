from fastapi import APIRouter
from fastapi.responses import JSONResponse
from smartx_rfid.utils.path import get_prefix_from_path

from app.services.controller import controller
from app.schemas.controller import LicenseRequest

router_prefix = get_prefix_from_path(__file__)
router = APIRouter(prefix=router_prefix, tags=[router_prefix])


@router.post('/generate_license_from_request_string')
async def generate_license_from_request_string(request: LicenseRequest):
	success, result = controller.generate_license_from_request_string(**request.model_dump())
	if success:
		return JSONResponse(content={'license': result})
	else:
		return JSONResponse(content={'error': result}, status_code=400)

from typing import Optional

from pydantic import BaseModel, Field


class LicenseRequest(BaseModel):
	request_string: str = Field(..., description='The license request string')
	days: int = Field(..., description='Duration of the license in days')
	data: Optional[dict] = Field({}, description='Additional data to include in the license')

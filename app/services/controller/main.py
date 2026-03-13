import logging

from typing import Tuple

from smartx_rfid.license.main import LicenseManager
from smartx_rfid.models.license import License

from app.db import setup_database
from app.core import settings


class Controller:
	def __init__(self):
		self.db_manager = setup_database(database_url=settings.DATABASE_URL)

	def generate_license_from_request_string(
		self, request_string: str, days: int, data: dict = {}
	) -> Tuple[bool, str]:
		"""
		Generates a license based on the provided request string.
		Returns a tuple (success: bool, message: str).
		"""
		try:
			# Parse the request string to extract public key and hardware ID
			license_data = LicenseManager.parse_license_request_string(request_string)
			public_key = license_data.get('public_key')
			public_key = public_key.strip() if public_key else None
			hardware_id = license_data.get('hardware_id')
			logging.info(
				f'Parsed license request - Public Key: {public_key}, Hardware ID: {hardware_id}'
			)
			if not public_key or not hardware_id:
				return False, 'Invalid request string: Missing public key or hardware ID.'

			# Verify if public key is on DB
			private_key = self._get_private_key_from_db(public_key)
			if not private_key:
				return False, 'Public key not found in database.'

			license_manager = LicenseManager(private_key_pem=private_key, public_key_pem=public_key)
			license_str = license_manager.create_license(
				hardware_id=hardware_id, duration_days=days, data=data
			)
			logging.info(f'Generated license string: {license_str}')
			return True, license_str
		except Exception as e:
			logging.error(f'Error generating license: {e}', exc_info=True)
			return False, f'Error generating license: {str(e)}'

	def _get_private_key_from_db(self, public_key: str) -> str:
		try:
			with self.db_manager.get_session() as session:
				license_entry: License = (
					session.query(License).filter_by(public_key=public_key).first()
				)
				if not license_entry:
					return None
				return license_entry.private_key
		except Exception as e:
			logging.error(f'Database error while retrieving private key: {e}', exc_info=True)
			return None

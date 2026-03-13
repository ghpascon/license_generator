import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / 'app/services/controller/main.py'


@pytest.fixture
def controller_module(monkeypatch):
	fake_app = ModuleType('app')
	fake_db = ModuleType('app.db')
	fake_core = ModuleType('app.core')

	fake_db.setup_database = lambda database_url=None: None
	fake_core.settings = SimpleNamespace(DATABASE_URL='sqlite:///:memory:')
	fake_app.db = fake_db
	fake_app.core = fake_core

	monkeypatch.setitem(sys.modules, 'app', fake_app)
	monkeypatch.setitem(sys.modules, 'app.db', fake_db)
	monkeypatch.setitem(sys.modules, 'app.core', fake_core)

	spec = importlib.util.spec_from_file_location('test_controller_main', MODULE_PATH)
	module = importlib.util.module_from_spec(spec)
	assert spec.loader is not None
	spec.loader.exec_module(module)
	return module


@pytest.fixture
def controller(controller_module):
	instance = controller_module.Controller.__new__(controller_module.Controller)
	instance.db_manager = None
	return instance


def test_generate_license_from_request_string_success(controller, controller_module, monkeypatch):
	create_license_calls = []

	class FakeLicenseManager:
		def __init__(self, private_key_pem, public_key_pem):
			self.private_key_pem = private_key_pem
			self.public_key_pem = public_key_pem

		@staticmethod
		def parse_license_request_string(request_string):
			assert request_string == 'request-string'
			return {'public_key': ' PUBLIC KEY ', 'hardware_id': 'HW-123'}

		def create_license(self, hardware_id, duration_days, data):
			create_license_calls.append(
				{
					'private_key_pem': self.private_key_pem,
					'public_key_pem': self.public_key_pem,
					'hardware_id': hardware_id,
					'duration_days': duration_days,
					'data': data,
				}
			)
			return 'generated-license'

	monkeypatch.setattr(controller_module, 'LicenseManager', FakeLicenseManager)
	monkeypatch.setattr(controller, '_get_private_key_from_db', lambda public_key: 'private-key')

	success, result = controller.generate_license_from_request_string(
		request_string='request-string',
		days=30,
		data={'customer': 'ACME'},
	)

	assert success is True
	assert result == 'generated-license'
	assert create_license_calls == [
		{
			'private_key_pem': 'private-key',
			'public_key_pem': 'PUBLIC KEY',
			'hardware_id': 'HW-123',
			'duration_days': 30,
			'data': {'customer': 'ACME'},
		}
	]


@pytest.mark.parametrize(
	'parsed_request',
	[
		{'public_key': None, 'hardware_id': 'HW-123'},
		{'public_key': 'PUBLIC KEY', 'hardware_id': None},
		{'public_key': '   ', 'hardware_id': 'HW-123'},
	],
)
def test_generate_license_from_request_string_rejects_invalid_request(
	controller,
	controller_module,
	monkeypatch,
	parsed_request,
):
	class FakeLicenseManager:
		@staticmethod
		def parse_license_request_string(request_string):
			assert request_string == 'request-string'
			return parsed_request

	monkeypatch.setattr(controller_module, 'LicenseManager', FakeLicenseManager)

	success, result = controller.generate_license_from_request_string('request-string', 30)

	assert success is False
	assert result == 'Invalid request string: Missing public key or hardware ID.'


def test_generate_license_from_request_string_returns_error_when_public_key_not_found(
	controller,
	controller_module,
	monkeypatch,
):
	class FakeLicenseManager:
		@staticmethod
		def parse_license_request_string(request_string):
			assert request_string == 'request-string'
			return {'public_key': 'PUBLIC KEY', 'hardware_id': 'HW-123'}

	monkeypatch.setattr(controller_module, 'LicenseManager', FakeLicenseManager)
	monkeypatch.setattr(controller, '_get_private_key_from_db', lambda public_key: None)

	success, result = controller.generate_license_from_request_string('request-string', 30)

	assert success is False
	assert result == 'Public key not found in database.'


def test_generate_license_from_request_string_wraps_parse_errors(
	controller,
	controller_module,
	monkeypatch,
):
	class FakeLicenseManager:
		@staticmethod
		def parse_license_request_string(request_string):
			raise ValueError('boom')

	monkeypatch.setattr(controller_module, 'LicenseManager', FakeLicenseManager)

	success, result = controller.generate_license_from_request_string('request-string', 30)

	assert success is False
	assert result == 'Error generating license: boom'


def test_generate_license_from_request_string_wraps_create_license_errors(
	controller,
	controller_module,
	monkeypatch,
):
	class FakeLicenseManager:
		def __init__(self, private_key_pem, public_key_pem):
			self.private_key_pem = private_key_pem
			self.public_key_pem = public_key_pem

		@staticmethod
		def parse_license_request_string(request_string):
			return {'public_key': 'PUBLIC KEY', 'hardware_id': 'HW-123'}

		def create_license(self, hardware_id, duration_days, data):
			raise RuntimeError('cannot create')

	monkeypatch.setattr(controller_module, 'LicenseManager', FakeLicenseManager)
	monkeypatch.setattr(controller, '_get_private_key_from_db', lambda public_key: 'private-key')

	success, result = controller.generate_license_from_request_string('request-string', 30)

	assert success is False
	assert result == 'Error generating license: cannot create'

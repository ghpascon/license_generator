import json
import logging
import os


class Settings:
	def __init__(self, config_path):
		"""Application settings loader and manager."""
		self._config_path = config_path
		self.load()

	def load(self, data: dict | None = None):
		"""Load configuration from JSON file."""
		if data is None:
			data = {}

			if os.path.exists(self._config_path):
				try:
					with open(self._config_path, 'r', encoding='utf8') as f:
						data = json.load(f)
				except Exception as e:
					logging.error(f'Error loading {self._config_path}: {e}')

		# Replace all empty string values with None recursively
		def replace_empty_with_none(obj):
			if isinstance(obj, dict):
				return {k: replace_empty_with_none(v) for k, v in obj.items()}
			elif isinstance(obj, list):
				return [replace_empty_with_none(v) for v in obj]
			elif obj == '':
				return None
			else:
				return obj

		data = replace_empty_with_none(data)

		# Load variables with defaults
		self.TITLE: str = data.get('TITLE', 'SMARTX')
		self.LOG_PATH: str = data.get('LOG_PATH', 'Logs')
		self.DATABASE_URL: str | None = data.get('DATABASE_URL', None)
		self.PORT: int = data.get('PORT', 5000)
		self.STORAGE_DAYS: int = data.get('STORAGE_DAYS', 7)

	def get_current_settings(self):
		return {
			key: value
			for key, value in vars(self).items()
			if not key.startswith('_') and not callable(value)
		}

	def save(self):
		"""Save all instance attributes except _config_path to JSON file."""
		try:
			logging.info(f'Saving config to: {self._config_path}')

			# Dynamically get all attributes except _config_path
			data = self.get_current_settings()

			# Make sure folder exists
			os.makedirs(os.path.dirname(self._config_path), exist_ok=True)

			with open(self._config_path, 'w', encoding='utf8') as f:
				json.dump(data, f, indent=4, ensure_ascii=False)

		except Exception as e:
			logging.error(f'Error saving config: {e}')

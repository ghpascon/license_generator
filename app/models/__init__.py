"""
Model auto-discovery module for SMARTX Connector.

This module automatically discovers and imports all SQLAlchemy models
from the models package, providing a centralized access point.

To add external model modules, append their dotted paths to EXTERNAL_MODEL_MODULES:
    EXTERNAL_MODEL_MODULES = [
        "smartx_rfid.models.products",
        "my_package.models.entities",
    ]
"""

import importlib
import inspect
import pkgutil
from typing import List, Type

try:
	from sqlalchemy.orm import DeclarativeBase
except ImportError:
	from sqlalchemy.ext.declarative import declarative_base

	DeclarativeBase = declarative_base()

# -----------------------------------------------------------------
# Add here any external module paths whose SQLAlchemy models should
# be auto-imported and registered with the metadata / Base.
# -----------------------------------------------------------------
EXTERNAL_MODEL_MODULES: List[str] = [
	'smartx_rfid.models.license',
]


def _load_external_models() -> List[Type]:
	"""Import every SQLAlchemy model class found in EXTERNAL_MODEL_MODULES."""
	discovered: List[Type] = []
	current_globals = globals()

	for module_path in EXTERNAL_MODEL_MODULES:
		try:
			module = importlib.import_module(module_path)
		except ImportError as exc:
			print(f"[models] Could not import '{module_path}': {exc}")
			continue

		for attr_name in dir(module):
			attr = getattr(module, attr_name)
			if (
				inspect.isclass(attr)
				and hasattr(attr, '__tablename__')
				and hasattr(attr, '__table__')
			):
				discovered.append(attr)
				# Expose the class in this package's namespace
				current_globals[attr_name] = attr
			elif inspect.isclass(attr) or not inspect.isroutine(attr):
				# Also re-export non-model symbols (Base, BaseMixin, …)
				# only if they originate from the target module
				if getattr(attr, '__module__', None) == module_path:
					current_globals[attr_name] = attr

	return discovered


# Run on import so every model is registered before Alembic / the app start
_external_models: List[Type] = _load_external_models()


def get_all_models() -> List[Type]:
	"""
	Return all SQLAlchemy model classes registered via EXTERNAL_MODEL_MODULES
	plus any models defined directly inside this package.

	Returns:
	    List[Type]: List of all discovered model classes
	"""
	models: List[Type] = list(_external_models)

	# Also scan submodules defined locally inside app/models/
	current_module = inspect.getmodule(inspect.currentframe())
	current_package = current_module.__package__ if current_module else None

	if current_package:
		for _, name, _ in pkgutil.iter_modules(__path__, current_package + '.'):
			try:
				module = importlib.import_module(name)
				for attr_name in dir(module):
					attr = getattr(module, attr_name)
					if (
						inspect.isclass(attr)
						and hasattr(attr, '__tablename__')
						and hasattr(attr, '__table__')
						and attr.__module__ == name
						and attr not in models
					):
						models.append(attr)
			except (ImportError, AttributeError):
				continue

	return models

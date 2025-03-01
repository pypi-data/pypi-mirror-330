"""
DjangAutomate
=============

A framework to automate Django app, model, serializer, and view generation
from SQLAlchemy database tables.

Modules:
--------
- `core` : Main class for automating Django app creation.
- `generators` : Classes for generating models, views, serializers, and app config.
- `utils` : Helper functions for updating URLs and settings.

Usage:
------
>>> from djangautomate import Djangautomate
>>> automator = Djangautomate("sqlite:///example.db", "users", app_name="my_app")
>>> automator.generate_code_files()
"""

from .core import Djangautomate
from .generators import ModelGenerator, ViewGenerator, SerializerGenerator, AppConfigGenerator
from .utils import update_urls, update_settings

__all__ = [
    "Djangautomate",
    "ModelGenerator",
    "ViewGenerator",
    "SerializerGenerator",
    "AppConfigGenerator",
    "update_urls",
    "update_settings"
]

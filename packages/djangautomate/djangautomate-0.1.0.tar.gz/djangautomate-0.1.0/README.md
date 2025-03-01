# DjangAutomate

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-orange.svg)](https://www.sqlalchemy.org/)

## Overview
**DjangAutomate** automates the creation of Django apps, models, serializers, and views directly from SQLAlchemy database tables. It eliminates manual code writing, enforces consistency, and speeds up development for Django projects.

## Features
- **Automatic Model Generation**: Converts SQLAlchemy tables into Django models.
- **Serializer & View Generation**: Generates Django REST Framework serializers and views.
- **Seamless ORM Transition**: Helps migrate from SQLAlchemy to Django ORM.
- **Configurable & Extensible**: Customize generators to fit your project.

## Installation
Install DjangAutomate using pip:

```bash
pip install djangautomate
```

Or using Poetry:

```bash
poetry add djangautomate
```

## Usage

### Generate Django Models from SQLAlchemy
```python
from djangautomate.generators import ModelGenerator

generator = ModelGenerator("sqlite:///example.db", "your_table")
model_code = generator.generate()
print(model_code)
```

### Automate Full Django App Generation
```python
from djangautomate import Djangautomate

automator = Djangautomate("sqlite:///example.db", "users", app_name="my_app")
automator.generate_code_files()
```

## Documentation
The full documentation is hosted on **Read the Docs**:

[https://djangautomate.readthedocs.io](https://djangautomate.readthedocs.io)

To build the documentation locally:

```bash
git clone https://github.com/pr1m8/djangautomate.git
cd djangautomate/docs
make html
```

## Contributing
See [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution guidelines.

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file.

## Author
Developed by **pr1m8** ([GitHub](https://github.com/pr1m8)).


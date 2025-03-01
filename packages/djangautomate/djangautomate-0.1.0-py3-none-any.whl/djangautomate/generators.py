import sqlalchemy

class ModelGenerator:
    """
    Generates Django model code from an SQLAlchemy table.

    Attributes:
        db_engine (sqlalchemy.engine.Engine): The SQLAlchemy database engine.
        table_name (str): The name of the SQLAlchemy table to convert to a Django model.
        index_cols (list[str]): A list of indexed columns.
    """

    def __init__(self, db_engine, table_name, index_cols):
        """
        Initializes the ModelGenerator class.

        Args:
            db_engine (sqlalchemy.engine.Engine): The SQLAlchemy database engine.
            table_name (str): The name of the table to generate the model from.
            index_cols (list[str]): A list of indexed columns.
        """
        self.db_engine = db_engine
        self.table_name = table_name
        self.index_cols = index_cols

    def generate(self) -> str:
        """
        Generates Django model code from the SQLAlchemy table.

        Returns:
            str: The generated Django model code.
        """
        model_code = "from django.db import models\n\n"
        model_code += f"class {self.table_name.capitalize()}(models.Model):\n"
        metadata = sqlalchemy.MetaData()
        table = sqlalchemy.Table(self.table_name, metadata, autoload_with=self.db_engine)
        
        for col in table.c:
            if col.name == 'index':
                continue
            model_code += f"    {col.name} = models.{self.get_field_type(col.type)}\n"

        model_code += "    class Meta:\n"
        model_code += f"        db_table = '{self.table_name}'\n"
        return model_code

    def get_field_type(self, col_type) -> str:
        """
        Maps SQLAlchemy column types to Django model field types.

        Args:
            col_type (sqlalchemy.types.TypeEngine): The SQLAlchemy column type.

        Returns:
            str: The corresponding Django model field type.
        """
        if isinstance(col_type, sqlalchemy.String):
            return "CharField(max_length=255)"
        elif isinstance(col_type, sqlalchemy.Integer):
            return "IntegerField()"
        elif isinstance(col_type, sqlalchemy.Float):
            return "FloatField()"
        elif isinstance(col_type, sqlalchemy.Boolean):
            return "BooleanField()"
        elif isinstance(col_type, sqlalchemy.DateTime):
            return "DateTimeField()"
        return "TextField()"


class ViewGenerator:
    """
    Generates Django ViewSet code for the given model.

    Attributes:
        app_name (str): The name of the Django app.
        camelcased_app_name (str): The app name in CamelCase format.
    """

    def __init__(self, app_name: str):
        """
        Initializes the ViewGenerator class.

        Args:
            app_name (str): The name of the Django app.
        """
        self.app_name = app_name
        self.camelcased_app_name = app_name.capitalize()

    def generate(self) -> str:
        """
        Generates Django ViewSet code for the model.

        Returns:
            str: The generated Django ViewSet code.
        """
        return f"""
from .models import {self.camelcased_app_name}
from .serializers import {self.camelcased_app_name}Serializer
from rest_framework import viewsets

class {self.camelcased_app_name}ViewSet(viewsets.ModelViewSet):
    queryset = {self.camelcased_app_name}.objects.all()
    serializer_class = {self.camelcased_app_name}Serializer
"""


class SerializerGenerator:
    """
    Generates Django REST Framework serializer code.

    Attributes:
        db_engine (sqlalchemy.engine.Engine): The SQLAlchemy database engine.
        table_name (str): The name of the SQLAlchemy table to generate a serializer for.
    """

    def __init__(self, db_engine, table_name: str):
        """
        Initializes the SerializerGenerator class.

        Args:
            db_engine (sqlalchemy.engine.Engine): The SQLAlchemy database engine.
            table_name (str): The name of the table to generate the serializer for.
        """
        self.db_engine = db_engine
        self.table_name = table_name

    def generate(self) -> str:
        """
        Generates Django REST Framework serializer code.

        Returns:
            str: The generated serializer code.
        """
        return f"""
from rest_framework import serializers
from .models import {self.table_name.capitalize()}

class {self.table_name.capitalize()}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {self.table_name.capitalize()}
        fields = '__all__'
"""


class AppConfigGenerator:
    """
    Generates Django app configuration.

    Attributes:
        app_name (str): The name of the Django app.
    """

    def __init__(self, app_name: str):
        """
        Initializes the AppConfigGenerator class.

        Args:
            app_name (str): The name of the Django app.
        """
        self.app_name = app_name.capitalize()

    def generate(self) -> str:
        """
        Generates Django app configuration.

        Returns:
            str: The generated Django app configuration.
        """
        return f"""
from django.apps import AppConfig

class {self.app_name}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'endpoints.{self.app_name.lower()}'
"""

import os
import subprocess
import sqlalchemy
from djangautomate.generators import ModelGenerator, ViewGenerator, SerializerGenerator, AppConfigGenerator
from djangautomate.utils import update_urls, update_settings


class Djangautomate:
    """
    Automates Django app creation by generating models, views, serializers, templates, and updating configurations.

    Attributes:
        db_engine (sqlalchemy.engine.Engine): The SQLAlchemy database engine.
        table_name (str): The name of the table to generate models from.
        index_cols (list[str], optional): List of indexed columns. Defaults to an empty list.
        app_name (str): The Django app name.
        project_name (str): The Django project name.
        camelcased_app_name (str): The formatted app name in CamelCase.
        viewset_name (str): The generated name for the Django ViewSet.
        serializer_name (str): The generated name for the Django Serializer.
    """

    def __init__(self, db_engine, table_name, index_cols=None, app_name='', project_name=''):
        """
        Initializes the Djangautomate class.

        Args:
            db_engine (sqlalchemy.engine.Engine): The SQLAlchemy database engine.
            table_name (str): The name of the SQLAlchemy table.
            index_cols (list[str], optional): List of indexed columns. Defaults to an empty list.
            app_name (str, optional): The Django app name. Defaults to an empty string.
            project_name (str, optional): The Django project name. Defaults to an empty string.
        """
        self.db_engine = db_engine
        self.table_name = table_name
        self.index_cols = index_cols or []
        self.app_name = app_name
        self.project_name = project_name

        self.camelcased_app_name = "".join([part.capitalize() for part in self.app_name.split('_')])
        self.viewset_name = f"{self.camelcased_app_name}ViewSet"
        self.serializer_name = f"{self.camelcased_app_name}Serializer"

    def create_django_app(self):
        """
        Creates a new Django app using `django-admin startapp`.

        This function runs the Django CLI command to initialize a new app inside the current project.
        """
        subprocess.run(['django-admin', 'startapp', self.app_name])

    def generate_code_files(self):
        """
        Generates all necessary Django files, including models, views, serializers, and app configuration.

        This function:
        - Creates the Django app directory (if it doesn't exist).
        - Generates the model, view, and serializer code using `ModelGenerator`, `ViewGenerator`, and `SerializerGenerator`.
        - Writes the generated code to respective files inside the app directory.
        - Updates Django's `urls.py` and `settings.py` to include the new app.

        Raises:
            Exception: If the Django app directory cannot be created.
        """
        app_directory = os.path.join(os.getcwd(), self.app_name)

        if not os.path.exists(app_directory):
            self.create_django_app()

        model_code = ModelGenerator(self.db_engine, self.table_name, self.index_cols).generate()
        view_code = ViewGenerator(self.app_name).generate()
        serializer_code = SerializerGenerator(self.db_engine, self.table_name).generate()
        app_code = AppConfigGenerator(self.app_name).generate()

        self._write_file(os.path.join(app_directory, "models.py"), model_code)
        self._write_file(os.path.join(app_directory, "views.py"), view_code)
        self._write_file(os.path.join(app_directory, "serializers.py"), serializer_code)
        self._write_file(os.path.join(app_directory, "apps.py"), app_code)

        update_urls(self.app_name, self.viewset_name)
        update_settings(self.app_name, self.camelcased_app_name)

        print(f"Code files generated for {self.project_name} successfully!")

    def _write_file(self, file_path: str, content: str):
        """
        Writes content to a file, creating it if it doesn't exist.

        Args:
            file_path (str): The path to the file.
            content (str): The content to write into the file.

        If the file already exists, the content is appended instead of being overwritten.
        """
        mode = 'a' if os.path.isfile(file_path) else 'w'
        with open(file_path, mode) as file:
            file.write(content)

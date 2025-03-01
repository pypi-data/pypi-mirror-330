import os

def update_urls(app_name: str, viewset_name: str):
    """
    Updates Django's `urls.py` to include the newly generated app's ViewSet.

    This function appends the required import statement and router registration 
    for the new Django app's view.

    Args:
        app_name (str): The name of the Django app.
        viewset_name (str): The name of the ViewSet class.
    
    Raises:
        FileNotFoundError: If `urls.py` is not found in the expected path.
    """
    urls_path = os.path.join(os.getcwd(), '..', 'delphi_api', 'urls.py')
    
    if not os.path.exists(urls_path):
        raise FileNotFoundError(f"urls.py not found at {urls_path}")

    with open(urls_path, 'a') as url_file:
        url_file.write(f"\nfrom endpoints.{app_name}.views import {viewset_name}\n")
        url_file.write(f"router.register(r'{app_name}', {viewset_name}, '{app_name}')\n")


def update_settings(app_name: str, camelcased_app_name: str):
    """
    Adds the generated Django app to `INSTALLED_APPS` in `settings.py`.

    This function appends the app configuration class to Django’s `INSTALLED_APPS`
    list, ensuring it is registered correctly.

    Args:
        app_name (str): The name of the Django app.
        camelcased_app_name (str): The app name in CamelCase format for the config class.
    
    Raises:
        FileNotFoundError: If `settings.py` is not found in the expected path.
    """
    settings_path = os.path.join(os.getcwd(), '..', 'delphi_api', 'settings.py')

    if not os.path.exists(settings_path):
        raise FileNotFoundError(f"settings.py not found at {settings_path}")

    with open(settings_path, 'a') as settings_file:
        settings_file.write(f"INSTALLED_APPS.append('endpoints.{app_name}.apps.{camelcased_app_name}Config')\n")

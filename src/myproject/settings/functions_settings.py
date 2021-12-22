import os
import json
from django.core.exceptions import ImproperlyConfigured


def get_last_update(base_dir: str) -> str:
    """Read the file last modified, which contains the date of the last modification of the project, updated using git hook"""
    with open(os.path.join(base_dir, 'myproject', 'settings', 'last-update.txt'), 'r') as f:
        last_modified = f.readline().strip()

    return last_modified


class Secrets:
    """Recover settings.txt to different source"""
    values = dict()

    @staticmethod
    def get_secret_json(setting: str) -> str:

        if len(Secrets.values) == 0:
            with open(os.path.join(os.path.dirname(__file__), 'secrets.json'), 'r') as f:
                Secrets.values.update(json.loads(f.read()))

        try:
            return Secrets.values[setting]
        except KeyError:
            error_msg = f'Set the {setting} secret variable'
            raise ImproperlyConfigured(error_msg)

    @staticmethod
    def get_secret_environment(setting: str) -> str:
        try:
            return os.environ[setting]
        except KeyError:
            error_msg = f'Set the {setting} environment variable'
            raise ImproperlyConfigured(error_msg)

    @staticmethod
    def get_secret(setting: str) -> str:
        """Get the secret variables or return explicit exception."""
        try:
            source_type = Secrets.get_secret_environment("SOURCE_TYPE")
        except ImproperlyConfigured:
            source_type = "JSON"  # default source

        source_options = dict(
            JSON=Secrets.get_secret_json,
            ENVIRONMENT=Secrets.get_secret_environment
        )

        return source_options[source_type](setting)

import os


class ImproperlyConfigured(Exception):
    def __init__(self, variable_name: str, *args, **kwargs):
        self.variable_name = variable_name
        self.message = f"Set the {variable_name} environment variable."
        super().__init__(self.message, *args, **kwargs)


def getenv(var_name: str, cast_to=str) -> str:
    try:
        value = os.environ[var_name]
        return cast_to(value)
    except KeyError:
        raise ImproperlyConfigured(var_name)
    except ValueError:
        raise ValueError(f"The value {value} can't be cast to {cast_to}.")

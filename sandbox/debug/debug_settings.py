from cflarepy.libs import settings
from dynaconf import Dynaconf


def debug_settings(settings_obj: Dynaconf, name: str = "<unknown>") -> None:
    try:
        print(f"{name} settings: {settings_obj.as_dict()}")
    except Exception as exc:
        msg = f"[ERROR] ({type(exc)}) Unhandled exception printing settings object. Details: {exc}"
        print(msg)


if __name__ == "__main__":
    ## Debug logging settings
    debug_settings(name="logging", settings_obj=settings.LOGGING_SETTINGS)

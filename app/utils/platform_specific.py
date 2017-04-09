"""

"""
import platform


def is_windows() -> bool:
    if 'win' in str(platform.system()).lower():
        return True
    else:
        return False


def format_path(path: str) -> str:
    if not is_windows():
        new_path = path.replace('\\', '/')
    else:
        new_path = path.replace('/', '\\')
    return new_path

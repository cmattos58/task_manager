"""Django's command-line utility for administrative tasks."""

import os
import sys


print(sys.argv)


def run_flake8():
    """Run Flake8 linting."""
    os.system("flake8")


def run_black():
    """Run Black code formatting."""
    os.system("black .")


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if "lint" in sys.argv:
        run_flake8()
        return
    elif "format" in sys.argv:
        run_black()
        return

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

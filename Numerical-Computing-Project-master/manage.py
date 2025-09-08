#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys



def main():
    """Run administrative tasks."""
    # Importar y configurar logging global
    try:
        from Apps.Common.utils import createLogFile
        createLogFile()
    except Exception as e:
        # Si falla el logging, imprime un error
        print(f"[WARNING] No se pudo inicializar el log global: {e}")

    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "NumericalComputingProject.settings"
    )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

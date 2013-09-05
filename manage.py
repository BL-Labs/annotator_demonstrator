#!/usr/bin/env python
import os
import sys

path = '/home/ben/djdan/djdan'
if path not in sys.path:
    sys.path.append(path)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djdan.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

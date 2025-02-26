import os
import shutil
import argparse

def create_project(project_name, app_name):
    # Create the project directory
    os.makedirs(project_name, exist_ok=True)

    # Copy project templates
    project_templates = os.path.join(os.path.dirname(__file__), 'templates', 'project')
    for item in os.listdir(project_templates):
        src = os.path.join(project_templates, item)
        dst = os.path.join(project_name, project_name, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    # Create the app directory
    app_dir = os.path.join(project_name, app_name)
    os.makedirs(app_dir, exist_ok=True)

    # Copy app templates
    app_templates = os.path.join(os.path.dirname(__file__), 'templates', 'app')
    for item in os.listdir(app_templates):
        src = os.path.join(app_templates, item)
        dst = os.path.join(app_dir, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    # Replace placeholders in files
    replace_placeholders(project_name, app_name, project_name)

    # Create manage.py
    manage_py_content = f'''#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{project_name}.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
'''
    with open(os.path.join(project_name, 'manage.py'), 'w') as f:
        f.write(manage_py_content)

    # Create requirements.txt
    requirements_content = """Django>=4.0
"""
    with open(os.path.join(project_name, 'requirements.txt'), 'w') as f:
        f.write(requirements_content)

    print(f"Project '{project_name}' with app '{app_name}' created successfully!")

def replace_placeholders(project_name, app_name, root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                content = f.read()
            content = content.replace('{{ project_name }}', project_name)
            content = content.replace('{{ app_name }}', app_name)
            with open(file_path, 'w') as f:
                f.write(content)

def main():
    parser = argparse.ArgumentParser(description="Create a Django project with a predefined structure.")
    parser.add_argument('project_name', help="Name of the Django project")
    parser.add_argument('app_name', help="Name of the Django app")
    args = parser.parse_args()

    create_project(args.project_name, args.app_name)

if __name__ == "__main__":
    main()
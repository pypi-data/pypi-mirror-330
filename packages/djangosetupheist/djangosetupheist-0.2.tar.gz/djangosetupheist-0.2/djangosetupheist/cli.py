import argparse
import os
import re
from djangosetupheist.methods import get_settings_folder
from djangosetupheist.utils import setup_project, startapp

def main():
    parser = argparse.ArgumentParser(description="Django Project Setup Tool")
    subparsers = parser.add_subparsers(dest="command")

    # `djs init project_name`
    init_parser = subparsers.add_parser("init", help="Initialize a new Django project")
    init_parser.add_argument("project_name", nargs="?", help="Django project name (optional)")
    
    # djs startapp app_name
    startapp_parser = subparsers.add_parser("startapp", help="Create a new Django app")
    startapp_parser.add_argument("app_name", help="Name of the app to create")

    args = parser.parse_args()

    if args.command == "init":
        project_name = args.project_name
        
        while not project_name:
            project_name = input("Enter the Django project name: ").strip()
            
            # Check for spaces
            if " " in project_name or not re.match(r"^[a-zA-Z0-9_-]+$", project_name):
                print("❌ Project name cannot contain spaces or special characters (only letters and numbers).")
                project_name = None
        
        folder = '.'

        setup_project(project_name, folder)

    elif args.command == "startapp":
        # check if there is a manage.py file in the current directory
        if not os.path.exists("manage.py"):
            print("❌ manage.py not found in this directory.")
            return
        
        settings_folder = get_settings_folder("manage.py")
        
        app_name = args.app_name or input("Enter Django app name: ").strip()

        if not app_name:
            print("❌ App name cannot be empty.")
            return

        # Check for spaces
        if (app_name[0] == "." or app_name[-1] == ".") or not re.match(r"^[a-zA-Z0-9_\-\.]+$", app_name):
            print("❌ App name cannot contain spaces or special characters (only letters, numbers, and .), and cannot start or end with a .")
            return
        
        startapp(args.app_name, settings_folder)
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

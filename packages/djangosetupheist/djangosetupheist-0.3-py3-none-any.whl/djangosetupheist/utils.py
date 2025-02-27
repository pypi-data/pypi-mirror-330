import os, random, string, re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def setup_project(project_name, folder):
    settings_app_path = os.path.join(folder, project_name) if folder else ''

    # Run `django-admin startproject`
    os.system(f"django-admin startproject {project_name} {folder}")

    # Set up `.env` file
    # get env
    env_sample_path = os.path.join(BASE_DIR, "assets/.envtemp")
    env_text = ''
    with open(env_sample_path, "r") as env_file:
        env_text = env_file.read()
    # create .envtemp
    env_temp_path = os.path.join(settings_app_path, ".envtemp")
    with open(env_temp_path, "w") as env_file:
        env_file.write(env_text)
    # create .env
    env_path = os.path.join(settings_app_path, ".env")
    env_text = env_text.replace('SECRET_KEY=', f'SECRET_KEY={generate_secret_key()}')
    with open(env_path, "w") as env_file:
        env_file.write(env_text)

    # Modify `settings.py` for `.env` support
    
    # 1. Get settings sample
    settings_sample_path = os.path.join(BASE_DIR, "assets/settings.py")
    with open(settings_sample_path, "r") as settings_file:
        settings_text = settings_file.read()

    # 2. Update settings
    settings_text = settings_text.replace("project_name", project_name)
    
    # 3. Write to `settings.py`
    settings_path = os.path.join(settings_app_path, "settings.py")
    with open(settings_path, "w") as settings_file:
        settings_file.write(settings_text)
        
    # Setup urls.py
    urls_sample_path = os.path.join(BASE_DIR, "assets/urls.py")
    with open(urls_sample_path, "r") as urls_file:
        urls_text = urls_file.read()
    
    urls_path = os.path.join(settings_app_path, "urls.py")
    with open(urls_path, "w") as urls_file:
        urls_file.write(urls_text)

    # Create static, media and templates directories
    os.makedirs(os.path.join(settings_app_path, "assets/static"), exist_ok=True)
    os.makedirs(os.path.join(settings_app_path, "assets/media"), exist_ok=True)
    os.makedirs(os.path.join(settings_app_path, "templates"), exist_ok=True)

    # Get appsConfig sample
    apps_config_sample_path = os.path.join(BASE_DIR, "assets/appsConfig.py")
    with open(apps_config_sample_path, "r") as apps_config_file:
        apps_config_text = apps_config_file.read()

    # Create `appsConfig.py`
    apps_config_path = os.path.join(settings_app_path, "appsConfig.py")
    with open(apps_config_path, "w") as apps_config_file:
        apps_config_file.write(apps_config_text)
        

    print(f"✅ Django project '{project_name}' initialized successfully.")


def startapp(full_app_name, settings_folder):
    is_multi_dirs = "." in full_app_name
    
    if is_multi_dirs:
        *folders, simple_app_name = full_app_name.split(".")
        app_folder = os.path.join(*folders, simple_app_name)
    else:
        simple_app_name = full_app_name
        app_folder = os.path.join(full_app_name)
    
    print(f"creating app in '{app_folder}'")
    
    # create the app folder
    os.makedirs(app_folder, exist_ok=True)

    # create the app in the folder
    success_status = os.system(f"django-admin startapp {simple_app_name} {app_folder}")

    if success_status != 0:
        print(f"Failed to create app {simple_app_name} in {app_folder}")
        return
    
    # create templates directory in app
    os.makedirs(os.path.join(app_folder, f"templates/{simple_app_name}/"), exist_ok=True)
    
    # get urls.py sample
    urls_sample_path = os.path.join(BASE_DIR, "assets/app_urls.py")
    with open(urls_sample_path, "r") as urls_file:
        urls_text = urls_file.read()

    # update urls.py
    urls_path = os.path.join(app_folder, "urls.py")
    with open(urls_path, "w") as urls_file:
        urls_text = urls_text.replace("app_name_replace", simple_app_name)
        urls_file.write(urls_text)
    
    # update appsConfig.py
    apps_config_path = os.path.join(settings_folder, "appsConfig.py")
    app_entry = "{ 'app_name': '" + full_app_name + "', 'url': '" + full_app_name.replace('.', '/') + "/', 'namespace': '" + simple_app_name + "' },"
    
    apps_config_text = ""
    
    # find the app_configs = [...] in appsConfig.py
    with open(apps_config_path, "r") as apps_config_file:
        apps_config_text = apps_config_file.read()

    replace_text = f"app_configs = [\n\t{app_entry}\n"
    
    apps_config_text = apps_config_text.replace("app_configs = [", replace_text)
    with open(apps_config_path, "w") as apps_config_file:
        apps_config_file.write(apps_config_text)
    


def generate_secret_key(length=32):
    characters = string.ascii_letters + string.digits + string.punctuation
    secret_key = "".join(random.choice(characters) for _ in range(length))
    return secret_key

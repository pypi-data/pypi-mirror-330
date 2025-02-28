import os, sys, subprocess, shutil
# Docker deploy
# We are going to use the dist version (obfuscated for production)

# 1. We must integrate again the removed files and folders (docker folder)
# 2. Build Docker container

def copy_docker_resources(version):
    '''
    Copy docker resources to the docker dist version
    '''
    current_path = os.path.dirname(__file__)
    source_root_path = os.path.join(current_path, 'spartaqube')
    dest_root_path = f"{os.getenv('BMY_PATH_PROJECT')}\\spartaqube_dist\\spartaqube_{version}\\spartaqube\\web\\spartaqube"
    # Copy docker-compose
    shutil.copy(os.path.join(source_root_path, 'docker-compose.yml'), os.path.join(dest_root_path, 'docker-compose.yml'))
    # Copy docker folder
    shutil.copytree(os.path.join(source_root_path, 'docker'), os.path.join(dest_root_path, 'docker'))
    
def build_docker_container():
    '''
    Build docker container
    '''
    # docker-compose up --build &


    pass
import os
from functools import partial
from fabric.contrib.files import append, sed, exists
from fabric.api import run, env, local, cd, sudo, put


media_directories = "media/{images}"
git_source = "https://github.com/sohail288/sheetswap.git"
BASE_DIR = '/home/{user}/sites'.format(**env)
HOME_DIR = '/home/{user}'.format(**env)
SITE_FOLDER = '{}/{}'.format(BASE_DIR, env.host)
VIRTUALENV_FOLDER = 'virtenv'

env.key_filename = '/Users/Sohail/Downloads/sheetswap.pem'

DEPENDENCIES = [
    'git',
    'postgresql postgresql-client postgresql-contrib postgresql-9.3 postgresql-common',
    'python-dev python3-dev',
    'libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev',
    'rabbitmq-server',
    'python-pip',
    'nginx',
    'supervisor'
]

PYTHON_DEPENDENCIES = [
    'virtualenv'
]

def _setup_ec2_server():
    pass

def _configure_globals():
    global BASE_DIR, HOME_DIR, SITE_FOLDER
    BASE_DIR = '/home/{user}/sites'.format(**env)
    HOME_DIR = '/home/{user}'.format(**env)
    SITE_FOLDER = '{}/{}'.format(BASE_DIR, env.host)

def _create_base_directory():
    if not exists(BASE_DIR):
        with cd(HOME_DIR):
            run("mkdir sites")

def _create_extra_directories(site_folder, extra_directories=[]):
    with cd(BASE_DIR):
        for folder in [media_directories].extend(extra_directories):
            run("mkdir -p {}/{}".format(site_folder, folder))


def _get_source():
    with cd(SITE_FOLDER):
        run('git clone {} .'.format(git_source))


def _install_dependencies():
        sudo('apt-get update')
        for dependency in DEPENDENCIES:
            sudo('apt-get -y install {}'.format(dependency))
        for dependency in PYTHON_DEPENDENCIES:
            sudo('pip install {}'.format(dependency))

def _copy_over_env_files():
    put('.env_production', SITE_FOLDER)

def _activate_env_files():
    run("source {}/{}".format(SITE_FOLDER, '.env_production'))

def _create_or_update_virtualenv():
    with cd(SITE_FOLDER):
        if not exists("./{}".format(virtualenv_folder)):
            run('virtualenv --no-site-packages -p python3 {}'.format(virtualenv_folder))
        # get the requirements
        run('{}/bin/pip install -r requirements/production.txt')


def _initialize_postgresql():
    sudo('mkdir -p /usr/local/pgsql/data')
    sudo('/usr/lib/postgresql/9.3/bin/initdb -D /usr/local/pgsql/data')
    sudo('chown postgres.postgres /usr/local/pgsql/data')
    sudo('chmod 750 /usr/local/pgsql/data')
    sudo('createdb sheetswap', user='postgres')

def _initialize_app():
    """ Does preliminary app steps.
    :return: None
    """
    with cd(SITE_FOLDER):
        run("./{}/bin/python run.py create_db".format(VIRTUALENV_FOLDER))


def _update_conf_scripts():
    virtualenv_directory = os.path.join(SITE_FOLDER, VIRTUALENV_FOLDER)
    static_directory = os.path.join(SITE_FOLDER, 'static')
    sed_global_nb = partial(sed, backup="", flags="g")
    with cd(SITE_FOLDER):
        for script in os.listdir('scripts'):
            # change all references to certain variables
            file = os.path.join(SITE_FOLDER, "scripts/{}".format(script))
            sed_global_nb(file, 'ROOT_DIRECTORY', SITE_FOLDER)
            sed_global_nb(file, 'VIRTUALENV_DIRECTORY', virtualenv_directory)
            sed_global_nb(file, 'HOST_NAME', env.host)
            sed_global_nb(file, 'USER', env.user)
            sed_global_nb(file, 'STATIC_DIRECTORY', static_directory)


def _setup_nginx_server():
    sudo('rm -f /etc/nginx/sites-enabled/default.conf')

    with cd(SITE_FOLDER):
        sudo('cp scripts/sheetswap_nginx.conf /etc/nginx/sites-available/{}.conf'.format(
            env.host
        ))

    sudo('ln /etc/nginx/sites-available/{}.conf /etc/nginx/sites-enabled/'.format(
        env.host
    ))
    sudo('service nginx restart')

def _setup_supervisor():
    with cd(SITE_FOLDER):
        sudo('cp scripts/sheetswap.conf etc/supervisor/conf.d/{}.conf'.format(
            env.host
        ))

    sudo('supervisorctl reread')
    sudo('supervisorctl update')
    sudo('supervisorctl start {}'.format(env.host))

def _activate_start_file():
    with cd(SITE_FOLDER):
        run('chmod 750 scripts/start.sh')


def deploy():
    _configure_globals()
    _create_base_directory()
    _install_dependencies()
    _get_source()
    _create_extra_directories(SITE_FOLDER)     # creates media folders
    _copy_over_env_files()
    _activate_env_files()
    _create_or_update_virtualenv()
    _initialize_app()
    _update_conf_scripts()
    _activate_start_file()
    _setup_nginx_server()
    _setup_supervisor()

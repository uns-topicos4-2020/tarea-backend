# -*- coding: utf-8 -*-
import getpass
from fabric import task, Connection, Config


# def sudo(func)
#     def sudo_wrapper(*args, **kwargs):

#         func(*args, **kwargs)

#     return sudo_wrapper

@task
def deploy(local):
    sudo_pass = getpass.getpass("[sudo] password: ")
    config = Config(overrides={'sudo': {'password': sudo_pass}})

    remote = Connection("abig", config=config)
    remote.run("cd /home/rc/webapps/topicos4 && git pull")
    remote.run("cd /home/rc/webapps/topicos4 && source /home/rc/.virtualenvs/topicos4/bin/activate && pip install -r requirements.txt")
    remote.sudo("sudo supervisorctl restart topicos4")

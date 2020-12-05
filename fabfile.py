# -*- coding: utf-8 -*-
import getpass
from fabric import task, Connection, Config


# def sudo(func)
#     def sudo_wrapper(*args, **kwargs):

#         func(*args, **kwargs)

#     return sudo_wrapper

@task
def deploy(local):
    sudo_pass = getpass.getpass("[sudo] password:")
    config = Config(overrides={'sudo': {'password': sudo_pass}})

    remote = Connection("abig", config=config)
    remote.run("cd /home/rc/webapps/topicos4")
    remote.run("git pull")
    remote.sudo("sudo supervisorctl restart topicos4")
#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers
"""

import os.path
from fabric.api import *
from fabric.operations import run, put

env.user = 'ubuntu'
env.hosts = ['xx.xx.xx.xx', 'xx.xx.xx.xx']


def do_pack():
    """Create a .tgz archive from the contents of the web_static folder"""
    try:
        if not os.path.exists("versions"):
            local("mkdir versions")
        created_at = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = "versions/web_static_{}.tgz".format(created_at)
        local("tar -cvzf {} web_static".format(file_path))
        return file_path
    except:
        return None


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        path_release = "/data/web_static/releases/{}/".format(no_ext)
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path_release))
        run("tar -xzf /tmp/{} -C {}".
            format(file_name, path_release))
        run("rm /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(path_release, path_release))
        run("rm -rf {}web_static".format(path_release))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".
            format(path_release))
        return True
    except:
        return False


def deploy():
    """Call the do_pack() function and store the path of the created archive.
    Call the do_deploy(archive_path) function, using the new path of the new archive"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)

#!/usr/bin/env python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder of your AirBnB Clone v2 repo, using the function do_pack.
"""

from fabric.api import *
import os
from datetime import datetime

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = os.getenv('USER')


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    local("mkdir -p versions")
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    file_path = "versions/web_static_{}.tgz".format(timestamp)
    local("tar -cvzf {} web_static".format(file_path))
    return file_path if os.path.exists(file_path) else None


def do_deploy(archive_path):
    """Distributes an archive to your web servers and deploys it"""
    if not os.path.exists(archive_path):
        return False

    archive_name = os.path.basename(archive_path)
    archive_name_no_ext = os.path.splitext(archive_name)[0]
    remote_path = "/tmp/{}".format(archive_name)
    put(archive_path, remote_path)

    releases_dir = "/data/web_static/releases"
    new_release_dir = "{}/{}".format(releases_dir, archive_name_no_ext)

    # Create the new release directory
    run("sudo mkdir -p {}".format(new_release_dir))

    # Extract the archive into the new release directory
    run("sudo tar -xzf {} -C {}"
        .format(remote_path, new_release_dir))

    # Remove the archive from the web server
    run("sudo rm {}".format(remote_path))

    # Move the contents of the new release directory to the web server root
    run("sudo mv {}/web_static/* {}/"
        .format(new_release_dir, new_release_dir))

    # Remove the now empty web_static directory
    run("sudo rm -rf {}/web_static".format(new_release_dir))

    # Update the symbolic link to point to the new release directory
    current_dir = "/data/web_static/current"
    run("sudo rm -rf {}".format(current_dir))
    run("sudo ln -s {} {}".format(new_release_dir, current_dir))

    return True


def deploy():
    """Creates and distributes an archive to your web servers and deploys it"""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)


def do_clean(number=0):
    """Deletes out-of-date archives"""
    if number == 0 or number == 1:
        number_to_keep = 1
    else:
        number_to_keep = int(number)

    with cd("/data/web_static/releases"):
        # Get a list of all the releases on the web servers
        releases = run("ls -1").split()

        # Sort the list of releases by version number, from newest to oldest
        sorted_releases = sorted(releases, reverse=True)

        # Remove all releases except the most recent number_to_keep releases
        for release in sorted_releases[number_to_keep:]:
            if release != "test":
                run("sudo rm -rf {}".format(release))

    with cd("/data/web_static"):
        # Get a list of all the archive files in the versions folder
        archives = run("ls -1 versions").split()

        # Sort the list of archives by date, from newest to oldest
        sorted_archives = sorted(

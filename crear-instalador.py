import os
import shutil
import stat

def setup_structure(target_dir):
    shutil.rmtree(target_dir, True)

    dir_applications = os.path.join(target_dir, "usr", "share", "applications", "")
    os.makedirs(dir_applications)

    shutil.copy2("installer/saludame.desktop", dir_applications)
    shutil.copytree("installer/bin/", target_dir + "/usr/bin")
    shutil.copytree("installer/DEBIAN", target_dir + "/DEBIAN")
    shutil.copytree("src", target_dir + "/usr/share/saludame")
    chmod_recurse(target_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH)


def chmod_recurse(base_path, mod):
    for subdir, dirs, files in os.walk(base_path):
        for entry in dirs:
            os.chmod(os.path.join(subdir, entry), mod)
        for entry in files:
            os.chmod(os.path.join(subdir, entry), mod)

target_dir = "dist"
setup_structure(target_dir)
os.system("dpkg -b %s saludame.deb" % (target_dir,))

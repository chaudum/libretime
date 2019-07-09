import os
import sys

from pathlib import Path
from setuptools import setup


def change_directory():
    """
    Change into script directory since setuptools uses relative paths.
    """
    script_path = Path(os.path.dirname(__file__)).resolve()
    os.chdir(script_path)
    print(script_path)


def get_data_files():
    """
    Return a list of data_files that should be installed in case setup.py is called
    with the following commands: ``install``, ``install_data``, or ``develop``.
    If the ``--no-install-script`` argument is provided, the function returns an
    empty list and drops the argument from ``sys.argv``.
    """
    is_installation = sys.argv[1] in ["install", "install_data", "develop"]
    install_init_scripts = "--no-init-script" not in sys.argv

    if is_installation and install_init_scripts:
        return [
            ("/etc/default", ["install/conf/airtime-celery"]),
            ("/etc/init.d", ["install/initd/airtime-celery"]),
        ]
    if not install_init_scripts:
        sys.argv.remove("--no-init-script")
    return []


def post_install():
    """
    Make /etc/init.d file executable and set proper permissions for the defaults
    config file.
    This function should only be called **after** ``setup()`` and only if
    ``data_files`` where provided.
    """
    os.chmod("/etc/init.d/airtime-celery", 0o755)
    os.chmod("/etc/default/airtime-celery", 0o640)
    print("---------------------")
    print("Run 'sudo service airtime-celery restart' now.")
    print("---------------------")


if __name__ == "__main__":
    change_directory()
    data_files = get_data_files()
    setup(
        name="airtime-celery",
        version="0.1",
        description="Libretime Celery service",
        url="http://github.com/Libretime/libretime",
        author="Sourcefabric",
        author_email="duncan.sommerville@sourcefabric.org",
        license="MIT",
        packages=["airtime-celery"],
        install_requires=[
            "soundcloud",
            "celery < 4",
            "kombu < 3.1",
            "configobj"
        ],
        data_files=data_files,
        zip_safe=False,
        classifiers=[
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: MIT",
            "Operating System :: POSIX",
            "Programming Language :: Python",
        ],
    )
    if data_files:
        post_install()

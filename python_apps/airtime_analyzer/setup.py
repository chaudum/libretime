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
    # Note: These files should be part of the LIbretime packaging,
    # not of this Python package!
    is_installation = sys.argv[1] in ["install", "install_data", "develop"]
    install_init_scripts = "--no-init-script" not in sys.argv

    if is_installation and install_init_scripts:
        return [
            ('/etc/init', ['install/upstart/airtime_analyzer.conf']),
            ('/etc/init.d', ['install/sysvinit/airtime_analyzer']),
        ]
    if not install_init_scripts:
        sys.argv.remove("--no-init-script")
    return []


def post_install():
    """
    Print instructions how to reload initclt configuration and restart airtime_analyzer
    daemon.
    This function should only be called **after** ``setup()`` and only if
    ``data_files`` where provided.
    """
    print("---------------------")
    print("Remember to reload the initctl configuration")
    print("Run \"sudo initctl reload-configuration; sudo service airtime_analyzer restart\" now.")
    print("Or on Ubuntu Xenial (16.04)")
    print("Remember to reload the systemd configuration")
    print("Run \"sudo systemctl daemon-reload; sudo service airtime_analyzer restart\" now.")
    print("---------------------")


if __name__ == "__main__":
    change_directory()
    data_files = get_data_files()
    setup(
        name='airtime_analyzer',
        version='0.1',
        description='Libretime Analyzer Worker and File Importer',
        url='http://github.com/sourcefabric/Airtime',
        author='Albert Santoni',
        author_email='albert.santoni@sourcefabric.org',
        license='MIT',
        packages=['airtime_analyzer'],
        scripts=['bin/airtime_analyzer'],
        install_requires=[
            'mutagen>=1.41.1',  # got rid of specific version requirement
            'pika',
            'daemon',
            'file-magic',
            'nose',
            'coverage',
            'mock',
            'python-daemon',
            'requests>=2.7.0',
            'rgain',
            # These next 3 are required for requests to support SSL with SNI. Learned this the hard way...
            # What sucks is that GCC is required to pip install these
            # 'ndg-httpsclient',
            # 'pyasn1',
            # 'pyopenssl'
        ],
        zip_safe=False,
        data_files=data_files,
    )
    if data_files:
        post_install()

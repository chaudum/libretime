#!/usr/bin/env python3

import os
import shutil
import sys

from functools import partial
from pathlib import Path

print_error = partial(print, file=sys.stderr)


def assert_superuser():
    if os.geteuid() != 0:
        print_error("Please run this as root.")
        sys.exit(1)


def install():
    """
    Copy ``airtime-icecast-status.xsl`` from local directory into
    ``/usr/share/icecast2/web`` directory. This operation requires superuser
    privileges.
    """

    assert_superuser()
    current_script_dir = Path(os.path.dirname(__file__))

    try:
        shutil.copy(
            current_script_dir.parent / "airtime-icecast-status.xsl",
            "/usr/share/icecast2/web",
        )
    except Exception as e:
        print_error("An error occured while installing icecast2: {}".format(e))
        sys.exit(1)


if __name__ == "__main__":
    install()

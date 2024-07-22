"""
This is the pyball module.
"""

import subprocess


def post_install():
    """
    Run the playwright install command.
    """
    subprocess.run(["playwright", "install"], check=True)

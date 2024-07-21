"""
This is the pyball module.
"""

import subprocess
from .playerid_lookup import *
from .utils import *
from .baseball_reference_player import *
from .baseball_reference_team import *
from .savant import *


def post_install():
    """
    Run the playwright install command.
    """
    subprocess.run(["playwright", "install"], check=True)

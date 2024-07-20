name = "pyball"
from .playerid_lookup import *
from .utils import *
from .baseball_reference_player import *
from .baseball_reference_team import *
from .savant import *

import subprocess

def post_install():
    subprocess.run(["playwright", "install"], check=True)
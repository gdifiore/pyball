name = "pyball"
from .playerid_lookup import *
from .utils import *
from .batting_stats import *
from .pitching_stats import *
from .team_batting_stats import *
from .team_pitching_stats import *
from .savant import *

import subprocess

def post_install():
    subprocess.run(["playwright", "install"], check=True)
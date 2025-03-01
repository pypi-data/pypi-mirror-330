from .crosscorr import *
from .airtovac import *
from .mask import *
from .utils import *

import sys
import site
import os

# Find the path to site-packages directory for the current environment
site_packages = site.getsitepackages()  # Returns a list of site-packages paths
crosscorr_path = None

# Search for the crosscorr directory in site-packages
for sp in site_packages:
    potential_path = os.path.join(sp, 'crosscorr')
    if os.path.exists(potential_path):
        crosscorr_path = potential_path
        break

# If found, add it to sys.path
if crosscorr_path:
    sys.path.append(crosscorr_path)

#
# imports
#

import os
import json
from pythonThemerHelpers.makeFileChanges import makeFileChanges
from pathlib import Path
import shutil, errno

#
# constants
#

automatedBuildSettings = 'builder-settings.json'

#
# helper functions
#

def getKeyFromBuildSettings(key):
    data = {}
    try:
        with open(automatedBuildSettings) as file:
            data = json.loads(file.read())
    except Exception as e:
        pass

    if key in data:
        return str(data[key])
    else:
        raise Exception('There is no "' + key + '" in builder-settings.json')


#
# 1. Determine whether we are building for iOS, Android, or both
#

platformsToBuildTo = getKeyFromBuildSettings('platformsToBuildTo') #['ios','android'] TODO

#
# 2. Clean the `build_arguments/` and `builds/` folder
#

#
# 3. Create build arguments for each build
#


















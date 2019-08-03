#
# imports
#

import os
import json
from jsmin import jsmin
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
        with open(automatedBuildSettings) as js_file:
            minified = jsmin(js_file.read())
            data = json.loads(minified)
    except Exception as e:
        print(e)
        pass

    if key in data:
        return data[key]
    else:
        raise Exception('There is no "' + key + '" in builder-settings.json')


#
# 1. Determine whether we are building for iOS, Android, or both
#

platformsToBuildTo = getKeyFromBuildSettings('platformsToBuildTo')
print(platformsToBuildTo)

#
# 2. Clean the `build_arguments/` and `builds/` folder
#

#
# 3. Create build arguments for each build
#


















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
# vars
#

dirname, filename = os.path.split(os.path.abspath(__file__))
buildFolder = dirname + "/" + getKeyFromBuildSettings("BuildFolder")

#
# startup
#
ios_appName = getKeyFromBuildSettings('ios_appName')
android_appName = getKeyFromBuildSettings('android_appName')

print("-----------------------------------------------")
print("----***************************************----")
print("\tWelcome to Automated Corona Builder ")
print("----***************************************----")
print("-----------------------------------------------\n")


#
# 1. Determine whether we are building for iOS, Android, or both
#

platformsToBuildTo = getKeyFromBuildSettings('platformsToBuildTo')

print(" Automated Corona Builder will build:")
if 'ios' in platformsToBuildTo:
    print(" - " + ios_appName+ " for iOS")
if 'android' in platformsToBuildTo:
    print(" - " + android_appName+ " for Android")
print("\n")

#
# 2. Clean the `build_arguments/` and `builds/` folder
#

if os.path.isdir('build_arguments'):
    shutil.rmtree('build_arguments')
os.mkdir('build_arguments')

if os.path.isdir('builds'):
    shutil.rmtree('builds')
os.mkdir('builds')

#
# 3. Create build arguments for each build
#
projectsToBuild = []
for index, platform in enumerate(platformsToBuildTo):
    projectsToBuild.append({
        'platform':       platform,
        'relProjectPath': getKeyFromBuildSettings("CoronaProjectToBuild"),
    })

print(projectsToBuild)














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
# Put the jobs into an array so we can loop through each job at each step together
#

projectsToBuild = []
for index, platform in enumerate(platformsToBuildTo):
    projectsToBuild.append({
        'platform':       platform,
        'appName':        getKeyFromBuildSettings(platform + "_appName"),
        'relProjectPath': getKeyFromBuildSettings("CoronaProjectToBuild"),
        'version':        str(getKeyFromBuildSettings("major")) + '.' + str(getKeyFromBuildSettings("minor"))
    })

#
# 3. Create build arguments for each build
#

for index, project in enumerate(projectsToBuild):
    data = "local params ="                                            + '\n'
    data += "{"                                                        + '\n\t'
    data += "-- general params"                                        + '\n\t'
    data += "platform = '"    + project["platform"]             + "'," + '\n\t'
    data += "appName = '"     + project["appName"]              + "'," + '\n\t'
    data += "appVersion = '"  + project["version"]              + "'," + '\n\t'
    data += "dstPath = '"     + dirname + "/builds"             + "'," + '\n\t'
    data += "projectPath = '" + dirname + "/" + project["relProjectPath"]  + "'," + '\n\t'

    data += "\n\t-- " + project["platform"] + " specific params" + '\n\t'
    if project["platform"] == "android":
        data += "androidAppPackage = '" + getKeyFromBuildSettings("android_appPackage")         + "'," + '\n\t'
        data += "androidVersionCode = '" + str(int(project["version"].replace(".", ""))) + str(getKeyFromBuildSettings("android_extraVersionCode")) + "'," + '\n\t'
        data += "certificatePath = '" + dirname + getKeyFromBuildSettings("android_keystorePath") + "'," + '\n\t'
        data += "keystorePassword = '" + getKeyFromBuildSettings("android_keystorePassword") + "'," + '\n\t'
        data += "keystoreAlias = '" + getKeyFromBuildSettings("android_keystoreAlias") + "'," + '\n\t'
        data += "keystoreAliasPassword = '" + getKeyFromBuildSettings("android_keystoreAliasPassword") + "'," + '\n'
    elif project["platform"] == "ios":
        # data += "platformVersion = '" + 'iOS11.4' + "'," + '\n\t'
        # data += "platformVersion = '" + 'iOS12.2' + "'," + '\n\t'
        data += "certificatePath = '" + dirname + getKeyFromBuildSettings("ios_provisionPath") + "'," + '\n'
    data += "}" + '\n'
    data += "return params"


    fileName = 'build_arguments/' + project["platform"] + '_' + str(project["version"].replace(".", "-")) + '.lua'
    file = open(fileName, 'w')
    file.write(data)
    file.close()














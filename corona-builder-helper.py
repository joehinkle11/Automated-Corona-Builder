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
# 2. Clean the `build_arguments/` and `builds/` folders
#

print("\n----------------------------")
print("Cleaning the `build_arguments/` and `builds/` folders")
print("----------------------------")
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
    absBuildPath = dirname + "/builds/" + getKeyFromBuildSettings(platform + "_appName")
    if platform == 'ios':
        absBuildPath += ".ipa"
    if platform == 'android':
        absBuildPath += ".apk"

    projectsToBuild.append({
        'platform':       platform,
        'appName':        getKeyFromBuildSettings(platform + "_appName"),
        'relProjectPath': getKeyFromBuildSettings("CoronaProjectToBuild"),
        'relBuildArgumentsPath': 'build_arguments/' + platform + '_' + str(str(getKeyFromBuildSettings("major")) + '.' + str(getKeyFromBuildSettings("minor")).replace(".", "-")) + '.lua',
        'absBuildPath':   absBuildPath,
        'version':        str(getKeyFromBuildSettings("major")) + '.' + str(getKeyFromBuildSettings("minor"))
    })

#
# 3. Create build arguments for each build
#

print("\n------------------------------------------")
print("Creating build arguments for CoronaBuilder")
print("------------------------------------------")
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
        data += "certificatePath = '" + dirname + "/" + getKeyFromBuildSettings("android_keystorePath") + "'," + '\n\t'
        data += "keystorePassword = '" + getKeyFromBuildSettings("android_keystorePassword") + "'," + '\n\t'
        data += "keystoreAlias = '" + getKeyFromBuildSettings("android_keystoreAlias") + "'," + '\n\t'
        data += "keystoreAliasPassword = '" + getKeyFromBuildSettings("android_keystoreAliasPassword") + "'," + '\n'
    elif project["platform"] == "ios":
        # data += "platformVersion = '" + 'iOS11.4' + "'," + '\n\t'
        # data += "platformVersion = '" + 'iOS12.2' + "'," + '\n\t'
        data += "certificatePath = '" + dirname + "/"  + getKeyFromBuildSettings("ios_provisionPath") + "'," + '\n'
    data += "}" + '\n'
    data += "return params"


    fileName = project["relBuildArgumentsPath"]
    file = open(fileName, 'w')
    file.write(data)
    file.close()


#
# 4. Run `CoronaBuilder` on the Corona project found in `src` for each build argument file found in `build_arguments/` and puts the output into `builds/`
#

print("\n----------------------------")
print("Building each Corona project")
print("----------------------------")
for index, project in enumerate(projectsToBuild):
    print(' ' + str(index+1) + " / " + str(len(projectsToBuild)))
    command = getKeyFromBuildSettings("CoronaBuilderPath") + "CoronaBuilder build --lua " + dirname + "/" + project['relBuildArgumentsPath']
    print('  relBuildArgumentsPath:\t'    + project['relBuildArgumentsPath'])
    print('  building...')
    print(command)
    os.system(command)
    print("  success!")

#
# 5. Run Fastlane's CLI to upload for each built app found in `builds` to either the App Store or Playstore
#

print("\n------------------------")
print("Uploading each built app")
print("------------------------")
for index, project in enumerate(projectsToBuild):
    print(' ' + str(index+1) + " / " + str(len(projectsToBuild)))
    absBuildPathEscapedSpaces = project['absBuildPath'].replace(' ','\\ ')
    release = getKeyFromBuildSettings(project['platform'] + "_pubLevel")
    packageName = getKeyFromBuildSettings(project['platform'] + "_appPackage")
    print('  project:\t'      + absBuildPathEscapedSpaces)
    print('  packageName:\t'  + packageName )
    print('  release:\t'      + release )
    print('  platform:\t'      + project['platform'])

    if project['platform'] == 'android':
        rolloutPercentage = "1.0"

        command =  'fastlane supply '
        command += '-p ' + packageName                                 + ' '
        command += '-a ' + release                                     + ' '
        command += '-r ' + rolloutPercentage                                      + ' '
        command += '-j ' + dirname + getKeyFromBuildSettings("android_playstoreServiceApiJsonPath")   + ' '
        command += '-b ' + absBuildPathEscapedSpaces                              + ' '
        command += '--skip_upload_metadata true'                                  + ' '
        command += '--skip_upload_images true'                                    + ' '
        command += '--skip_upload_screenshots true'                               + ' '
        command += '--track_promote_to ' + release                     + ' '
        # command += '--validate_only true'                                         + ' '
        # command += '--verbose'

        print('  command:\t'      + command)
        # if not debug:
        #     os.system(command)
    if project['platform'] == 'ios':
        command =  'fastlane run testflight '
        command += 'username:"' + getKeyFromBuildSettings("ios_testflightUsername") + '"'                             + ' '
        command += 'app_identifier:"' + packageName + '"'              + ' '
        command += 'app_platform:"ios"'                                           + ' '
        command += 'apple_id:"' + getKeyFromBuildSettings('ios_appleAppId') + '"'                     + ' '
        command += 'ipa:"' + project['absBuildPath'] + '"'                        + ' '
        # beta_app_review_info
        # localized_app_info
        # beta_app_description
        # beta_app_feedback_email
        # localized_build_info
        # changelog
        command += 'skip_submission:"false"'                                      + ' '
        command += 'distribute_external:"false"'                                  + ' '
        command += 'notify_external_testers:"true"'                               + ' '
        command += '--verbose'

        print('  command:\t'      + command)
        # if not debug:
            # os.system(command)










# imports
import os
import json
from pythonThemerHelpers.makeFileChanges import makeFileChanges
from pathlib import Path
import shutil, errno

# constants
coronaBuilderPath = '/Applications/CoronaSDK/Native/Corona/mac/bin/CoronaBuilder.app/Contents/MacOS/'
themeVersioningPath = 'builder-settings.json'
releaseLevelPriority = ["production","beta","alpha","internal"] #TODO
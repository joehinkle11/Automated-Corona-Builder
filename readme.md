Fyi, I'm still putting this together.

# <img src="https://coronalabs.com/wordpress/wp-content/uploads/2014/12/Flat-Corona-300x300-75x75.png" width="30"> Welcome to the Automated Corona Builder <img src="https://coronalabs.com/wordpress/wp-content/uploads/2014/12/Flat-Corona-300x300-75x75.png" width="30">

## Project Overview

Automated Corona Builder combines the following technologies in one simple CLI
* [Corona SDK](https://coronalabs.com/product/)'s `CoronaBuilder`
* [Fastlane](https://fastlane.tools/)'s CLI for app deployment

The result is that you are able to compile and publish your Corona SDK project for production in one command.

The Automated Corona Builder codebase is broken down into the following components...

### Git-Tracked Components

| Component (tracked) | Location |
| ------------------- | -------- |
| Python script which coordinates the whole build process | `builder.py` |
| Controls for which themes publish to which deployment level (i.e. prod, beta) and with which version code | `builder-settings.json` |
| Not sure why I'm documenting this obvious piece | `.gitignore` |
| Private keys used for signing apps | `private_keys/` |
| Root folder of your Corona SDK project | `src/` |
| zlib/libpng license | `LICENSE.md` |
| This file lol | `README.md` |

### Non-Git-Tracked Components

Many of these are autogenerated by the Automated Corona Builder CLI.

| Component (untracked) | Location | Generated by |
| --------------------- | -------- | ------------ |
| Production build arguments given to Corona's `CoronaBuilder` | `build_arguments/` | `builder.py` |
| Production Corona builds to be uploaded to app stores | `builds/` | `builder.py` |

## Setup
1. Install Click for the CLI by running `sudo pip install click` and `sudo pip install watchdog` and `sudo pip install pillow` and `python3 -m pip install Pillow`
2. Or run `python3 -m pip install click` and `python3 -m pip install watchdog`
3. Install Xcode command line tools by running `xcode-select --install`.

## Using Automated Corona Builder
### Commands
* `python3 builder.py`

### Overview of the steps `builder.py` runs
1. Determines whether it's building for iOS, Android, or both
2. Cleans (removes contents of) the `build_arguments/` and `builds/` folder
3. Creates build arguments as a Lua file for iOS, Android or both in `build_arguments/` based on what is written in `builder-settings.json`
4. Runs `CoronaBuilder` on the Corona project found in `src` for each build argument file found in `build_arguments/` and puts the output into `builds/`
5. Runs Fastlane's CLI to upload for each built app found in `builds` to either the App Store or Playstore

## TODO
### CLI
* finished the `builder.py` script. (I have one finished, but I'm just cleaning it up and slowly migrating it into this new git project)
* add setup documentation
* add setup documentation for the iOS-SDKs.json file you need to change in Corona (or something like that?)
* maybe think of a less confusing name? `CoronaBuilder` is a CLI Corona made, but mine is called Automated-Corona-Builder. And my python script is called `builder.py`...kind of confusing.
* create video demonstrating how to setup and run this thing
* somehow get the builder.py to line up with your project's git...
* support continuous deployment


# License

This project is released zlib/libpng license, see the [LICENSE.md](LICENSE.md) file.

# Shameless plugs

* <img src="https://cdnjs.cloudflare.com/ajax/libs/webicons/2.0.0/webicons/webicon-youtube-s.png" width="15"> [My YouTube channel](https://www.youtube.com/channel/UCje9o1NPdBs0vhPp7AEgWvg)
* <img src="https://cdnjs.cloudflare.com/ajax/libs/webicons/2.0.0/webicons/webicon-youtube-s.png" width="15"> [My second YouTube channel](https://www.youtube.com/channel/UC5aSLB42ZZIDtQXrZgnS1iA)
* <img src="https://www.joehinkle.io/favicon.png" width="15"> [My Website](https://www.joehinkle.io/)
* <img src="https://cdnjs.cloudflare.com/ajax/libs/webicons/2.0.0/webicons/webicon-twitter-s.png" width="15"> [My Twitter](https://twitter.com/joehink95)
* <img src="https://cdnjs.cloudflare.com/ajax/libs/webicons/2.0.0/webicons/webicon-android-s.png" width="15"> [My Android Apps](https://play.google.com/store/apps/dev?id=6380399300644608862)
* <img src="https://cdnjs.cloudflare.com/ajax/libs/webicons/2.0.0/webicons/webicon-apple-s.png" width="15"> [My iOS Apps](https://apps.apple.com/us/developer/joseph-hinkle/id916334630)


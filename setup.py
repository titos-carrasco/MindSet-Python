# {dist}-{version}(-{build})?-{python}-{abi}-{platform}.whl

from setuptools import setup
import sys

SETUP = {
    "name"             : "rcr-mindset",
    "version"          : "4.0.1",
    "description"      : "Libreria para utilizar los módulos EEG MindSet/MindWave/MindLink",
    "license"          : "MIT",
    "author"           : "Roberto Carrasco",
    "author_email"     : "titos.carrasco@gmail.com",
    "maintainer"       : "Roberto Carrasco",
    "maintainer_email" : "titos.carrasco@gmail.com",
    "packages"         : [ "mindset" ],
    "package_dir"      : { "mindset": "mindset/" },
}

setup( **SETUP )

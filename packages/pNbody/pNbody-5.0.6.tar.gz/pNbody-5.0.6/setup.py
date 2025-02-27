'''
 @package   pNbody
 @file      setup.py
 @brief     Install pNbody
 @copyright GPLv3
 @author    Yves Revaz <yves.revaz@epfl.ch>
 @section   COPYRIGHT  Copyright (C) 2017 EPFL (Ecole Polytechnique Federale de Lausanne)  LASTRO - Laboratory of Astrophysics of EPFL

 This file is part of pNbody.
'''

import os
import sys
from setuptools import setup, find_packages, Extension
from glob import glob
from copy import deepcopy
import versioneer
import numpy as np


# get and save the current git version
#versioneer.get_version("pNbody")


# optional modules
options = {
    "ptreelib": False,
    "cooling_with_metals": True,
    "pygsl": True,
}

# special flags for modules
spec_flags = {
    # "logger_loader": ["-Wall", "-Wextra", "-DSWIFT_DEBUG_CHECKS"]
}

# default flags
flags = ["-Werror=strict-prototypes", "-Wno-unused-parameter"]

# directory containing headers
include_dirs = [
    ".",
    "/usr/include",     # gsl
    "/usr/local/include",     # macOS (homebrew) headers
    np.get_include(),
]

# special includes (not used)
spec_inc = {
    "ptreelib": ["$MPICH_ROOT/include",
                 "src/ptreelib"],

}

# libraries
libraries = ["m"]

# special libraries
spec_lib = {
    "ptreelib": ["mpich"],
    "cooling_with_metals": ["gsl", "gslcblas"],
    "pygsl": ["gsl"]
}

# special libraries directory
spec_lib_dir = {
    "ptreelib": ["$MPICH_ROOT/lib"]
}

# C modules
modules_name = [
    "nbodymodule",
    "myNumeric",
    "mapping",
    "kernels",
    "montecarlolib",
    "iclib",
    "treelib",
    "nbdrklib",
    "peanolib",
    "coolinglib",
    "cosmolib",
    "asciilib",
    "tessel",
    "pychem",
    # "libtipsy",    crash which fedora 23: needs CFLAGS="-I/usr/include/tirpc" CXXFLAGS="-I/usr/include/tirpc"
    "thermodynlib",
    "orbitslib"
]

# data files
'''
data_files = []

data_files.append(('config', glob('./config/*parameters')))
data_files.append(('config/rgb_tables', glob('./config/rgb_tables/*')))
# # trick to avoid rpm problems
data_files.append(('config/formats', glob('./config/formats/*.py')))
data_files.append(('config/extensions', glob('./config/extensions/*.py')))

data_files.append(('plugins', glob('./config/*.py')))
data_files.append(('plugins', glob('./config/plugins/*.py')))
data_files.append(('config/opt/SSP', glob('./config/opt/SSP/*[txt,dat]')))
data_files.append(('config/opt/SSP/P94_salpeter',
                   glob('./config/opt/SSP/P94_salpeter/*')))
data_files.append(('fonts', glob('./fonts/*')))

# examples
data_files.append(('examples', glob('./examples/*.dat')))
data_files.append(('examples', glob('./examples/*.py')))
data_files.append(('examples/scripts', glob('./examples/scripts/*.py')))

# examples ic
data_files.append(('examples/ic', glob('./examples/ic/*.py')))
data_files.append(('examples/ic', glob('./examples/ic/Readme')))
'''


package_files = glob('./examples/snapshots/*')
package_files += glob('./config/*parameters')
package_files += glob('./config/rgb_tables/*')
package_files += glob('./config/formats/*.py')
package_files += glob('./config/extensions/*.py')
package_files += glob('./config/opt/*')
package_files += glob('./config/opt/SSP/*')
package_files += glob('./plugins/*.py')
package_files += glob('./fonts/*')
package_files += glob('./config/opt/filters/*')


# DO NOT TOUCH BELOW

# add options
for k in options.keys():
    if options[k]:
        modules_name.append(k)


# Generate extensions
ext_modules = []

for k in modules_name:
    # get flags
    extra_flags = deepcopy(flags)
    if k in spec_flags:
        extra_flags.extend(spec_flags[k])
    # get libraries
    extra_lib = deepcopy(libraries)
    if k in spec_lib:
        extra_lib.extend(spec_lib[k])
    # get library directories
    extra_lib_dirs = []
    if k in spec_lib_dir:
        extra_lib_dirs.extend(spec_lib_dir[k])

    # compile extension
    tmp = Extension("pNbody." + k,
                    glob("src/" + k + "/*.c"),
                    include_dirs=include_dirs,
                    libraries=extra_lib,
                    extra_compile_args=extra_flags,
                    library_dirs=extra_lib_dirs)

    ext_modules.append(tmp)


# add new C extension, but a cleaner way
ext = Extension("pNbody.rtlib",
                glob("src/rtlib/*.c"),
                include_dirs=include_dirs+["src/rtlib/include"],
                libraries=extra_lib,
                extra_compile_args=extra_flags,
                library_dirs=extra_lib_dirs)

ext_modules.append(ext)


# scripts to install
scripts = glob("scripts/pNbody/*")
scripts += glob("scripts/mockimgs/*")
scripts += glob("scripts/imf/*")
scripts += glob("scripts/isochrones/*")
scripts += glob("scripts/ic/*")
scripts += glob("scripts/plot/*")
scripts += glob("scripts/orbits/*")
scripts += glob("scripts/rt/*")
scripts += glob("scripts/il/*")
scripts += glob("scripts/sw/*")
scripts += glob("scripts/ssp/*")
scripts += glob("scripts/sed/*")
scripts += glob("scripts/pnbmov/*")
scripts += glob("scripts/snapshots/*")

setup(
    name="pNbody",
    author="Yves Revaz",
    author_email="yves.revaz@epfl.ch",
    url="http://obswww.unige.ch/~revaz/pNbody/index.html",
    description="""
    This module provides lots of tools used
    to deal with Nbody particles models.
    """,
    long_description_content_type="text/x-rst",
    license="GPLv3",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    scripts=scripts,
    ext_modules=ext_modules,
    # data_files=data_files,
    package_data={'pNbody': package_files},
    #install_requires=["scipy", "h5py","astropy", "pillow", "tqdm", "versioneer", "ipython","numpy<2.0"],
    install_requires=["numpy<2.0","scipy","h5py","tqdm","astropy","pillow","ipython","matplotlib"],
)

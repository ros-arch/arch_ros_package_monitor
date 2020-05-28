#!/usr/bin/env python

# Copyright © 2020 Felix Exner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.
# 3. Neither the name of the organization nor the
# names of its contributors may be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY Felix Exner ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Felix Exner BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import sys

import catkin_pkg

import helpers.aur as aur
from helpers.rosdistro_adapter import RosdistroAdapter

def main():
    # pkg_name = sys.argv[1]

    distro_name = "melodic"

    rosdistro = RosdistroAdapter(distro_name)
    package_distribution_list = rosdistro.get_package_list()

    for pkg_name in package_distribution_list:
        print("---\nChecking %s" % pkg_name)
        try:
            pkg_info = rosdistro.get_package_by_name(pkg_name)
            aur_pkg_name = "ros-%s-%s" % (distro_name, pkg_name.replace('_', '-'))
            aur_pkg = aur.get_package_info(aur_pkg_name)

            print("  Upstream version: %s" % pkg_info.version)
            aur_version = "None"
            if aur_pkg['results']:
                aur_version = aur_pkg['results']['Version']
            print("  AUR version:      %s" % aur_version)
        except TypeError as e:
            print("Parsing error: %s" % e)
        except catkin_pkg.package.InvalidPackage as err:
            print("Invalid package: %s" % err)



if __name__ == "__main__":
    main()

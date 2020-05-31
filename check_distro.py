#!/usr/bin/env python3

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

import argparse
import sys

import catkin_pkg

from helpers.aur import AURAdapter
from helpers.github import GHAdapter
from helpers.rosdistro_adapter import RosdistroAdapter
from helpers.package import Package


def main():
    parser = argparse.ArgumentParser(
        description='A small package to get an overview of Archlinux ROS packages')
    parser.add_argument('--distro_name', type=str, help='The ROS distribution that should be used',
                        default='noetic')
    parser.add_argument('--hide_outdated', dest='show_outdated', action='store_false',
                        help='Hide packages that are outdated in AUR')
    parser.add_argument('--hide_outofsync', dest='show_outofsync', action='store_false',
                        help="Hide packages where the github version doesn't match the AUR version")
    parser.add_argument('--show_installed_only', dest='show_installed', action='store_true',
                        help='Show only outdated packages that are installed.')
    # parser.add_argument('--show_missing', type=bool, help='Show packages that are missing in AUR',
    # default=True)
    parser.set_defaults(show_outdated=True)
    parser.set_defaults(show_outofsync=True)
    parser.set_defaults(show_installed=False)

    args = parser.parse_args()

    print('Checking distro "%s". this might take a while...' % args.distro_name)

    rosdistro = RosdistroAdapter(args.distro_name)
    package_distribution_list = rosdistro.get_package_list()

    aur_adapter = AURAdapter(args.distro_name)
    gh_adapter = GHAdapter(args.distro_name)

    outdated_pkgs = list()
    outofsync_pkgs = list()
    missing_pkgs = list()
    error_pkgs = list()

    for pkg_name in package_distribution_list:
        # if pkg_name == 'capabilities':
        # # DEBUG stop
        # break
        # print("---\nChecking %s" % pkg_name)
        pkg = Package(pkg_name)
        try:
            pkg_info = rosdistro.get_package_by_name(pkg_name)
            pkg.add_rosdistro_information(pkg_info)
            aur_pkg_name = "ros-%s-%s" % (args.distro_name, pkg_name.replace('_', '-'))
            aur_pkg = aur_adapter.get_package_info(aur_pkg_name)

            # print('Upstream version: %s' % pkg_info.version)

            if aur_pkg:
                pkg.add_aur_information(aur_pkg)
                # print('AUR version: %s' % aur_pkg['Version'])

            gh_pkg = gh_adapter.get_package_info(aur_pkg_name)
            if gh_pkg:
                pkg.add_gh_information(gh_pkg)

            if pkg.get_status() == 'outdated':
                outdated_pkgs.append(pkg)
            if pkg.get_status() == 'outofsync':
                outofsync_pkgs.append(pkg)
            elif pkg.get_status() == 'missing':
                missing_pkgs.append(pkg)

        except TypeError as err:
            error_pkgs.append(pkg)
            print("Parsing error: %s\n%s" % (pkg_name, err), file=sys.stderr)
        except catkin_pkg.package.InvalidPackage as err:
            error_pkgs.append(pkg)
            print("Invalid package: %s\n%s" % (pkg_name, err), file=sys.stderr)

    if args.show_outdated:
        print("\nOutdated packages:")
        for pkg in outdated_pkgs:
            if args.show_installed and not pkg.is_installed():
                # skip this package
                continue
            print(pkg)
    if args.show_outofsync:
        print("\nOut of sync packages:")
        for pkg in outofsync_pkgs:
            if args.show_installed and not pkg.is_installed():
                # skip this package
                continue
            print(pkg)


if __name__ == "__main__":
    main()

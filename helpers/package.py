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

import re
import subprocess
import sys


class VersionParsingException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Version():
    """Version representation"""

    def __init__(self, version_string):
        self.major = 0
        self.minor = 0
        self.bugfix = 0
        self.parse(version_string)

    def parse(self, version_string):
        regex = re.compile(r'(?P<major>\d+)\.(?P<minor>\d+)\.(?P<bugfix>\d+)')
        match = re.match(regex, version_string)
        if match:
            self.major = int(match.group('major'))
            self.minor = int(match.group('minor'))
            self.bugfix = int(match.group('bugfix'))
        else:
            raise VersionParsingException('Could not parse version %s' % (version_string))

    def __eq__(self, other):
        return self.major == other.major \
            and self.minor == other.minor \
            and self.bugfix == other.bugfix

    def __gt__(self, other):
        if self.major == other.major:
            if self.minor == other.minor:
                return self.bugfix > other.bugfix
            else:
                return self.minor > other.minor
        else:
            return self.major > other.major

    def __lt__(self, other):
        if self.major == other.major:
            if self.minor == other.minor:
                return self.bugfix < other.bugfix
            else:
                return self.minor < other.minor
        else:
            return self.major < other.major

    def __ge__(self, other):
        return self == other or self > other

    def __le__(self, other):
        return self == other or self < other

    def __str__(self):
        return '%i.%i.%i' % (self.major, self.minor, self.bugfix)


class Package():
    """Package representation that contains information from multiple sources such as AUR and
    rosdistro"""

    def __init__(self, pkg_name):
        self.package_name = pkg_name

        self._rosdistro_version = None
        self._aur_version = None
        self._aur_maintainer = None
        self._gh_version = None
        self._installed = False
        self._installed_version = None

    def add_aur_information(self, aur_pkg):
        """Add information received from AUR to this package. This has to be a valid dictionary
        build from the AURweb json response."""
        try:
            self._aur_version = Version(aur_pkg['Version'])
        except VersionParsingException as err:
            print("Error parsing AUR version of package %s: %s" % (self.package_name, err.message),
                  file=sys.stderr)
        self._aur_maintainer = aur_pkg['Maintainer']
        self.update_installed_status(aur_pkg['Name'])

    def add_rosdistro_information(self, pkg_info):
        """Add information from a parsed package manifest"""
        try:
            self._rosdistro_version = Version(pkg_info.version)
        except VersionParsingException as err:
            print("Error parsing rosdistro version of package %s: %s" % (self.package_name, err.message),
                  file=sys.stderr)

    def add_gh_information(self, pkg_info):
        """Add information from a parsed PKGBUILD from the GH repository"""
        try:
            self._gh_version = Version(pkg_info['version'])
        except VersionParsingException as err:
            print("Error parsing github version of package %s: %s" % (self.package_name, err.message),
                  file=sys.stderr)

    def is_outdated(self):
        """Returns information whether this package is outdated inside AUR. If it doesn't have a
        corresponding AUR package, False is returned."""
        if self._aur_version:
            return self._rosdistro_version > self._aur_version
        return False

    def is_ahead(self):
        if self._aur_version:
            return self._rosdistro_version < self._aur_version
        return False

    def is_outofsync(self):
        """Returns information whether the AUR version differs from the on on Github. If either the
        AUR version or the Github version is missing, False is returned."""
        if self._aur_version and self._gh_version:
            if self._gh_version != self._aur_version:
                return True
        return False

    def is_missing(self):
        """Returns True if no corresponding AUR package could be found."""
        if self._aur_version:
            return False
        return True

    def is_installed(self):
        return self._installed

    def update_installed_status(self, pkg_name):
        """Checks whether the package is installed locally"""
        cmd = ["pacman", "--noconfirm", "-Q", pkg_name]
        process = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = process.communicate()

        if process.returncode == 0:
            self._installed = True
            version_str = output[0].decode('utf-8').split()[1]
            try:
                self._installed_version = Version(version_str)
            except VersionParsingException as err:
                print("Error parsing rosdistro version of package %s: %s" % (self.package_name, err.message),
                      file=sys.stderr)

    def __str__(self):
        output = '%s:' % self.package_name
        output += '\n - rosdistro: %s' % self._rosdistro_version
        if self._aur_version:
            output += '\n - AUR:       %s (Maintainer: %s)' %(
                    self._aur_version,
                    self._aur_maintainer)
        if self._gh_version:
            output += '\n - Github:    %s' % self._gh_version
        output += '\nInstalled:    %s' % self._installed_version
        return output

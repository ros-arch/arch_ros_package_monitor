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
            # TODO: Throw
            print('Could not parse version')

    def __eq__(self, other):
        return self.major == other.major \
            and self.minor == other.minor \
            and self.bugfix == other.bugfix

    def __str__(self):
        return '%i.%i.%i' % (self.major, self.minor, self.bugfix)


class Package():
    """Package representation that contains information from multiple sources such as AUR and
    rosdistro"""

    def __init__(self, pkg_name):
        super(Package, self).__init__()
        self.package_name = pkg_name

        self.rosdistro_version = None
        self.aur_version = None

    def add_aur_information(self, aur_pkg):
        self.aur_version = Version(aur_pkg['Version'])

    def add_rosdistro_information(self, pkg_info):
        self.rosdistro_version = Version(pkg_info.version)

    def get_status(self):
        if self.aur_version:
            if self.rosdistro_version != self.aur_version:
                return 'outdated'
            return 'uptodate'
        elif self.rosdistro_version:
            return 'missing'

        # TODO throw
        return 'error'

    def __str__(self):
        output = '%s:\n - rosdistro: %s\n - AUR:       %s' % (self.package_name,
                                                              self.rosdistro_version,
                                                              self.aur_version)
        return output

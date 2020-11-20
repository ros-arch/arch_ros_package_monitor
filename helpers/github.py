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
import re
import urllib


class GHAdapter():
    """Wrapper for ros-<distro>-arch organization repos"""

    def __init__(self, distro_name):
        self.distro_name = distro_name
        self.repo_base_url = "https://raw.githubusercontent.com/ros-%s-arch" % distro_name

    def get_package_info(self, pkg_name):
        pkg = {'name': pkg_name}
        pkgbuild_url = '/'.join([self.repo_base_url, pkg_name, "master/PKGBUILD"])
        # print(pkgbuild_url)
        try:
            pkgbuild = urllib.request.urlopen(pkgbuild_url).read().decode('utf-8')
            regex = r"pkgver\s*=\s*[\"']?(?P<version>[^\"']+)[\"']?"
            match = re.search(regex, pkgbuild)
            if match:
                pkg['version'] = match.group('version')
                return pkg
            print('Could not parse GH version for package %s\nLink to PKGBUILD: %s'
                  % (pkg_name, pkgbuild_url))
        except urllib.request.URLError:
            # did not find corresponding GH repository
            # print("Did not find package %s on Github" % pkg_name)
            pass
        return None

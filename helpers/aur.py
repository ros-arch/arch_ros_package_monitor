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


import json
import sys
import urllib


class AURAdapter():
    """Wrapper for AURWeb rpc"""

    aur_api_url = "http://aur.archlinux.org/rpc.php"

    def __init__(self, distro_name):
        self.distro_name = distro_name
        self.packages = self._get_packages()


    def _get_packages(self):
        package_name = "ros-%s-" % self.distro_name
        params = urllib.parse.urlencode({'type': 'search', 'arg': package_name})
        response = urllib.request.urlopen("%s?%s" % (self.aur_api_url, params)).read()
        parsed_response = json.loads(response)
        if parsed_response['resultcount'] > 0:
            return parsed_response['results']
        # TODO throw
        print("Could not find any package matching %s" % package_name, file=sys.stderr)
        return list()

    def get_package_info(self, pkg_name):
        for pkg in self.packages:
            if pkg['Name'] == pkg_name:
                return pkg
        return None

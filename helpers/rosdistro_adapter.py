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


import rosdistro
from catkin_pkg import package


class RosdistroAdapter(object):
    """Small python wrapper to quickly query package information out of a rosdistro"""

    def __init__(self, distro_name):
        super(RosdistroAdapter, self).__init__()
        self._index = None
        self._distro_name = distro_name
        self._distro = self.get_distro()

    def get_distro(self):
        """Get a rosdistro object from the distro name configured in this object"""
        self._index = rosdistro.get_index(rosdistro.get_index_url())
        return rosdistro.get_cached_distribution(self._index, self._distro_name)

    def get_package_by_name(self, package_name):
        """Get a package representation from a package name"""
        manifest = self._distro.get_release_package_xml(package_name)
        return package.parse_package_string(manifest)

    def get_package_list(self):
        distr_file = rosdistro.get_distribution_file(self._index, self._distro_name)
        return distr_file.release_packages.keys()

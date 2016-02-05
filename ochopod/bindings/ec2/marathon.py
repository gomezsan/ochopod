#
# Copyright (c) 2015 Autodesk Inc.
# All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging
from requests import get

from ochopod.frameworks.marathon import Marathon

#: Our ochopod logger.
logger = logging.getLogger('ochopod')


class Pod(Marathon):
    """
    Implementation for the :class:`ochopod.frameworks.marathon.Marathon` base class.
    """

    def get_node_details(self):
        #
        # - we are (assuming to be) deployed on EC2
        # - get our underlying metadata using curl at 169.254.169.254
        #
        def _peek(token):
            return get('http://169.254.169.254/latest/meta-data/%s' % token).content

        #
        # - get our local and public IPV4 addresses
        # - the "node" will show up as the EC2 instance ID
        # - note we allow the public IPv4 lookup to fail (in case we run in VPC)
        #
        hints = \
            {
                'fwk': 'marathon (ec2)',
                'ip': _peek('local-ipv4'),
                'node': _peek('instance-id'),
                'public': _peek('public-ipv4'),
            }

        assert hints['ip'] and hints['node'], 'are you running on EC2 ?'
        return hints

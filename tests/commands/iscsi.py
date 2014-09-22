#
# Martin Gracik <mgracik@redhat.com>
#
# Copyright 2009 Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.  Any Red Hat
# trademarks that are incorporated in the source code or documentation are not
# subject to the GNU General Public License and may only be used or replicated
# with the express permission of Red Hat, Inc.
#

import unittest
from tests.baseclass import *

class FC6_TestCase(CommandTest):
    command = "iscsi"

    def runTest(self):
        # pass
        self.assert_parse("iscsi --ipaddr=1.1.1.1", "iscsi --ipaddr=1.1.1.1\n")
        self.assert_parse("iscsi --ipaddr=1.1.1.1 --target=tar --port=1234 --user=name --password=secret",
                          "iscsi --target=tar --ipaddr=1.1.1.1 --port=1234 --user=name --password=secret\n")
        self.assert_parse("iscsi --ipaddr=1.1.1.1 --target=tar", "iscsi --target=tar --ipaddr=1.1.1.1\n")
        self.assert_parse("iscsi --ipaddr=1.1.1.1 --port=1234", "iscsi --ipaddr=1.1.1.1 --port=1234\n")
        self.assert_parse("iscsi --ipaddr=1.1.1.1 --user=name", "iscsi --ipaddr=1.1.1.1 --user=name\n")
        self.assert_parse("iscsi --ipaddr=1.1.1.1 --password=secret", "iscsi --ipaddr=1.1.1.1 --password=secret\n")

        # fail
        # missing required option --ipaddr
        self.assert_parse_error("iscsi", KickstartValueError)
        self.assert_parse_error("iscsi --target=tar --user=name --password=secret --port=1234", KickstartValueError)
        # missing --ipaddr argument
        self.assert_parse_error("iscsi --ipaddr", KickstartParseError)
        # unexpected arguments
        self.assert_parse_error("iscsi --ipaddr=1.2.3.4 not expected", KickstartValueError)
        # unknown flag
        self.assert_parse_error("iscsi --ipaddr=1.2.3.4 --unknown=value", KickstartParseError)
        # empty arguments
        self.assert_parse_error("iscsi --target --ipaddr=1.2.3.4", KickstartParseError)
        self.assert_parse_error("iscsi --ipaddr=1.2.3.4 --user", KickstartParseError)
        self.assert_parse_error("iscsi --ipaddr=1.2.3.4 --password", KickstartParseError)
        self.assert_parse_error("iscsi --ipaddr=1.2.3.4 --port", KickstartParseError)


class F10_TestCase(FC6_TestCase):
    def runTest(self):
        # run FC6 test case
        FC6_TestCase.runTest(self)

        # pass
        self.assert_parse("iscsi --ipaddr=1.1.1.1 --reverse-user=name --reverse-password=secret",
                          "iscsi --ipaddr=1.1.1.1 --reverse-user=name --reverse-password=secret\n")
        self.assert_parse("iscsi --ipaddr=1.1.1.1 --reverse-user=name", "iscsi --ipaddr=1.1.1.1 --reverse-user=name\n")
        self.assert_parse("iscsi --ipaddr=1.1.1.1 --reverse-password=secret", "iscsi --ipaddr=1.1.1.1 --reverse-password=secret\n")

        # fail
        # empty arguments
        self.assert_parse_error("iscsi --ipaddr=1.1.1.1 --reverse-user", KickstartParseError)
        self.assert_parse_error("iscsi --ipaddr=1.1.1.1 --reverse-password", KickstartParseError)

class RHEL6_TestCase(F10_TestCase):
    def runTest(self):
        F10_TestCase.runTest(self)

        self.assert_parse("iscsi --ipaddr=1.1.1.1 --iface=eth0\n")

if __name__ == "__main__":
    unittest.main()

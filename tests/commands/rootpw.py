# Andy Lindeberg <alindebe@redhat.com>
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

from pykickstart.errors import *
from pykickstart.commands.rootpw import *

class FC3_TestCase(CommandTest):
    command = "rootpw"

    def runTest(self):
        # pass
        self.assert_parse("rootpw --iscrypted secrethandshake", "rootpw --iscrypted secrethandshake\n")

        # fail
        self.assert_parse_error("rootpw", KickstartValueError)
        self.assert_parse_error("rootpw --iscrypted=OMGSEKRITZ", KickstartParseError)
        self.assert_parse_error("rootpw --iscrypted", KickstartValueError)

class F8_TestCase(FC3_TestCase):
    def runTest(self):
        FC3_TestCase.runTest(self)

        # pass
        self.assert_parse("rootpw --lock secrethandshake", "rootpw --lock --plaintext secrethandshake\n")
        self.assert_parse("rootpw --plaintext secrethandshake", "rootpw --plaintext secrethandshake\n")
        self.assert_parse("rootpw --plaintext --iscrypted secrethandshake", "rootpw --iscrypted secrethandshake\n")
        self.assert_parse("rootpw --iscrypted --plaintext secrethandshake\n", "rootpw --plaintext secrethandshake\n")
        self.assert_parse("rootpw --lock --plaintext secrethandshake", "rootpw --lock --plaintext secrethandshake\n")
        self.assert_parse("rootpw --iscrypted --lock secrethandshake", "rootpw --iscrypted --lock secrethandshake\n")
        self.assert_parse("rootpw --lock --iscrypted --plaintext secrethandshake", "rootpw --lock --plaintext secrethandshake\n")
        self.assert_parse("rootpw --lock --plaintext --iscrypted secrethandshake", "rootpw --iscrypted --lock secrethandshake\n")
        self.assert_parse("rootpw --plaintext --iscrypted --lock secrethandshake", "rootpw --iscrypted --lock secrethandshake\n")
        self.assert_parse("rootpw --iscrypted --plaintext --lock secrethandshake", "rootpw --lock --plaintext secrethandshake\n")

        # fail
        self.assert_parse_error("rootpw --plaintext=ISEEENGLAND secrethandshake", KickstartParseError)
        self.assert_parse_error("rootpw --lock=NOKEYSFORYOU secrethandshake", KickstartParseError)
        self.assert_parse_error("rootpw --plaintext", KickstartValueError)

        if self.__class__.__name__ == "F8_TestCase":
            self.assert_parse_error("rootpw --lock", KickstartValueError)

class F18_TestCase(F8_TestCase):
    def runTest(self):
        F8_TestCase.runTest(self)

        self.assert_parse("rootpw --lock", "rootpw --lock\n")

if __name__ == "__main__":
    unittest.main()

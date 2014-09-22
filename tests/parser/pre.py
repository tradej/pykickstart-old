import unittest
from tests.baseclass import *

from pykickstart import constants
from pykickstart.errors import KickstartParseError
from pykickstart import version

class Simple_Terminated_TestCase(ParserTest):
    ks = """
%pre
ls /tmp
%end
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)
        self.assertEqual(len(self.handler.scripts), 1)

        # Verify the script defaults.
        script = self.handler.scripts[0]
        self.assertEqual(script.interp, "/bin/sh")
        self.assertFalse(script.inChroot)
        self.assertEqual(script.lineno, 2)
        self.assertFalse(script.errorOnFail)
        self.assertEqual(script.type, constants.KS_SCRIPT_PRE)

        # Also verify the body, which is the most important part.
        self.assertEqual(script.script.rstrip(), "ls /tmp")

class Simple_Header_TestCase(ParserTest):
    ks = """
%pre --interpreter /usr/bin/python --erroronfail --log=/tmp/blah
ls /tmp
%end
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)
        self.assertEqual(len(self.handler.scripts), 1)

        # Verify the changes we made in the header.
        script = self.handler.scripts[0]
        self.assertEqual(script.interp, "/usr/bin/python")
        self.assertFalse(script.inChroot)
        self.assertTrue(script.errorOnFail)
        self.assertEqual(script.lineno, 2)
        self.assertEqual(script.type, constants.KS_SCRIPT_PRE)
        self.assertEqual(script.logfile, "/tmp/blah")

        # Also verify the body, which is the most important part.
        self.assertEqual(script.script.rstrip(), "ls /tmp")

class Pre_Given_Nochroot_TestCase(ParserTest):
    ks = """
%pre --nochroot
ls /tmp
%end
"""

    def runTest(self):
        self.assertRaises(KickstartParseError, self.parser.readKickstartFromString, self.ks)

class Multiple_Terminated_TestCase(ParserTest):
    ks = """
%pre
ls /tmp
%end

%pre
ls /var
%end
"""

    def runTest(self):
        self.parser.readKickstartFromString(self.ks)
        self.assertEqual(len(self.handler.scripts), 2)

        # Verify the script defaults.
        script = self.handler.scripts[0]
        self.assertEqual(script.interp, "/bin/sh")
        self.assertFalse(script.inChroot)
        self.assertFalse(script.errorOnFail)
        self.assertEqual(script.lineno, 2)
        self.assertEqual(script.type, constants.KS_SCRIPT_PRE)

        # Also verify the body, which is the most important part.
        self.assertEqual(script.script.rstrip(), "ls /tmp")

        script = self.handler.scripts[1]
        self.assertEqual(script.script.rstrip(), "ls /var")

class Simple_Unterminated_TestCase(Simple_Terminated_TestCase):
    version = version.F7

    ks = """
%pre
ls /tmp
"""

class Simple_Unterminated_Fails_TestCase(Simple_Unterminated_TestCase):
    version = version.F8

    def runTest(self):
        self.assertRaises(KickstartParseError, self.parser.readKickstartFromString, self.ks)

class Multiple_Unterminated_TestCase(Multiple_Terminated_TestCase):
    version = version.F7

    ks = """
%pre
ls /tmp

%pre
ls /var
"""

class Multiple_Unterminated_Fails_TestCase(Multiple_Unterminated_TestCase):
    version = version.F8

    def runTest(self):
        self.assertRaises(KickstartParseError, self.parser.readKickstartFromString, self.ks)

if __name__ == "__main__":
    unittest.main()

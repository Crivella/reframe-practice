import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.builtins import run_after, run_before, sanity_function
from reframe.core.parameters import TestParam as parameter
from reframe.core.variables import TestVar as variable


@rfm.simple_test
class HelloTest(rfm.RegressionTest):
    valid_systems = ['*']
    valid_prog_environs = ['*']
    # sourcepath = './hw.c'
    lang = parameter(['c', 'cpp'])


    @run_before('compile')
    def set_sourcepath(self):
        self.sourcepath = f'hw.{self.lang}'

    @sanity_function
    def assert_hello(self):
        return sn.assert_found(r'Hello, World\!', self.stdout)
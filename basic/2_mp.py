import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.buildsystems import SingleSource
from reframe.core.builtins import run_after, run_before, sanity_function
from reframe.core.parameters import TestParam as parameter
from reframe.core.variables import TestVar as variable


@rfm.simple_test
class HelloThreadedTest(rfm.RegressionTest):
    valid_systems = ['*']
    valid_prog_environs = ['*']
    # sourcepath = './hw.c'
    # lang = parameter(['c', 'cpp'])
    sourcepath = 'hwmp.cpp'
    build_system = SingleSource()
    executable_opts = ['16']

    @run_before('compile')
    def set_compilation_flags(self):
        self.build_system.cppflags = ['-DSYNC_MESSAGES']
        self.build_system.cxxflags = ['-std=c++11', '-Wall']
        environ = self.current_environ.name
        if environ in {'clang', 'gnu'}:
            self.build_system.cxxflags += ['-pthread']

    @sanity_function
    def assert_hello(self):
        num_messages = sn.len(
            sn.findall(r'\[\s?\d+\] Hello, World\!', self.stdout)
            )
        return sn.assert_eq(num_messages, 16)
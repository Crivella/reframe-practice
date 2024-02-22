import os

import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.builtins import (require_deps, run_after, run_before,
                                   sanity_function)
from reframe.core.parameters import TestParam as parameter
from reframe.core.variables import TestVar as variable
from reframe.utility import udeps


@rfm.simple_test
class HelloTestBuild(rfm.CompileOnlyRegressionTest):
    valid_systems = ['cecam-workstation:default']
    valid_prog_environs = ['gnu', 'clang']
    # sourcepath = './hw.c'
    # lang = parameter(['c', 'cpp'])
    lang = variable(str, value='c')


    @run_before('compile')
    def set_sourcepath(self):
        self.sourcepath = f'hw.{self.lang}'

    @sanity_function
    def assert_hello(self):
        return sn.assert_true(os.path.exists(self.executable))
        # return sn.assert_found(r'Hello, World\!', self.stdout)
    

@rfm.simple_test
class HelloTestRun(rfm.RunOnlyRegressionTest):
    valid_systems = ['cecam-workstation:default']
    valid_prog_environs = ['gnu', 'clang']
    # sourcepath = './hw.c'
    # lang = parameter(['c', 'cpp'])


    @run_after('init')
    def inject_dependencies(self):
        # variants = HelloTestBuild.get_variant_nums()
        # for v in variants:
        #     self.depends_on(HelloTestBuild.variant_name(v))
        self.depends_on('HelloTestBuild', udeps.by_env)

    @require_deps
    def set_vars(self, HelloTestBuild):
        self.executable = HelloTestBuild().executable
        self.sourcesdir = HelloTestBuild().stagedir

    @sanity_function
    def assert_hello(self):
        return sn.assert_found(r'Hello, World\!', self.stdout)
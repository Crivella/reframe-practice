import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.buildsystems import SingleSource
from reframe.core.builtins import (performance_function, run_after, run_before,
                                   sanity_function)
from reframe.core.containers import Docker
from reframe.core.parameters import TestParam as parameter
from reframe.core.variables import TestVar as variable


@rfm.simple_test
class ContainerTest(rfm.RunOnlyRegressionTest):
    platform = variable(str, value='Docker')
    valid_systems = ['cecam-workstation:container']
    valid_prog_environs = ['builtin']
    image = parameter(['ubuntu:22.04', 'ubuntu:20.04', None])
    executable = 'echo'
    executable_opts = ['Hello from the container!']
    # container_platform = Docker()
    
    @run_before('run')
    def setup_container_platf(self):
        self.container_platform = 'Docker'
        self.container_platform.image = self.image
        self.container_platform.command = ' '.join([self.executable] + self.executable_opts)

    @sanity_function
    def validate_solution(self):
        return sn.assert_found(r'Hello from the container\!', self.stdout)

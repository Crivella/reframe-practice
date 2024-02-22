import reframe as rfm
import reframe.utility.sanity as sn
from reframe.core.buildsystems import SingleSource
from reframe.core.builtins import (performance_function, run_after, run_before,
                                   sanity_function)
from reframe.core.parameters import TestParam as parameter
from reframe.core.variables import TestVar as variable


@rfm.simple_test
class StreamTest(rfm.RegressionTest):
    num_bytes = parameter(1 << pow for pow in range(19, 30))
    array_size = variable(int)
    ntimes = variable(int)

    valid_systems = ['*']
    valid_prog_environs = ['gnu']
    # sourcepath = './hw.c'
    # lang = parameter(['c', 'cpp'])
    sourcepath = 'stream.c'
    prebuild_cmds = [
        'wget https://raw.githubusercontent.com/jeffhammond/STREAM/master/stream.c'
    ]
    build_system = SingleSource()
    env_vars = {
        'OMP_NUM_THREADS': '4',
        'OMP_PLACES': 'cores'
    }
    # reference = {
    #     'cecam-workstation': {
    #         'Copy':  (25200, -0.05, 0.05, 'MB/s'),
    #         'Scale': (16800, -0.05, 0.05, 'MB/s'),
    #         'Add':   (18500, -0.05, 0.05, 'MB/s'),
    #         'Triad': (18800, -0.05, 0.05, 'MB/s')
    #     }
    # }
    
    @run_after('init')
    def setup_build(self):
        self.array_size = (self.num_bytes >> 3) // 3
        self.ntimes = 100*1024*1024 // self.array_size
        self.descr = (
            f'STREAM test (array size: {self.array_size}, '
            f'ntimes: {self.ntimes})'
        )

    @run_before('compile')
    def set_compilation_flags(self):
        self.build_system.cppflags = [
            f'-DSTREAM_ARRAY_SIZE={self.array_size}',
            f'-DNTIMES={self.ntimes}'
            ]
        self.build_system.cflags = ['-fopenmp', '-O3', '-Wall']

    @sanity_function
    def validate_solution(self):
        return sn.assert_found(r'Solution Validates', self.stdout)

    @performance_function('MB/s', perf_key='Triad')
    def extract_triad_bw(self):
        return sn.extractsingle(r'Triad:\s+(\S+)\s+.*', self.stdout, 1, float)
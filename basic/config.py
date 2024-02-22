# Copyright 2016-2024 Swiss National Supercomputing Centre (CSCS/ETH Zurich)
# and other ReFrame Project Developers. See the top-level LICENSE file for
# details.
#
# SPDX-License-Identifier: BSD-3-Clause


site_configuration = {
    'systems': [
        {
            'name': 'cecam-workstation',
            'descr': 'CECAM Workstation',
            'hostnames': ['crivella-desktop'],
            'modules_system': 'nomod',
            'partitions': [
                {
                    'name': 'default',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['gnu', 'clang'],
                },
                {
                    'name': 'container',
                    'scheduler': 'local',
                    'launcher': 'local',
                    'environs': ['builtin'],
                    'container_platforms': [
                            {
                                'type': 'Docker',
                                'modules': [],
                            },
                        ],
                }
            ]
        }
    ],
    'environments': [
        {
            'name': 'gnu',
            'cc': 'gcc-11',
            'cxx': 'g++-11',
            'ftn': 'gfortran-11',
            'target_systems': ['cecam-workstation']
        },
        {
            'name': 'clang',
            'cc': 'clang-14',
            'cxx': 'clang++-14',
            'ftn': '',
            'target_systems': ['cecam-workstation']
        },
    ]
}
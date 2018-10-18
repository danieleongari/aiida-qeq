""" Tests for calculations

"""
from __future__ import print_function
from __future__ import absolute_import

import aiida_qeq.tests as tests
#import aiida_qeq.data as data
from aiida.utils.fixtures import PluginTestCase
import os


class TestEqeq(PluginTestCase):
    def setUp(self):
        # Set up code, if it does not exist
        self.code = tests.get_code(entry_point='qeq.eqeq')

    def test_submit(self):  # pylint: disable=too-many-locals
        """Test submitting a calculation"""
        from aiida.orm.data.singlefile import SinglefileData
        from aiida.orm.data.cif import CifData
        import aiida_qeq.data as data

        code = self.code

        # Prepare input parameters
        from aiida.orm import DataFactory
        EQeqParameters = DataFactory('qeq.eqeq')
        parameters = EQeqParameters({'method': 'ewald'})

        charge_file = SinglefileData(
            file=os.path.join(data.DATA_DIR, data.DEFAULT_CHARGE_FILE_NAME))
        ionization_file = SinglefileData(
            file=os.path.join(data.DATA_DIR, data.
                              DEFAULT_IONIZATION_FILE_NAME))
        cif = CifData(
            file=os.path.join(tests.TEST_DIR, 'HKUST1.cif'),
            parse_policy='lazy')

        # set up calculation
        calc = code.new_calc()
        calc.label = "aiida_qeq test"
        calc.description = "Test job submission with the aiida_qeq plugin"
        calc.set_max_wallclock_seconds(30)
        calc.set_withmpi(False)
        calc.set_resources({"num_machines": 1, "num_mpiprocs_per_machine": 1})

        calc.use_parameters(parameters)
        calc.use_charge_data(charge_file)
        calc.use_ionization_data(ionization_file)
        calc.use_structure(cif)

        calc.store_all()

        # output input files and scripts to temporary folder
        from aiida.common.folders import SandboxFolder
        with SandboxFolder() as folder:
            subfolder, script_filename = calc.submit_test(folder=folder)
            print("inputs created successfully at {0} with script {1}".format(
                subfolder.abspath, script_filename))
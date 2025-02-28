import os
from glob import glob
import importlib
import inspect
from pyvisa import ResourceManager
import yaml

from pyoctal.instruments.base import DeviceID
from pyoctal.utils.util import get_callable_funcs

class TestClassCalls:
    """
    Test that all the classes in the instruments folder can be called and have a docstring.
    """
    sim_fpath = './tests/sim_dev.yaml'
    sim_rm = sim_fpath + '@sim'
    untestable_files = ("thorlabsAPT", 'keysightPAS', "fiberlabsAMP","base")
    untestable_modules = [
        'BaseInstrument','BaseSweeps', 'DeviceID','KeysightFlexDCA',
        'KeysightILME','ThorlabsAPT', 'FiberlabsAMP', "Agilent816xB"
    ]

    def test_instr_initialization(self):
        """ Test that the instruments can all be connected. """

        with open(file=self.sim_fpath, mode='r', encoding="utf-8") as file:
            configs = yaml.safe_load(file)

        # get parameters straight from the yaml file

        rm = ResourceManager(self.sim_rm)
        addr = rm.list_resources()[0]
        identity = configs["devices"]["device 1"]["dialogues"][0]["r"]
        tested_module = []

        # search through the name of the files matching *.py under the folder
        for file in glob(os.path.join("./pyoctal/instruments" + "/*.py")):
            name = os.path.splitext(os.path.basename(file))[0]
            # ignore the two classes as they are not inherited from BaseInstrument class
            if name in self.untestable_files:
                continue
            module = f'pyoctal.instruments.{name}'

            # perform dynamic import
            for member, cls in inspect.getmembers(importlib.import_module(module), inspect.isclass):
                print(member)
                if str(member).startswith('__') or \
                    member in self.untestable_modules + tested_module:
                    continue
                tested_module.append(member)
                # initialise a device
                dev = cls(addr=addr, rm=rm)
                dev.connect()
                # check that the ids are as expected
                assert DeviceID(identity) == dev.identity
        rm.close()

    def test_class_docstrings(self):
        """ Test that the instruments all have a class docstring and display it when tested. """
        # get the address from opening up another resource manager
        rm = ResourceManager(self.sim_rm)
        addr = rm.list_resources()[0]
        tested_module = []

        # search through the name of the files matching *.py under the folder
        print()
        print("-"*117)
        print(f'| {"Class":<20} | {"Description":<90} |')
        print("-"*117)
        for file in glob(os.path.join("./pyoctal/instruments" + "/*.py")):
            name = os.path.splitext(os.path.basename(file))[0]
            # ignore the two classes as they are not inherited from BaseInstrument class
            if name in self.untestable_files:
                continue
            module = f'pyoctal.instruments.{name}'
            # perform dynamic import
            for member, cls in inspect.getmembers(importlib.import_module(module), inspect.isclass):
                if member in self.untestable_modules + tested_module or str(member).startswith('__'):
                    continue

                # make sure that tested modules won't be tested again
                tested_module.append(member)

                dev = cls(addr=addr, rm=rm) # instantiate a device
                dev.connect()
                doc = cls.__doc__.split('.')[0].rstrip().lstrip()
                print(f"| {member:20} | {doc:90} |")
        print("-"*117)
        rm.close()

def test_callable_funcs():
    from pyoctal.instruments.base import BaseInstrument
    funcs = get_callable_funcs(obj=BaseInstrument)
    test_funcs = ['write', 'query', 'get_idn'] # only testing a fraction of callable functions
    assert [name for name in test_funcs if name in funcs]

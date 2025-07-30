import importlib.util
import sys
import types
import os

# Stub config.config_ to avoid heavy imports
if 'config' not in sys.modules:
    sys.modules['config'] = types.ModuleType('config')
if 'config.config_' not in sys.modules:
    dummy = types.ModuleType('config.config_')
    import re
    dummy.re = re
    sys.modules['config.config_'] = dummy

module_path = os.path.join(os.path.dirname(__file__), os.pardir,
                           'Cleansing', 'libs', 'or_utils_.py')
spec = importlib.util.spec_from_file_location('or_utils', module_path)
or_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(or_utils)


def test_remove_delimiter_dots():
    assert or_utils.remove_delimiter('1.500.000') == '1500000'


def test_remove_delimiter_comma_dot():
    assert or_utils.remove_delimiter('2,029.7') == '2029.7'

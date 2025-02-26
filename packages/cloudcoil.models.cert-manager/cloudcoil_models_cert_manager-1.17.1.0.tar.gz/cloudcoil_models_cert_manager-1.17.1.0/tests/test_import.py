from types import ModuleType

import cloudcoil.models.cert_manager as cert_manager


def test_has_modules():
    modules = list(filter(lambda x: isinstance(x, ModuleType), cert_manager.__dict__.values()))
    assert modules, "No modules found in cert_manager"

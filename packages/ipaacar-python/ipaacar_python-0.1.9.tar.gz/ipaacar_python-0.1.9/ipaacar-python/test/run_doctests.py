import doctest
import importlib
import inspect
import pkgutil
import sys
import tomllib
import ipaacar


def find_recursive(obj, name='', module_name=None):
    finder = doctest.DocTestFinder()

    tests = []
    if inspect.isclass(obj):
        tests.extend(finder.find(obj))

    if inspect.ismodule(obj):
        if module_name is None:
            module_name = obj.__name__

        for attr_name in obj.__dict__:
            attr = getattr(obj, attr_name)
            if inspect.isclass(attr):
                tests.extend(finder.find(attr))

            if inspect.ismodule(attr) and attr.__name__.startswith(module_name):
                tests.extend(find_recursive(attr, name=f'{name}.{attr_name}', module_name=module_name))

    return tests


# with open("../Cargo.toml", "rb") as f:
#    cargo_toml = tomllib.load(f)
# lib_name = cargo_toml["lib"]["name"]
# module = __import__(lib_name)#, fromlist=cargo_toml["package"]["metadata"]["doctest_classes"])
# print("Running Doctests for Module", lib_name)
runner = doctest.DocTestRunner(verbose=True)
for test in find_recursive(ipaacar):
    runner.run(test)
res = runner.summarize()
if res[0] > 0:
    sys.exit(1)

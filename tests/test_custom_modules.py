"""


Run pystest in terminal:

    (venv) $ cd ~/github/pizza_project
    (venv) $ python3 -m pytest -v pizzapy/tests/test_custom_modules.py


"""

import os
import site


def test_batterypy_dimsumpy_available_in_site_packages():

    site_packages_dir = site.getsitepackages()

    packages = []
    
    for directory in site_packages_dir:
        packages = packages + os.listdir(directory)
    
    print(site_packages_dir)

    print(packages)

    assert any("batterypy" in s for s in packages)

    assert any("dimsumpy" in s for s in packages)



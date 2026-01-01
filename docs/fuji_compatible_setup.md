


Q: HOW TO MAKE A FUJI COMPATIBLE VENV?

    1. Use apt pandas and numpy, they are build with wider CPU support
        sudo apt install python3-pandas python3-numpy
        ie pandas 1.5.3

    2. Use Debian 12 system python3.11 to build venv, and include system python packages

        /usr/bin/python3 -m venv --system-site-packages venv

    3. Make a custom requirements.txt in pizza/ folder, parent of pizzapy. This file should not contain pandas and numpy.

    * When I use py 3.11 venv, and pip install pandas 1.5.3, this does not work. Fuji will show `Illegal instruction`.

    * Not sure if I can use 3.14 python to work with system pandas 1.5.3

    * The unsupported CPU instruction set is mainly caused by numpy, not pandas.


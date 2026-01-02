


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




Q : HOW TO FIX VERSION CONFLICTS OF `urllib3`? DUE TO MY VENV INCLUDE SYSTEM PACKAGES --system-site-packages.

This is a dependency conflict issue. Your system has an incompatible version of `urllib3` (2.6.2) that doesn't work with the older system-installed `requests-toolbelt`. Here are several solutions:

## Solution 1: Upgrade requests-toolbelt (Recommended)

```bash
pip install --upgrade requests-toolbelt
```

## Solution 2: Downgrade urllib3

```bash
pip install 'urllib3<2.0'
```

## Solution 3: Upgrade all related packages

```bash
pip install --upgrade requests urllib3 requests-toolbelt cloudscraper
```

## Solution 4: Fix the system/venv conflict

The issue is that you're mixing system packages (`/usr/lib/python3/dist-packages/`) with venv packages. To fix this:

```bash
# Uninstall the system package version (if you have sudo access)
sudo apt remove python3-requests-toolbelt

# Or create a fresh virtual environment without system packages
deactivate
cd /opt/github/pizza
rm -rf venv
python3 -m venv venv --without-system-packages
source venv/bin/activate

# Reinstall your dependencies
pip install --upgrade pip
pip install requests urllib3 requests-toolbelt cloudscraper
# ... install other dependencies
```

## Solution 5: Quick workaround - Install compatible versions

```bash
pip install 'urllib3<2.0' 'requests>=2.28.0' 'requests-toolbelt>=0.10.1'
```

**Try Solution 1 first** - it's the simplest. If that doesn't work, try Solution 3, then Solution 4 if you continue to have issues.

The root cause is that `urllib3` 2.x removed the `appengine` module, but older versions of `requests-toolbelt` still try to import it.
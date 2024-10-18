"""
Run the program:
1. Activate virtual environment

    $ cd ~/github

    $ source venv/bin/activate

    (I put venv outside pizzapy repo to prevent upload)

2. Run Pizza:

    (venv) $ python3 -m pizzapy.main
    OR
    (venv) $ python3 -m pizzapy.updater

    No need to import sys and sys.append in this main module because this main.py module is in the program folder.
"""

from .gui_dock.main_dock_controller import main

if __name__ == '__main__':
    main()

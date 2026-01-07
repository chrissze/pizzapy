"""
Run the program:
1. Activate virtual environment

    $ cd ~/github

    $ source venv/bin/activate

    (I put venv outside pizzapy repo to prevent upload)

2. Run Pizza:

    (venv) $ python3 -m pizzapy.main
    OR
    (venv) $ python3 -m pizzapy.cli

    No need to import sys and sys.append in this main module because this main.py module is in the program folder.

3. Generate new S&P 500 and Nasdaq 100 components:

    (venv) $ python3 generate_file_model.py
    
"""

from pizzapy.gui_dock.main_dock_controller import main

if __name__ == '__main__':
    main()

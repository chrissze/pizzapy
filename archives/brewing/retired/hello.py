Last login: Wed Aug 30 13:24:26 on ttys002
hi I'm chris  /Users/chris/.bash_profile start
hi I'm chris  /Users/chris/.bash_profile ends

The default interactive shell is now zsh.
To update your account to use zsh, please run `chsh -s /bin/zsh`.
For more details, please visit https://support.apple.com/kb/HT208050.
17:52:46 Wed Aug 30 chris@CHRISs-Mac-mini ~ $ the shell is bash
-bash: the: command not found
17:52:46 Wed Aug 30 chris@CHRISs-Mac-mini ~ $ which llvm
17:52:51 Wed Aug 30 chris@CHRISs-Mac-mini ~ $ which clang
/opt/homebrew/opt/llvm/bin/clang
17:52:55 Wed Aug 30 chris@CHRISs-Mac-mini ~ $ cd github/pizzapy/
/Users/chris/github/pizzapy

__init__.py		main.py			stock_core_browser
brewing			main_dock		core_stock_update
documentation.txt	main_script.py		stock_price_browser
futures_browser		requirements.txt	stock_price_update
futures_update		shared_model		venv
17:53:12 Wed Aug 30 chris@CHRISs-Mac-mini ~/github/pizzapy $ venv
(venv) 17:53:17 Wed Aug 30 chris@CHRISs-Mac-mini ~/github/pizzapy $ pipr
Requirement already satisfied: beautifulsoup4==4.12 in ./venv/lib/python3.11/site-packages (from -r requirements.txt (line 5)) (4.12.0)
Collecting lxml==4.3 (from -r requirements.txt (line 7))
  Using cached lxml-4.3.0.tar.gz (2.5 MB)
  Preparing metadata (setup.py) ... done
Requirement already satisfied: pandas==2.0 in ./venv/lib/python3.11/site-packages (from -r requirements.txt (line 9)) (2.0.0)
Requirement already satisfied: psycopg[binary,pool] in ./venv/lib/python3.11/site-packages (from -r requirements.txt (line 11)) (3.1.10)
Requirement already satisfied: PySide6==6.5 in ./venv/lib/python3.11/site-packages (from -r requirements.txt (line 13)) (6.5.0)
Requirement already satisfied: requests==2.31 in ./venv/lib/python3.11/site-packages (from -r requirements.txt (line 15)) (2.31.0)
Requirement already satisfied: wheel in ./venv/lib/python3.11/site-packages (from -r requirements.txt (line 26)) (0.41.2)
Requirement already satisfied: soupsieve>1.2 in ./venv/lib/python3.11/site-packages (from beautifulsoup4==4.12->-r requirements.txt (line 5)) (2.4.1)
Requirement already satisfied: python-dateutil>=2.8.2 in ./venv/lib/python3.11/site-packages (from pandas==2.0->-r requirements.txt (line 9)) (2.8.2)
Requirement already satisfied: pytz>=2020.1 in ./venv/lib/python3.11/site-packages (from pandas==2.0->-r requirements.txt (line 9)) (2023.3)
Requirement already satisfied: tzdata>=2022.1 in ./venv/lib/python3.11/site-packages (from pandas==2.0->-r requirements.txt (line 9)) (2023.3)
Requirement already satisfied: numpy>=1.21.0 in ./venv/lib/python3.11/site-packages (from pandas==2.0->-r requirements.txt (line 9)) (1.25.2)
Requirement already satisfied: shiboken6==6.5.0 in ./venv/lib/python3.11/site-packages (from PySide6==6.5->-r requirements.txt (line 13)) (6.5.0)
Requirement already satisfied: PySide6-Essentials==6.5.0 in ./venv/lib/python3.11/site-packages (from PySide6==6.5->-r requirements.txt (line 13)) (6.5.0)
Requirement already satisfied: PySide6-Addons==6.5.0 in ./venv/lib/python3.11/site-packages (from PySide6==6.5->-r requirements.txt (line 13)) (6.5.0)
Requirement already satisfied: charset-normalizer<4,>=2 in ./venv/lib/python3.11/site-packages (from requests==2.31->-r requirements.txt (line 15)) (3.2.0)
Requirement already satisfied: idna<4,>=2.5 in ./venv/lib/python3.11/site-packages (from requests==2.31->-r requirements.txt (line 15)) (3.4)
Requirement already satisfied: urllib3<3,>=1.21.1 in ./venv/lib/python3.11/site-packages (from requests==2.31->-r requirements.txt (line 15)) (2.0.4)
Requirement already satisfied: certifi>=2017.4.17 in ./venv/lib/python3.11/site-packages (from requests==2.31->-r requirements.txt (line 15)) (2023.7.22)
Requirement already satisfied: typing-extensions>=4.1 in ./venv/lib/python3.11/site-packages (from psycopg[binary,pool]->-r requirements.txt (line 11)) (4.7.1)
Requirement already satisfied: psycopg-binary==3.1.10 in ./venv/lib/python3.11/site-packages (from psycopg[binary,pool]->-r requirements.txt (line 11)) (3.1.10)
Requirement already satisfied: psycopg-pool in ./venv/lib/python3.11/site-packages (from psycopg[binary,pool]->-r requirements.txt (line 11)) (3.1.7)
Requirement already satisfied: six>=1.5 in ./venv/lib/python3.11/site-packages (from python-dateutil>=2.8.2->pandas==2.0->-r requirements.txt (line 9)) (1.16.0)
Building wheels for collected packages: lxml
  Building wheel for lxml (setup.py) ... error
  error: subprocess-exited-with-error

  × python setup.py bdist_wheel did not run successfully.
  │ exit code: 1
  ╰─> [93 lines of output]
      Building lxml version 4.3.0.
      /private/var/folders/k3/9czshfgn0sjd3vf8zzy51clr0000gn/T/pip-install-916uyiek/lxml_8343726434ff4471ae22e06d49514020/setup.py:61: DeprecationWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html
        import pkg_resources
      Building without Cython.
      Using build configuration of libxslt 1.1.35
      Building against libxml2/libxslt in the following directory: /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/lib
      running bdist_wheel
      running build
      running build_py
      creating build
      creating build/lib.macosx-13-arm64-cpython-311
      creating build/lib.macosx-13-arm64-cpython-311/lxml
      copying src/lxml/_elementpath.py -> build/lib.macosx-13-arm64-cpython-311/lxml
      copying src/lxml/sax.py -> build/lib.macosx-13-arm64-cpython-311/lxml
      copying src/lxml/pyclasslookup.py -> build/lib.macosx-13-arm64-cpython-311/lxml
      copying src/lxml/__init__.py -> build/lib.macosx-13-arm64-cpython-311/lxml
      copying src/lxml/builder.py -> build/lib.macosx-13-arm64-cpython-311/lxml
      copying src/lxml/doctestcompare.py -> build/lib.macosx-13-arm64-cpython-311/lxml
      copying src/lxml/usedoctest.py -> build/lib.macosx-13-arm64-cpython-311/lxml
      copying src/lxml/cssselect.py -> build/lib.macosx-13-arm64-cpython-311/lxml
      copying src/lxml/ElementInclude.py -> build/lib.macosx-13-arm64-cpython-311/lxml
      creating build/lib.macosx-13-arm64-cpython-311/lxml/includes
      copying src/lxml/includes/__init__.py -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      creating build/lib.macosx-13-arm64-cpython-311/lxml/html
      copying src/lxml/html/soupparser.py -> build/lib.macosx-13-arm64-cpython-311/lxml/html
      copying src/lxml/html/defs.py -> build/lib.macosx-13-arm64-cpython-311/lxml/html
      copying src/lxml/html/_setmixin.py -> build/lib.macosx-13-arm64-cpython-311/lxml/html
      copying src/lxml/html/clean.py -> build/lib.macosx-13-arm64-cpython-311/lxml/html
      copying src/lxml/html/_diffcommand.py -> build/lib.macosx-13-arm64-cpython-311/lxml/html
      copying src/lxml/html/html5parser.py -> build/lib.macosx-13-arm64-cpython-311/lxml/html
      copying src/lxml/html/__init__.py -> build/lib.macosx-13-arm64-cpython-311/lxml/html
      copying src/lxml/html/formfill.py -> build/lib.macosx-13-arm64-cpython-311/lxml/html
      copying src/lxml/html/builder.py -> build/lib.macosx-13-arm64-cpython-311/lxml/html
      copying src/lxml/html/ElementSoup.py -> build/lib.macosx-13-arm64-cpython-311/lxml/html
      copying src/lxml/html/_html5builder.py -> build/lib.macosx-13-arm64-cpython-311/lxml/html
      copying src/lxml/html/usedoctest.py -> build/lib.macosx-13-arm64-cpython-311/lxml/html
      copying src/lxml/html/diff.py -> build/lib.macosx-13-arm64-cpython-311/lxml/html
      creating build/lib.macosx-13-arm64-cpython-311/lxml/isoschematron
      copying src/lxml/isoschematron/__init__.py -> build/lib.macosx-13-arm64-cpython-311/lxml/isoschematron
      copying src/lxml/etree.h -> build/lib.macosx-13-arm64-cpython-311/lxml
      copying src/lxml/etree_api.h -> build/lib.macosx-13-arm64-cpython-311/lxml
      copying src/lxml/lxml.etree.h -> build/lib.macosx-13-arm64-cpython-311/lxml
      copying src/lxml/lxml.etree_api.h -> build/lib.macosx-13-arm64-cpython-311/lxml
      copying src/lxml/includes/xmlerror.pxd -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      copying src/lxml/includes/c14n.pxd -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      copying src/lxml/includes/xmlschema.pxd -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      copying src/lxml/includes/__init__.pxd -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      copying src/lxml/includes/schematron.pxd -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      copying src/lxml/includes/tree.pxd -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      copying src/lxml/includes/uri.pxd -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      copying src/lxml/includes/etreepublic.pxd -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      copying src/lxml/includes/xpath.pxd -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      copying src/lxml/includes/htmlparser.pxd -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      copying src/lxml/includes/xslt.pxd -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      copying src/lxml/includes/config.pxd -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      copying src/lxml/includes/xmlparser.pxd -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      copying src/lxml/includes/xinclude.pxd -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      copying src/lxml/includes/dtdvalid.pxd -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      copying src/lxml/includes/relaxng.pxd -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      copying src/lxml/includes/lxml-version.h -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      copying src/lxml/includes/etree_defs.h -> build/lib.macosx-13-arm64-cpython-311/lxml/includes
      creating build/lib.macosx-13-arm64-cpython-311/lxml/isoschematron/resources
      creating build/lib.macosx-13-arm64-cpython-311/lxml/isoschematron/resources/rng
      copying src/lxml/isoschematron/resources/rng/iso-schematron.rng -> build/lib.macosx-13-arm64-cpython-311/lxml/isoschematron/resources/rng
      creating build/lib.macosx-13-arm64-cpython-311/lxml/isoschematron/resources/xsl
      copying src/lxml/isoschematron/resources/xsl/XSD2Schtrn.xsl -> build/lib.macosx-13-arm64-cpython-311/lxml/isoschematron/resources/xsl
      copying src/lxml/isoschematron/resources/xsl/RNG2Schtrn.xsl -> build/lib.macosx-13-arm64-cpython-311/lxml/isoschematron/resources/xsl
      creating build/lib.macosx-13-arm64-cpython-311/lxml/isoschematron/resources/xsl/iso-schematron-xslt1
      copying src/lxml/isoschematron/resources/xsl/iso-schematron-xslt1/iso_abstract_expand.xsl -> build/lib.macosx-13-arm64-cpython-311/lxml/isoschematron/resources/xsl/iso-schematron-xslt1
      copying src/lxml/isoschematron/resources/xsl/iso-schematron-xslt1/iso_dsdl_include.xsl -> build/lib.macosx-13-arm64-cpython-311/lxml/isoschematron/resources/xsl/iso-schematron-xslt1
      copying src/lxml/isoschematron/resources/xsl/iso-schematron-xslt1/iso_schematron_skeleton_for_xslt1.xsl -> build/lib.macosx-13-arm64-cpython-311/lxml/isoschematron/resources/xsl/iso-schematron-xslt1
      copying src/lxml/isoschematron/resources/xsl/iso-schematron-xslt1/iso_svrl_for_xslt1.xsl -> build/lib.macosx-13-arm64-cpython-311/lxml/isoschematron/resources/xsl/iso-schematron-xslt1
      copying src/lxml/isoschematron/resources/xsl/iso-schematron-xslt1/iso_schematron_message.xsl -> build/lib.macosx-13-arm64-cpython-311/lxml/isoschematron/resources/xsl/iso-schematron-xslt1
      copying src/lxml/isoschematron/resources/xsl/iso-schematron-xslt1/readme.txt -> build/lib.macosx-13-arm64-cpython-311/lxml/isoschematron/resources/xsl/iso-schematron-xslt1
      running build_ext
      building 'lxml.etree' extension
      creating build/temp.macosx-13-arm64-cpython-311
      creating build/temp.macosx-13-arm64-cpython-311/src
      creating build/temp.macosx-13-arm64-cpython-311/src/lxml
      clang -Wsign-compare -Wunreachable-code -fno-common -dynamic -DNDEBUG -g -fwrapv -O3 -Wall -DCYTHON_CLINE_IN_TRACEBACK=0 -I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include -Isrc -Isrc/lxml/includes -I/Users/chris/github/pizzapy/venv/include -I/opt/homebrew/opt/python@3.11/Frameworks/Python.framework/Versions/3.11/include/python3.11 -c src/lxml/etree.c -o build/temp.macosx-13-arm64-cpython-311/src/lxml/etree.o -w -flat_namespace
      src/lxml/etree.c:289:12: fatal error: 'longintrepr.h' file not found
        #include "longintrepr.h"
                 ^~~~~~~~~~~~~~~
      1 error generated.
      Compile failed: command '/opt/homebrew/opt/llvm/bin/clang' failed with exit code 1
      creating var
      creating var/folders
      creating var/folders/k3
      creating var/folders/k3/9czshfgn0sjd3vf8zzy51clr0000gn
      creating var/folders/k3/9czshfgn0sjd3vf8zzy51clr0000gn/T
      cc -I/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include -I/usr/include/libxml2 -c /var/folders/k3/9czshfgn0sjd3vf8zzy51clr0000gn/T/xmlXPathInithp2_u5kx.c -o var/folders/k3/9czshfgn0sjd3vf8zzy51clr0000gn/T/xmlXPathInithp2_u5kx.o
      cc var/folders/k3/9czshfgn0sjd3vf8zzy51clr0000gn/T/xmlXPathInithp2_u5kx.o -L/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/lib -lxml2 -o a.out
      error: command '/opt/homebrew/opt/llvm/bin/clang' failed with exit code 1
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
  ERROR: Failed building wheel for lxml
  Running setup.py clean for lxml
Failed to build lxml
ERROR: Could not build wheels for lxml, which is required to install pyproject.toml-based projects
(venv) 17:53:23 Wed Aug 30 chris@CHRISs-Mac-mini ~/github/pizzapy $ pipr
Requirement already satisfied: beautifulsoup4==4.12 in ./venv/lib/python3.11/site-packages (from -r requirements.txt (line 5)) (4.12.0)
Collecting lxml (from -r requirements.txt (line 7))
  Obtaining dependency information for lxml from https://files.pythonhosted.org/packages/d6/56/9d5cb3438143a5aebad59088ca392950d74a531e1b96d0959144370b3b59/lxml-4.9.3-cp311-cp311-macosx_11_0_universal2.whl.metadata
  Downloading lxml-4.9.3-cp311-cp311-macosx_11_0_universal2.whl.metadata (3.8 kB)
Requirement already satisfied: pandas==2.0 in ./venv/lib/python3.11/site-packages (from -r requirements.txt (line 9)) (2.0.0)
Requirement already satisfied: psycopg[binary,pool] in ./venv/lib/python3.11/site-packages (from -r requirements.txt (line 11)) (3.1.10)
Requirement already satisfied: PySide6==6.5 in ./venv/lib/python3.11/site-packages (from -r requirements.txt (line 13)) (6.5.0)
Requirement already satisfied: requests==2.31 in ./venv/lib/python3.11/site-packages (from -r requirements.txt (line 15)) (2.31.0)
Requirement already satisfied: wheel in ./venv/lib/python3.11/site-packages (from -r requirements.txt (line 26)) (0.41.2)
Requirement already satisfied: soupsieve>1.2 in ./venv/lib/python3.11/site-packages (from beautifulsoup4==4.12->-r requirements.txt (line 5)) (2.4.1)
Requirement already satisfied: python-dateutil>=2.8.2 in ./venv/lib/python3.11/site-packages (from pandas==2.0->-r requirements.txt (line 9)) (2.8.2)
Requirement already satisfied: pytz>=2020.1 in ./venv/lib/python3.11/site-packages (from pandas==2.0->-r requirements.txt (line 9)) (2023.3)
Requirement already satisfied: tzdata>=2022.1 in ./venv/lib/python3.11/site-packages (from pandas==2.0->-r requirements.txt (line 9)) (2023.3)
Requirement already satisfied: numpy>=1.21.0 in ./venv/lib/python3.11/site-packages (from pandas==2.0->-r requirements.txt (line 9)) (1.25.2)
Requirement already satisfied: shiboken6==6.5.0 in ./venv/lib/python3.11/site-packages (from PySide6==6.5->-r requirements.txt (line 13)) (6.5.0)
Requirement already satisfied: PySide6-Essentials==6.5.0 in ./venv/lib/python3.11/site-packages (from PySide6==6.5->-r requirements.txt (line 13)) (6.5.0)
Requirement already satisfied: PySide6-Addons==6.5.0 in ./venv/lib/python3.11/site-packages (from PySide6==6.5->-r requirements.txt (line 13)) (6.5.0)
Requirement already satisfied: charset-normalizer<4,>=2 in ./venv/lib/python3.11/site-packages (from requests==2.31->-r requirements.txt (line 15)) (3.2.0)
Requirement already satisfied: idna<4,>=2.5 in ./venv/lib/python3.11/site-packages (from requests==2.31->-r requirements.txt (line 15)) (3.4)
Requirement already satisfied: urllib3<3,>=1.21.1 in ./venv/lib/python3.11/site-packages (from requests==2.31->-r requirements.txt (line 15)) (2.0.4)
Requirement already satisfied: certifi>=2017.4.17 in ./venv/lib/python3.11/site-packages (from requests==2.31->-r requirements.txt (line 15)) (2023.7.22)
Requirement already satisfied: typing-extensions>=4.1 in ./venv/lib/python3.11/site-packages (from psycopg[binary,pool]->-r requirements.txt (line 11)) (4.7.1)
Requirement already satisfied: psycopg-binary==3.1.10 in ./venv/lib/python3.11/site-packages (from psycopg[binary,pool]->-r requirements.txt (line 11)) (3.1.10)
Requirement already satisfied: psycopg-pool in ./venv/lib/python3.11/site-packages (from psycopg[binary,pool]->-r requirements.txt (line 11)) (3.1.7)
Requirement already satisfied: six>=1.5 in ./venv/lib/python3.11/site-packages (from python-dateutil>=2.8.2->pandas==2.0->-r requirements.txt (line 9)) (1.16.0)
Downloading lxml-4.9.3-cp311-cp311-macosx_11_0_universal2.whl (8.6 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 8.6/8.6 MB 10.5 MB/s eta 0:00:00
Installing collected packages: lxml
Successfully installed lxml-4.9.3
Package            Version
------------------ ---------
beautifulsoup4     4.12.0
certifi            2023.7.22
charset-normalizer 3.2.0
idna               3.4
lxml               4.9.3
numpy              1.25.2
pandas             2.0.0
pip                23.2.1
psycopg            3.1.10
psycopg-binary     3.1.10
psycopg-pool       3.1.7
PySide6            6.5.0
PySide6-Addons     6.5.0
PySide6-Essentials 6.5.0
python-dateutil    2.8.2
pytz               2023.3
requests           2.31.0
setuptools         68.1.2
shiboken6          6.5.0
six                1.16.0
soupsieve          2.4.1
typing_extensions  4.7.1
tzdata             2023.3
urllib3            2.0.4
wheel              0.41.2
(venv) 17:53:38 Wed Aug 30 chris@CHRISs-Mac-mini ~/github/pizzapy $
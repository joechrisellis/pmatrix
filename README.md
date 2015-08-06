pmatrix
=======

pmatrix is a cmatrix clone written in Python. It creates the falling text display.

Installation (using pip)
========================

The easiest and best way to install pmatrix is using pip.

1. If you don't have pip installed, use your package manager to install the package python-pip. For Debian based systems
   the command to use would be `$ sudo apt-get install python-pip`.
2. Next, use pip to install pmatrix. `$ pip install pmatrix`

Installation (from source)
==========================

Installing pmatrix is easy. It is worth noting that this package will only work on \*nix systems. This is because the
Python curses module responsible for terminal control is currently only supported on \*nix systems. With that in mind,
if you're running a \*nix system, you can follow these steps:

1. Get the source. `$ git clone https://github.com/jce-devel/pmatrix`
2. Enter the source directory. `$ cd pmatrix`
3. If you don't have sudo installed/configured, execute setup.py as the root user. `$ su && python setup.py install`
4. if you have sudo installed, log in as a sudoer and execute the setup.py file with sudo. `$ sudo setup.py install`
5. Done! It should now be a simple case of executing `$ pmatrix` in your favorite terminal emulator.

pmatrix in Action
=================

![pmatrix --help](http://i.imgur.com/1sQNm6Q.png)
![pmatrix -f red](http://i.imgur.com/a6PWnER.png)
![pmatrix -f white -b black](http://i.imgur.com/veXrhYA.png)
![pmatrix -p 1](http://i.imgur.com/dKBmndR.png)

TODO
====

* Work on efficiency. You will always have to expect some overhead with Python and accept the fact that pmatrix will
  never be as fast as cmatrix.
* Parallelize loops (if possible).

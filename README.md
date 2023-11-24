# Logical Statement (+arithmetics!) Graphical User Interface

>`Name:` **Taib Izzat Samawi**
>`NRP :` **5025221085**

Created in order to complete a Discrete Math assignment in Institut Teknologi Sepuluh Nopember (ITS) Surabaya

> This program is created solely by me (Taib Izzat Samawi).
> This means, nowhere in the code is copy-pasted from another source.

> Currently, the license of this code is set as **Private/Closed-source**
> If there exists a submission or program with a similar look,
> please do notify me through my email, as such instances
> may signify attempts in plagiarizing my work without my permision.

## Features
- Convert a logical statement into its prefix tree
- Convert an arithmetic statement into its prefix tree
- Convert a logical statemtent into a logical circuit

## Tech

This application utilizes a number of open-source packages to run smoothly:
- [Python] - The most popular programming language for hobbyist developers!
- [TkInter] - Python binding to the Tk GUI toolkit
- [Schemdraw] - The one-stop package for high-quality electrical circuit schematic diagrams.
- [Pillow] - Supercharge python with image-processing abilities!
- [MatPlotLib] - Comprehensive library for creating static, animated, and interactive visualizations in Python

## Installation
Install all the packages required by this application
```sh
pip install -r requirements.txt
```

Run the python application
```sh
cd src/
python ./logical_statement_tree.py
```

## Using the app
- After running the app, a window will appear. Users can input a logical or arithmetic statement inside the input box.
- There will be 2 buttons. The button labeled `find tree` will show the prefix tree of the statement. The button labeled `find tree and circuit` will first remove all non-junction operations in the statement and creates both the prefix tree and logical circuit of the statement.

[//]: # 
   [Python]: <https://www.python.org/>
   [TkInter]: <https://wiki.python.org/moin/TkInter>
   [Schemdraw]: <https://schemdraw.readthedocs.io/en/stable/>
   [Pillow]: <https://pypi.org/project/Pillow/>
   [MatPlotLib]: <https://matplotlib.org/>

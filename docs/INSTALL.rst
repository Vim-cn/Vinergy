============
Installation
============

1. Make sure to install all required modules.

2. If you want to do the test, to enter the directory of Vinergy, then::

    ~ % nosetests

  **Note** ``~ %`` is NOT part of command.

3. Run::

    ~ % python setup.py install

  You can also extract ``vinergy/`` to the place wherever you want to.

4. Open vinergy/config.py with your favorite editor, change ``URL`` (site url)
   and ``DBURL`` (database url) to fit your server environment.

5. Start service::

    ~ % ./vinergy/vinergy.py

  Done.


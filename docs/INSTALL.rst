============
Installation
============

.. TODO fix all broken sentences

1. Make sure to install all required modules.

2. Run::

    ~ % python setup.py install

  **Note** ``~ %`` is NOT part of command.

  You can also extract ``vinergy/`` to the place wherever you want to.

3. Import ``dbsetup.sql`` to setup tables.

4. Start service::

    ~ % ./vinergy/vinergy.py --db=psql-connection-string

  Done.


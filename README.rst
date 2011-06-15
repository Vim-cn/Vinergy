=======
Vinergy
=======

..
    __     __ _                                 
    \ \   / /(_) _ __    ___  _ __  __ _  _   _ 
     \ \ / / | || '_ \  / _ \| '__|/ _` || | | |
      \ V /  | || | | ||  __/| |  | (_| || |_| |
       \_/   |_||_| |_| \___||_|   \__, | \__, |
                                   |___/  |___/ 

-----------------------------
CLI Pastebin within VimEnergy
-----------------------------

Make sure to check Github_ for the latest updates.

.. _Github: https://github.com/vayn/vinergy


Requirement
-----------

web.py_, pymongo_, pygments_, and nosetests_, paste_ (for testing)

.. _web.py: http://webpy.org
.. _pymongo: http://pypi.python.org/pypi/pymongo/
.. _pygments: http://pygments.org
.. _nosetests: http://somethingaboutorange.com/mrl/projects/nose/
.. _paste: http://pythonpaste.org


Installation
------------

See ``docs/INSTALL.rst``


Usage
-----

    ~ % cat bin/pyconsole.vim | curl -F 'vimcn=<-' http://p.vim-cn.com
       http://p.vim-cn.com/cbc

    ~ % curl http://p.vim-cn.com/cbc?js

    ~ % wget -qO- http://p.vim-cn.com/cbc/js

    ~ % firefox http://p.vim-cn.com/cbc?js


Credit
------

Special thanks to rupa_ and his sprunge_.

.. _rupa: https://github.com/rupa/
.. _sprunge: http://sprunge.us


License
-------

This program is released unders ``GPL3`` license, see ``LICENSE`` for more detail.

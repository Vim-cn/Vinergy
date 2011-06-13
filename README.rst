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


Installation
------------

Requirement
^^^^^^^^^^^

web.py_, pymongo_, pygments_, and nosetests_, paste_ (for testing)

.. _web.py: http://webpy.org
.. _pymongo: pypi.python.org/pypi/pymongo/
.. _pygments: http://pygments.org
.. _nosetests: http://somethingaboutorange.com/mrl/projects/nose/
.. _paste: http://pythonpaste.org


Usage
-----

    ~ % cat bin/pyconsole.vim | curl -F 'vimcn=<-' http://p.vim-cn.com
       http://p.vim-cn.com/wuitE

    ~ % curl http://p.vim-cn.com/wuitE?vim
    ~ % firefox http://p.vim-cn.com/wuitE?vim

Credit
------

Special thanks to rupa_ and his sprunge_.

.. _rupa: https://github.com/rupa/
.. _sprunge: http://sprunge.us


License
-------

This program is released unders ``GPL3`` license, see ``LICENSE`` for more detail.

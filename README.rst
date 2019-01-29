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

Make sure to check GitHub_ for the latest updates.

.. _GitHub: https://github.com/Vim-cn/Vinergy


Requirements
------------

tornado_, asyncpg_, pygments_

.. _tornado: http://www.tornadoweb.org/
.. _asyncpg: https://pypi.org/project/asyncpg/
.. _pygments: http://pygments.org


Installation
------------

See ``docs/INSTALL.rst``


Usage
-----

    ~ % cat bin/pyconsole.vim | curl -F 'vimcn=<-' https://cfp.vim-cn.com
       https://cfp.vim-cn.com/cbc

    ~ % curl https://cfp.vim-cn.com/cbc?js

    ~ % wget -qO- https://cfp.vim-cn.com/cbc/js

    ~ % firefox https://cfp.vim-cn.com/cbc?js


Authors
-------

Vayn <vayn at vayn dot de>

lilydjwg <lilydjwg at gmail dot com>


Credit
------

Special thanks to rupa_ and his sprunge_.

.. _rupa: https://github.com/rupa
.. _sprunge: http://sprunge.us


License
-------

This program is released under ``GPLv3`` license, see ``LICENSE`` for more detail.

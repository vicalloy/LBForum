=======
LBForum
=======

.. contents::

.. |rst| replace:: :emphasis:`re`\ :strong:`Structured`\ :sup:`Text`

LBForum is a quick and simple forum which uses the Django Framework (written 
in Python language). LBForum is a reusable Django application, can be added 
to any existing django project.
LBForum is distributed under the BSD and GPL license. 

Demo site(Skin FluxBB): http://vik.haoluobo.com/lbforum/
Demo site(Skin V2EX): http://vik.haoluobo.com/lbforum2/

Demo site's source: https://github.com/vicalloy/lbforum-site

Features
========

* user-friendly installation process
* the ease of integration into any Django project and the ease of installation
* classic view of the forum like FluxBB
* Allow users to upload attachments to their posts(by AJAX).
* avatar support(Gravatar or user upload)
* BBCode support
* friendly edtor(by markItUp!).
* Sticky threads (These threads are always sorted first in the list of threads)

Requirements
============

* `Python 2.5+`_
* `Django 1.3+`_
* PIL_
* django-pagination_
* `south 0.7.2+`_
* postmarkup_
* BeautifulSoup_
* django-helper_
* django-lb-attachments_
* django-onlineuser_
* django-simple-avatar_

.. _`Python 2.5+`: http://python.org/
.. _`Django 1.3+`: http://www.djangoproject.com/
.. _PIL: http://www.pythonware.com/products/pil/
.. _django-pagination: http://code.google.com/p/django-pagination/
.. _`south 0.7.2+`: http://south.aeracode.org/
.. _BeautifulSoup: http://www.crummy.com/software/BeautifulSoup/
.. _postmarkup: http://code.google.com/p/postmarkup/
.. _django-helper: https://github.com/vicalloy/django-helper
.. _django-lb-attachments: https://github.com/vicalloy/django-lb-attachments
.. _django-onlineuser: https://github.com/vicalloy/onlineuser
.. _django-simple-avatar: https://github.com/vicalloy/django-simple-avatar

Installation
============

Installation
------------

#. Install LBForum by easy_install or pip.

``easy_install``::

    $ easy_install lbforum

``pip``::

    $ pip install lbforum

Configuration
-------------

Config urls.py::

    (r'^attachments/', include('attachments.urls')),
    (r'^', include('lbforum.urls')),


The LBForum has some settings should be set in `settings.py`:

#. Add the following app to ``INSTALLED_APPS``::

    'pagination', 
    'south',
    'lbforum',
    'simpleavatar',
    'djangohelper',
    'onlineuser',
    'attachments',

#. Add the following middleware to ``MIDDLEWARE_CLASSES``::

    'pagination.middleware.PaginationMiddleware',
    'onlineuser.middleware.OnlineUserMiddleware',
    
#. add ``"djangohelper.context_processors.ctx_config",`` to ``TEMPLATE_CONTEXT_PROCESSORS``::

    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.core.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.core.context_processors.request",

        "djangohelper.context_processors.ctx_config",
    )

#. setting urls for lbforum::
    
    # URL prefix for lbforum media -- CSS, JavaScript and images. Make sure to use a
    # trailing slash.
    # Examples: "http://foo.com/media/", "/media/".    
    
    #The URL where requests are redirected after login
    LOGIN_REDIRECT_URL = '/'
    #The URL where requests are redirected for login
    LOGIN_URL = "/accounts/login/"
    #LOGIN_URL counterpart
    LOGOUT_URL = "/accounts/logout/"
    #register url 
    REGISTER_URL = '%saccounts/register/' % ROOT_URL
    
#. vars for templates::

    CTX_CONFIG = {
            'LBFORUM_TITLE': 'LBForum',
            'LBFORUM_SUB_TITLE': 'A forum engine written in Python using Django',
            'FORUM_PAGE_SIZE': 50,
            'TOPIC_PAGE_SIZE': 20,
    
            'LOGIN_URL': LOGIN_URL,
            'LOGOUT_URL': LOGOUT_URL,
            'REGISTER_URL': REGISTER_URL,
            }
            
#. settings for BBCODE::

    BBCODE_AUTO_URLS = True
    #add allow tags
    HTML_SAFE_TAGS = ['embed']
    HTML_SAFE_ATTRS = ['allowscriptaccess', 'allowfullscreen', 'wmode']
    #add forbid tags
    HTML_UNSAFE_TAGS = []
    HTML_UNSAFE_ATTRS = []
    
    """
    #default html safe settings 
    acceptable_elements = ['a', 'abbr', 'acronym', 'address', 'area', 'b', 'big',
        'blockquote', 'br', 'button', 'caption', 'center', 'cite', 'code', 'col',
        'colgroup', 'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt', 'em',
        'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 
        'ins', 'kbd', 'label', 'legend', 'li', 'map', 'menu', 'ol', 
        'p', 'pre', 'q', 's', 'samp', 'small', 'span', 'strike',
        'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
        'thead', 'tr', 'tt', 'u', 'ul', 'var']
    acceptable_attributes = ['abbr', 'accept', 'accept-charset', 'accesskey',
        'action', 'align', 'alt', 'axis', 'border', 'cellpadding', 'cellspacing',
        'char', 'charoff', 'charset', 'checked', 'cite', 'clear', 'cols',
        'colspan', 'color', 'compact', 'coords', 'datetime', 'dir', 
        'enctype', 'for', 'headers', 'height', 'href', 'hreflang', 'hspace',
        'id', 'ismap', 'label', 'lang', 'longdesc', 'maxlength', 'method',
        'multiple', 'name', 'nohref', 'noshade', 'nowrap', 'prompt', 
        'rel', 'rev', 'rows', 'rowspan', 'rules', 'scope', 'shape', 'size',
        'span', 'src', 'start', 'summary', 'tabindex', 'target', 'title', 'type',
        'usemap', 'valign', 'value', 'vspace', 'width', 'style']
    """
    
#. if you want to use skin v2ex, you should add the follow config to settings.py::

    #always show topic post in topic page.
    LBF_STICKY_TOPIC_POST = True
    #show last topic in index page
    LBF_LAST_TOPIC_NO_INDEX = True
    #add v2ex template dir to TEMPLATE_DIRS
    import lbforum
    V2EX_TEMPLATE_DIR = os.path.join(lbforum.__path__[0], 'templates_v2ex')
    TEMPLATE_DIRS = (
            os.path.join(HERE, 'templates_plus'),
            os.path.join(HERE, 'templates_v2ex'),
            V2EX_TEMPLATE_DIR,
    )
    
Initialize The Database
-----------------------

#. Run command ``manage.py migrate``

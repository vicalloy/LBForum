=======
LBForum
=======

.. contents::

.. |rst| replace:: :emphasis:`re`\ :strong:`Structured`\ :sup:`Text`

LBForum is a quick and simple forum which uses the Django Framework (written
in Python language). LBForum is a reusable Django application, can be added
to any existing django project.
LBForum is distributed under the BSD.

Demo site: http://lbf.haoluobo.com/

Demo site's source: https://github.com/vicalloy/lbforum-site

Features
========

* user-friendly installation process
* the ease of integration into any Django project and the ease of installation
* classic view of the forum like FluxBB
* Allow users to upload attachments to their posts(by AJAX).
* avatar support
* BBCode support
* friendly edtor(by markItUp!).
* Sticky threads (These threads are always sorted first in the list of threads)

Requirements
============

* `Python 2.7 or 3.4+`_
* `Django 1.10`_

.. _`Python 2.7 or 3.4+`: http://python.org/
.. _`Django 1.10`: http://www.djangoproject.com/

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

    url(r'^', include('lbforum.urls')),
    url(r'^attachments/', include('lbattachment.urls')),


The LBForum has some settings should be set in `settings.py`:

#. Add the following app to ``INSTALLED_APPS``::

    'el_pagination',
    'easy_thumbnails',
    'constance',
    'constance.backends.database',
    'djangobower',

    'lbforum',
    'lbattachment',
    'lbutils',

#. Add the following middleware to ``TEMPLATES['OPTIONS']['context_processors']``::

    'django.contrib.messages.context_processors.messages',
    
#. setting urls for lbforum::
    
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(PRJ_ROOT, 'collectedstatic')

    HOST_URL = ''
    MEDIA_URL_ = '/media/'
    MEDIA_URL = HOST_URL + MEDIA_URL_
    MEDIA_ROOT = os.path.join(PRJ_ROOT, 'media')
    
    SIGNUP_URL = '/accounts/signup/'
    LOGIN_URL = '/accounts/login/'
    LOGOUT_URL = '/accounts/logout/'
    LOGIN_REDIRECT_URL = '/'
    CHANGE_PASSWORD_URL = '/accounts/password/change/'

#. settings for constance::

    CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

    CONSTANCE_CONFIG = {
        'forbidden_words': ('', 'Forbidden words', str),
    }

#. settings for bower::

    from django.conf.global_settings import STATICFILES_FINDERS
    STATICFILES_FINDERS += (('djangobower.finders.BowerFinder'),)

    BOWER_COMPONENTS_ROOT = PRJ_ROOT

    BOWER_INSTALLED_APPS = (
        'jquery#1.12',
        'markitup#1.1.14',
        'mediaelement#2.22.0',
        'blueimp-file-upload#9.12.5',
    )
    
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
    
Initialize The Database & Static Files
-----------------------

#. Run command ``manage.py bower install``

#. Run command ``manage.py migrate``

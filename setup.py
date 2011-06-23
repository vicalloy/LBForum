from setuptools import setup, find_packages
import lbforum

version = lbforum.__version__

setup(
    name = "LBForum",
    version = version,
    url = 'https://github.com/vicalloy/LBForum',
    author = 'vicalloy',
    author_email = 'zbirder@gmail.com',
    description = 'LBForum is a quick and simple forum which uses the Django Framework.',
    packages=find_packages(),
    install_requires=[
        "Django>=1.2",
        "django-helper>=0.8.1",
        "django-lb-attachments>=0.8",
        "django-onlineuser>=0.8",
        "django-simple-avatar>=0.8.1",
        "BeautifulSoup",
        "postmarkup",
        "django-pagination",
        "PIL",
        "south>=0.7.2",
        ],
    classifiers = ['Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   ],
)

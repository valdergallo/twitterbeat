#from distutils.core import setup
from setuptools import setup, find_packages

# http://guide.python-distribute.org/quickstart.html
# python setup.py sdist
# python setup.py register
# python setup.py sdist upload
# pip install twitterbeat
# pip install twitterbeat --upgrade --no-deps
# Manual upload to PypI
# http://pypi.python.org/pypi/twitterbeat
# Go to 'edit' link
# Update version and save
# Go to 'files' link and upload the file


tests_require = [
]

install_requires = [
    'python-twitter==0.8.2',
    'feedparser==5.1.2'
]

setup(name='twitterbeat',
      url='https://github.com/valdergallo/twitterbeat',
      author="valdergallo",
      author_email='valdergallo@gmail.com',
      keywords='python django twitter follow subprocess daemon',
      description='A library to follow one user from twitter with daemon mode.',
      license='MIT',
      classifiers=[
          'Framework :: Django',
          'Operating System :: OS Independent',
          'Topic :: Software Development'
      ],

      version='0.9',
      install_requires=install_requires,
      # tests_require=tests_require,
      # test_suite='runtests.runtests',
      # extras_require={'test': tests_require},

      packages=find_packages(),
)
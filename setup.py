from setuptools import setup, find_packages

setup(name='thevoid-extractor',
      version='0.1.0',
      entry_points={
          'console_scripts': [
              'thevoid-extractor = thevoid_extractor:main',
          ],
      })

# EOF #

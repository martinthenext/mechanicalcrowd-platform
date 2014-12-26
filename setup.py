#!/usr/bin/env python3
from setuptools import setup

setup(name='mcrowd-platform',
      version='0.0.1',
      description="Mechanical Crowd Platform",
      author='Kirill Goldshtein',
      author_email='goldshtein.kirill@gmail.com',
      packages=["mcrowd", "mcrowd.xlsx", "mcrowd.task",
                "mcrowd.mturk", "mcrowd.common", "mcrowd.audit"],
      install_requires=open('requirements.txt').read().split('\n'),
      scripts=['mcrowd.py'],
      license='Commercial',
      url='https://github.com/martinthenext/mechanicalcrowd-platform',
      classifiers=['Intended Audience :: Developers',
                   'Environment :: Console',
                   'Programming Language :: Python :: 3.4',
                   'Natural Language :: English',
                   'Development Status :: 1 - Planning',
                   'Operating System :: Unix',
                   'Topic :: Utilities'])

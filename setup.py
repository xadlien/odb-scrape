from setuptools import setup

setup(name='odb-scrape',
      version='0.1',
      description='Program to pull devotional info from Our Daily Bread',
      url='https://github.com/xadlien/odb-scrape',
      author='Daniel Martin',
      author_email='djm24862@gmail.com',
      packages=['odbscrape'],
      install_requires=['psycopg2', 'requests'],
      entry_points = {
          'console_scripts': ['odb-scrape=odbscrape.odb_scrape:main']
      },
      zip_safe=False)
from setuptools import setup


setup(name='stransfer',
      version='0.1.2',
      py_modules=['stransfer'],
      author='Terry Lim',
      url='https://github.com/terry-lim/stransfer',
      description="helps cookie transfer between requests "
                  "session and selenium browser instance with ease",
      install_requires=[
          'requests>=2.18.1',
          'selenium>=3.7.0',
          'beautifulsoup4>=4.6.0',
          'pytest>=3.2.5',
          'pytest-cov>=2.5.1',
          'flake8>=3.5.0'
      ],
      license='MIT',
      keywords=['cookie', 'session', 'selenium',
                'requests', 'chrome', 'firefox']
      )

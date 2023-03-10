from setuptools import setup, find_packages

setup(name='mercury-proxy',
      version='1.0',
      url='https://github.com/webtoucher/mercury-proxy',
      license='BSD-3-Clause',
      author='Alexey Kuznetsov',
      author_email='mirakuru@webtoucher.ru',
      description='Proxy server for communicating with Incotex Mercury meters via TCP/IP',
      classifiers=[
          'Development Status :: 1 - Planning',
          'Intended Audience :: Developers',
          'Topic :: Internet :: Proxy Servers',
          'Topic :: Terminals :: Serial',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3',
          'Operating System :: Unix',
      ],
      packages=find_packages(),
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      install_requires=[
          'flask~=2.2.2',
          'mercury-base~=1.2',
          'simple-socket-server~=1.8',
          'waitress~=2.1.2',
      ],
      zip_safe=False)

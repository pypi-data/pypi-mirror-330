from os import path
from setuptools import setup, find_packages
import io

version = '2.0.2'

# Just here for Python2
# compatibility
# If not needed:
# import setuptools
# if __name__ == "__main__":
# setuptools.setup()

here = path.abspath(path.dirname(__file__))
with io.open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
	name='xmllayout2',
    version=version,
    description="Formats Python log messages as log4j XMLLayout XML",
    long_description=long_description,
    classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: BSD License',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: Implementation :: CPython',
		'Programming Language :: Python :: Implementation :: PyPy',
		'Programming Language :: Python :: Implementation :: Jython',
		'Topic :: System :: Logging'
    ],
    keywords='logging log4j',
    author='Jonas Lindner',
    author_email='jonaslindner55@gmail.com',
    url='http://pypi.python.org/pypi/XMLLayout',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    tests_require=['pytest'],
)

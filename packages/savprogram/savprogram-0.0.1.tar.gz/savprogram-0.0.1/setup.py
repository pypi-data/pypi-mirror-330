from setuptools import setup, find_packages

classifiers = [
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3.11'
]

setup(
    name='savprogram',
    version='0.0.1',
    description='A library with different Machine Learning Algorithms: Hill Climbing, Simulated Annealing, Brute Force, and A star search',
    long_description=open('README.md').read(),
    url='',
    author='Savannah Shannon',
    author_email='snshannon2002@gmail.com',
    License='GNU',
    classifiers=classifiers,
    keywords='ai algorithms',
    packages=find_packages(),
    install_requires=['']
)

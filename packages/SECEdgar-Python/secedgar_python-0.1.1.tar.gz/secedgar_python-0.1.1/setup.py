from setuptools import setup, find_packages

setup(
    name='SECEdgar-Python',
    version='0.1.1',
    author='Aasa Singh Bhui',
    author_email='aasasingh2005@gmail.com',
    description='A Python package for SEC Edgar data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AasaSingh05/SECEdgarPy',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.25.1',
        'pandas>=1.2.0',
        'beautifulsoup4>=4.9.3',
        'lxml>=4.6.2',
    ],
)
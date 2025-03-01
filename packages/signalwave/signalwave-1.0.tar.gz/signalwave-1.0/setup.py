from setuptools import setup, find_packages

setup(
    name='signalwave',
    version='1.0',
    packages=find_packages(),
    install_requires=['numpy'],
    author='Sourceduty',
    author_email='sourceduty@gmail.com',
    description='A library for creating and analyzing signal wave function models.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://sourceduty.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

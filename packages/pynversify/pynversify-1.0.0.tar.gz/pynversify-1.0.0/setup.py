from setuptools import setup, find_packages

setup(
    name='pynversify',
    version='1.0.0',
    packages=find_packages(),
    description='Dependency Injection Container inspired by Inversify for Python',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Fernando Dorantes',
    author_email='fernando@dorant.es',
    url='https://github.com/fdorantesm/pynversify',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

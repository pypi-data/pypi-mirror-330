from setuptools import setup, find_packages

setup(
    name='akatool',
    version='0.0.5',
    description='read descript thag writed by korean what write in github.',
    author='du7ec',
    author_email='dutec6834@gmail.com',
    url='https://github.com/FarAway6834/akatool',
    install_requires=['edprompt', 'lbdc', 'sympy', 'ipitin'],
    packages=find_packages(exclude=[]),
    python_requires='>=3.6',
    package_data={},
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
    ],
)

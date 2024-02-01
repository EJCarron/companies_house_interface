from setuptools import setup

setup(
    name='companies_house_interface',
    version='0.1.0',
    py_modules=['chi'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'chi = chi:chi',
        ],
    },
)
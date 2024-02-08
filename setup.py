from setuptools import setup, find_packages

setup(
    name='companies_house_interface',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['requests~=2.31.0',
                      'neo4j~=5.16.0',
                      'click~=8.1.7',
                      'XlsxWriter~=3.1.9',
                      'pandas~=2.0.3',
                      'thefuzz~=0.22.1'
                      ],
    entry_points={
        'console_scripts': [
            'chi = src.scripts.chi:chi',
        ],
    },
)

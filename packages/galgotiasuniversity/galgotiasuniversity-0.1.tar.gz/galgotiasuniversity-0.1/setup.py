from setuptools import setup, find_packages


setup(
    name='galgotiasuniversity',
    version='0.1',
    packages=find_packages(),
    install_requires=[
    ],
    
    entry_points={
        'console_scripts': [
            'hi = ansira:hi',
        ]
    }
    
    
)
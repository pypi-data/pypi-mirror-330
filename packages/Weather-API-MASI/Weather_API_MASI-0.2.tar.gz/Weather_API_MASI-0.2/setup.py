from setuptools import setup, find_packages

setup(
    name='Weather_API_MASI',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'requests>=2.31.0',
        'selenium>=4.28.1',
        'geopy>=2.4.1'
    ],
    entry_points={
        "console_scripts": ["Weather-API-MASI = Weather_API_MASI.main:main"]
    }
)

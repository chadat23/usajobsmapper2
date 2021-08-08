from setuptools import find_packages, setup

setup(
    name='usajobsmapped',
    version='0.0.3',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'folium',
        'geopy'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-mock'],
)

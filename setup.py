from setuptools import setup, find_packages

with open('requirements.txt') as f:	
    requirements = f.read().splitlines()

setup(
    name='bhl_born_digital_utils',
    version='0.0.1',
    url='https://github.com/bentley-historical-library/bhl_born_digital_utils',
    author='Bentley Historical Library',
    packages=find_packages(),
    scripts=['bhl_bd_utils.py'],
    include_package_data=True,
    description='Bentley Historical Library born-digital utilities',
    install_requires=requirements
)
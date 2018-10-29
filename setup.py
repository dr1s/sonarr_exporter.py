from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sonarr_exporter',
    version='0.1.dev0',
    url='https://github.com/dr1s/sonarr_exporter.py',
    author='dr1s',
    author_email='dr1s@drs.li',
    license='Apache License 2.0',
    description='Export sonarr metrics for prometheus',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["prometheus_client"],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts':
        ['sonarr_exporter=sonarr_exporter:main']
    },
)

from setuptools import setup, find_packages

NAME = "valuate"
PACKAGES = [NAME] + ["%s.%s" % (NAME, i) for i in find_packages(NAME)]

setup(
    name=NAME,
    version='5.1.7',
    author='DJ Leo',
    author_email='m18349125880@gmail.com',
    description='Used car valuation api.',
    packages=PACKAGES,
    package_data={
        '': ['*.csv'],
    },
    install_requires=[
        'numpy==1.15.4',
        'pandas==0.23.4',
        'setuptools==40.6.2',
        'SQLAlchemy==1.2.14',
        'mysql-connector-python==8.0.5',
        'PyMySQL==0.9.2',
    ],
    # include_package_data=True
)

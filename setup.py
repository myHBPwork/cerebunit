# ~/cerebunit/setup.py
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
        name="cerebunit",
        version="0.3.0",
        author="Lungsi",
        author_email="lungsi.sharma@unic.cnrs-gif.fr",
        #packages=find_packages(),
        packages=["cerebunit",
                  #"cerebunit.file_manager",
                  #"cerebunit.test_manager",
                  "cerebunit.statistics",
                  # capabilities 
                  "cerebunit.capabilities",
                  "cerebunit.capabilities.cells",
                  # validation_tests
                  "cerebunit.validation_tests",
                  "cerebunit.validation_tests.cells",
                  #"cerebunit.validation_tests.cells.general",
                  #"cerebunit.validation_tests.cells.PurkinjeCell",
                  "cerebunit.validation_tests.cells.Granule",
                  #"cerebunit.validation_tests.cells.GolgiCell"
                  ],
        #url="",
        license="BSD Clause-3",
        #description="",
        long_description="",
        #install_requires=["sciunit>=0.1.3.1"]
)
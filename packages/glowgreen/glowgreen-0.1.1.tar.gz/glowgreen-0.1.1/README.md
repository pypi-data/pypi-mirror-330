[![DOI](https://zenodo.org/badge/546642261.svg)](https://zenodo.org/badge/latestdoi/546642261)

# glowgreen
A Python package for calculating radiation dose from close contact patterns with radioactive patients. 

## Requires
- Python >= 3.9

## Installation
Install the package from the [Python Package Index](https://pypi.org/) (PyPI) using `pip`:

    python -m pip install --upgrade glowgreen

Alternatively, if you have a clone of the repository on your local computer, you can install it via the *pyproject.toml* file.
First update your pip:

    python -m pip install --upgrade pip

Then enter e.g.:

    python -m pip install -e \path\to\glowgreen\

These are the preferred methods as they handle the dependencies for you. 
Another way is to add the **src** directory to the PYTHONPATH environment variable. For example, for Windows:

    set PYTHONPATH=%PYTHONPATH%;\path\to\glowgreen\src\

## Dependencies
Python packages:
- `numpy` >= 1.21.4
- `scipy` >= 1.7.3
- `matplotlib` >= 3.5.0
- `pandas` >= 1.3.4

It has not been tested with earlier versions of these packages.

## Test suite
You can run the test suite if you have a clone of this repository and glowgreen is installed or in PYTHONPATH. Install `pytest`:

    python -m pip install pytest

Then in the root directory run:

    python -m pytest

## Documentation
Documentation including API reference can be found here: https://glowgreen.readthedocs.io.

### Building the documentation

Documentation is generated using `sphinx`.
See this [tutorial](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/read-the-docs.html). 

If the **docs/source/** directory does not exist, see *howto_documentation.md* to bootstrap the documentation.
Otherwise, do the following:

Ensure the hand-crafted elements of the documentation in the **docs** directory are up-to-date: 
- project information in *docs/source/conf.py*
- *src/glowgreen_sample.py* is used to generate the figures in *docs/source* and some of the text in *docs/source/overview.rst*

Install `sphinx`:

    python -m pip install sphinx

Note the empty directories **docs/source/_static** and **docs/source/_templates** are not under version control; optionally create these empty directories to avoid a warning in the next step.

In **docs** directory, run:

    make html

This last step is how the documentation hosted on `Read the Docs` is built (see also the configuration file *.readthedocs.yaml*).

## Source 
https://github.com/SAMI-Medical-Physics/glowgreen

## Bug tracker
https://github.com/SAMI-Medical-Physics/glowgreen/issues

## Authors
- Jake Forster (Jake.Forster@sa.gov.au)
- Erin Lukas (Erin.Lukas@sa.gov.au)

## Copyright
`glowgreen` is Copyright (C) 2022, 2023, 2025 South Australia Medical Imaging.

## License
MIT license. See LICENSE file.

## Publishing
`glowgreen` is published on PyPI:

https://pypi.org/project/glowgreen/

See this [tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

## Publications
Papers that use `glowgreen`:
- Forster JC et al. "Close contact restriction periods for patients who have received iodine-131 therapy for differentiated thyroid cancer." J Radiol Prot. 2023;43(2):021501. doi: 10.1088/1361-6498/acc4d0.
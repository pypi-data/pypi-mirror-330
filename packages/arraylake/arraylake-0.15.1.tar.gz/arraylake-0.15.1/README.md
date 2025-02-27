<p align="center">
<img src="https://earthmover-web-assets.s3.amazonaws.com/04-Arraylake-Lockup-Midnight-RGB-LARGE.png" width="80%" alt="Arraylake">
</p>

<p align="center">
  <a href="https://earthmover.io" rel="nofollow">earthmover.io</a> -
  <a href="https://docs.earthmover.io" rel="nofollow">documentation</a>
</p>

Arraylake is a cloud-based platform that understands a wide array of multidimensional scientific data. Organize, analyze, build, and collaborate—effortlessly.

Check out the [documentation](https://docs.earthmover.io) to get started.

## Install

```
# using pip
pip install arraylake

# using conda
conda install arraylake
```

## Using hatch for Project Management

This project uses Hatch for dependency management, virtual environment management, and packaging. For further details, refer to the [official hatch documentation](https://hatch.pypa.io/latest/).

### Prerequisites

Before you can use Hatch with this project, make sure you have the following installed:

- **Python** (version 3.10 or higher)
- **Hatch** (installed via `pip`)

You can install Hatch globally by running:

```bash
pip install hatch
```

Hatch can also be installed via Homebrew:

```bash
brew install hatch
```

### Setting Up the Project
**1. Clone the Repository:**

If you haven't already, clone the arraylake repository to your local machine:

```bash
git clone https://github.com/earth-mover/arraylake.git
cd client
```

** 2. Create a Virtual Environment:**

To create a new environment for the project, run:

```bash
hatch env create
```

This will create a virtual environment with the necessary dependencies based on the project's configuration.

** 3. Install Dependencies:**

After creating the virtual environment, you can install the project’s dependencies by running:

```bash
hatch install
```

This will install the dependencies listed in the pyproject.toml file under [tool.hatch.dependencies].

### Managing Environments
Hatch allows you to manage multiple environments for a project. Here’s how you can work with them:

To create a specific environment, use the following command:

```bash
hatch env create <env_name>
```

To list all available environments:

```bash
hatch env list
```

To activate an environment:

```bash
hatch env use <env_name>
```

To deactivate the current environment:

```bash
hatch env deactivate
```

The following are the available environments for the arraylake client:

* `dev`: Contains the project dependencies (including Zarr v2) and dev dependencies
* `standard`: Contains the project dependencies (including Zarr v2), dev dependencies, and all extras
* `icechunk`: Contains the project dependencies (including Zarr v3), dev dependencies, xarray extras, and icechunk extras
* `minimal`: Contains the minimum versions of the project dependencies (including Zarr v2) and dev dependencies
* `minimal-latest-python`:  Contains the minimum versions of the project dependencies (including Zarr v2), dev dependencies, and `widgets`, `virtual`, `xarray`, and `maximal` extras on Python 3.12.
* `upstream`: Contains all of the upstream versions of the project dependencies (Zarr is pinned to v2), dev dependencies, and all extras
* `performance`: Contains the performance dependencies.


### Versioning and Packaging
We also use Hatch to manage versioning and packaging.

Hatch supports automatic version bumps and is configured to update the version based on the git tags.

To make sure your local build is configured with the correct version, run the following to fetch the latest tags:

```bash
git fetch --tags
```

To build a distributable package (e.g., for PyPI):

```bash
hatch build
```

This will create a `dist/` directory with your package. This will also update the `_version.py` file with the latest tag from git. __Do not commit `_version.py` to git!__

To print out the version to the terminal without modifying the source directory, run:

```bash
hatch version
```

To publish to PyPI:

```bash
hatch publish
```

### Running tests

It is recommended that the `standard` environment be used to run tests.

```bash
hatch -e standard run run-tests
```

Alternatively, run:

```bash
hatch -e standard run pytest -vvv tests/
```

or

```bash
hatch -e standard shell
pytest -vvv tests/
```

To run Icehunk and Zarr v3 specific tests, run:

```bash
hatch -e icechunk run run-tests
```

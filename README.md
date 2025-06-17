# empa-spack

Spack packages of software used or maintained at Empa.

Check out the [wiki](https://github.com/empa-scientific-it/empa-spack/wiki) for more guides and information on how to use this repository.

## Repository structure

This repository must follow the standard Spack repository structure, plus a few additions:
```
repo/
  ├── repo.yaml   # Metadata for the repository
  └── packages/   # Directory containing package recipes
      ├── package1/
      │   └── package.py
      └── package2/
          └── package.py
uenv/
  ├── software_name/   # Root folder for a given uenv
      ├── vX.Y.Z/      # Version folder (semver schema, patch is optional)
          ├── arch/    # Architecture, 'eiger' (zen2) or 'daint' (gh200)
containers/
  ├── software_name/   # Root folder for an image containing the Dockerfile and all its dependencies
  ├── edf/             # Environment Definition File (EDF) required by the Container Engine
                       #   i.e., which image to load, paths to mount, options, etc.
modules/
  ├── software_name/   # Root folder containing Lmod module files (LUA modules)
                       #   for custom software setup (e.g. paths, env variables, etc.)
```

The `repo.yaml` defines the namespace as `empa`:
```yaml
repo:
  namespace: empa
```

The `arch/` subfolder under `uenv` must follow the [directory structure](https://eth-cscs.github.io/stackinator/recipes/) of the `stackinator` tool, to be able to build locally or remotely (with `uenv build`).

## Spack

### Prerequisites

1. Ensure you have Spack installed on your system. Follow the [Spack installation guide](https://spack.readthedocs.io/en/latest/getting_started.html) if needed.
2. Ensure `git` is installed on your system to clone this repository.

### Add this repository

1. **Clone**

Clone the repository to your local system:
```bash
git clone https://github.com/empa-scientific-it/empa-spack.git /path/to/local/repo
```

2. **Add the repository to Spack**

Register the cloned repository with Spack:
```bash
spack repo add --scope site /path/to/local/repo
```

The `--scope site` option will register the repository in `$(prefix)/etc/spack`. Settings saved within the `site` scope affect only *this instance* of Spack and override the defaults and system scopes.

You can confirm that the repository was added successfully by running:
```bash
spack repo list
```
You should see an entry for this repository, followed by the built-in Spack repository (or any other repository previously added).

3. **Check for available packages**

To list all packages provided by this repository, run:
```bash
spack list
```

Packages from this repository will appear with the repository's namespace (e.g., `empa.package-name`).


### Using the custom packages

1. **Search for a package**

You can search for a specific package using:
```bash
spack info package-name
```

2. **Install a package**

Install any package from this repository as you would for any Spack package:
```bash
spack install package-name
```

If you want to make sure to install a package from this specific repository, specify the namespace explicitly:
```bash
spack install empa.package-name
```
> [!IMPORTANT]
> Spack's repos order matters. If you have multiple repositories with the same package, Spack will use the first one in the list.

For example, if your `repos.yaml` file looks like:
```yaml
repos:
  - ~/proto
  - /usr/local/spack
  - $spack/var/spack/repos/builtin
```

The command `spack install hdf5` will install the package from the `~/proto` repository, if available. If not, it will install the package from the `/usr/local/spack` repository, falling back to the built-in Spack repository if necessary, and failing if no repository provides the package.

---

For additional info, refer to the [Spack documentation](https://spack.readthedocs.io).

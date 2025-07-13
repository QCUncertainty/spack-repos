# QCUncertainty Spack Package Repositories

**WARNING:** Under heavy construction and subject to change at any moment. Not ready for use yet!

## Installation

### Spack >=1.0.0:

Spack versions >=1.0.0 support cloning GitHub repositories with potentially multiple Spack repositories inside. This is the easiest method to fetch and add the Spack repositories here.

```bash
# Clone the repo into '~/.spack/package_repos/<hashed_name>'
spack repo add --name qcuncertainty https://github.com/QCUncertainty/spack-repos.git
# Or, to choose the destination
spack repo add --name qcuncertainty https://github.com/QCUncertainty/spack-repos.git <destination>
```

### Spack <1.0.0

In pre-1.0.0 Spack releases, GitHub-hosted package repositories need to be downloaded and added manually.

```bash
# Clone the repo into your <desired_directory>
git clone https://github.com/QCUncertainty/spack-repos.git <desired_directory>

# Add desired QCUncertainty Spack repos
spack repo add <desired_directory>/spack_repo/qcuncertainty/core
spack repo add <desired_directory>/spack_repo/qcuncertainty/overrides
# ... other sub-repos ...
```

## Updating

### Spack >1.0.0

As of Spack v1.0.0, there is no automatic update mechanism for Git-based repos in Spack. They recommend doing so manually with the following commands:

```bash
# Navigate to the repo directory
spack cd --repo qcuncertainty

# Pull the latest changes from GitHub
git pull
# Or checkout a specific commit or version tag
git checkout <commit|tag>
```

NOTE: Spack may have an undocumented update command now. The following worked for me with Spack `1.0.0.dev0 (b63f793f74c672eaf4768b7a5a711c83882bbebd)`:
```bash
spack repo update
```

### Spack <1.0.0

Updating with Spack <1.0.0 is approximately the same as >=1.0.0, and must be done by manually updating the cloned GitHub repository. The following commands will update *all* `qcuncertainty.*` sub-repos at once. You do not need to run this separately for each `qcuncertainty.*` sub-repo!

```bash
# Navigate to the repo directory
# (any qcuncertainty.* sub-repo can be used here in place of qcuncertainty.core)
spack cd --repo qcuncertainty.core

# Pull the latest changes from GitHub
git pull
# Or checkout a specific commit or version tag
git checkout <commit|tag>
```

## Usage

### Namespacing

This GitHub repository provides various package repositories for the QCUncertainty project under an `qcuncertainty` organization-level namespace with the following structure:

```
spack_repo
└── qcuncertainty
    ├── core
    │   ├── packages
    │   │   ├── package_1
    │   │   ├── package_2
    │   │   └── ... more packages ...
    │   └── repo.yaml
    ├── overrides
    │   ├── packages
    │   │   └── ...
    │   └── repo.yaml
    └── another_repo
        ├── packages
        │   └── ...
        └── repo.yaml
```

In Spack, package repositories are namespaced as `qcuncertainty.<sub_repo_name>` and are defined on disk as `spack_repo/qcuncertainty/<sub_repo_name>/`. The current package repositories can be found inside [`spack_subrepo/qcuncertainty/`](https://github.com/QCUncertainty/spack-repos/tree/master/spack_repo/qcuncertainty).

Packages can be distinguished by prefixing the package name with the package repository namespace it is defined in (e.g. `qcuncertainty.repo_a.package_1`). This is useful to determine from which repository a package originated, like to confirm that you are using the correct override of a package. However, in general, namespaces are not needed when identifying a package in a package specification and should be avoided. Spack actually strongly discourages using explicit namespacing in `depends_on()` statements of packages, as "It makes the package non-portable and tightly coupled to a specific repository configuration, hindering sharing and composition of repositories." (see warning at the bottom of Spack's [Search Order and Overriding Packages](https://spack.readthedocs.io/en/latest/repositories.html#search-order-and-overriding-packages)).

### `qcuncertainty.core`

Spack package repository for core (first-party) packages in the QCUncertainty software stack.

### `qcuncertainty.overrides`

Spack package repository to override existing packages for use in QCUncertainty software stack.

For packages in the `qcuncertainty.overrides` repository to work once installed, `qcuncertainty.overrides` must be listed above the repository whose package it is overriding in `repos.yaml` or the `repos:` section of an environment `spack.yaml`. The correct file can be opened for updating with:

```bash
spack config edit repos
```

For more information, see the Spack's [Search Order and Overriding Packages](https://spack.readthedocs.io/en/latest/repositories.html#search-order-and-overriding-packages).

## Helpful Spack Commands

For a broader list of helpful Spack repository management commands, see Spack's [The `spack repo` Command](https://spack.readthedocs.io/en/latest/repositories.html#the-spack-repo-command).

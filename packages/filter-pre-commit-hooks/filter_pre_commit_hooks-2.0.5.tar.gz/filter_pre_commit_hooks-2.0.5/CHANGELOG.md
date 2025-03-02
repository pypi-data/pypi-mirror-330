# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0),
and adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0).

## Unreleased

Nothing.

## [2.0.5](https://github.com/trallnag/filter-pre-commit-hooks/compare/v2.0.4...v2.0.5) / 2025-03-01

### Changed

- Added info about shell completion to documentation.

## [2.0.4](https://github.com/trallnag/filter-pre-commit-hooks/compare/v2.0.3...v2.0.4) / 2025-02-20

### Fixed

- Moved script into proper package called `filter_pre_commit_hooks` and not just
  `src` which should resolve problems with installing in some environments.

## [2.0.3](https://github.com/trallnag/filter-pre-commit-hooks/compare/v2.0.2...v2.0.3) / 2025-02-20

### Fixed

- Properly handle parsing of invalid config instead of bubbling up internal
  exceptions.

## [2.0.2](https://github.com/trallnag/filter-pre-commit-hooks/compare/v2.0.1...v2.0.2) / 2025-02-19

### Changed

- Program is now also available as a package on PyPI. Installed from PyPI, the
  program can be executed with `filter-pre-commit-hooks`.

## [2.0.1](https://github.com/trallnag/filter-pre-commit-hooks/compare/v2.0.0...v2.0.1) / 2025-02-14

### Changed

- Added info about uv and shebang to script help message.

## [2.0.0](https://github.com/trallnag/filter-pre-commit-hooks/compare/v1.1.2...v2.0.0) / 2025-02-11

### Changed

- **BREAKING:** Complete rewrite of the script. It is best to check out the
  README and the help message of the script for more information. The script now
  comes with inline script metadata and with that dependencies on a third-party
  package.

## [1.1.2](https://github.com/trallnag/filter-pre-commit-hooks/compare/v1.1.1...v1.1.2) / 2025-01-22

### Changed

- Simplified code based on feedback from Ruff.

## [1.1.1](https://github.com/trallnag/filter-pre-commit-hooks/compare/v1.1.0...v1.1.1) / 2025-01-05

### Fixed

- Switched minium required version of Python from 3.10 to 3.9.

## [1.1.0](https://github.com/trallnag/filter-pre-commit-hooks/compare/v1.0.0...v1.1.0) / 2025-01-02

### Added

- Ensure that at least one filter is provided to script (in any mode).

## [1.0.0](https://github.com/trallnag/filter-pre-commit-hooks/compare/6014a859fec1b8842ea1dc573e096609e61ceecd...v1.0.0) / 2025-01-01

Initial release.

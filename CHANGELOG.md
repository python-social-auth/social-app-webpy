# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased](https://github.com/python-social-auth/social-app-webpy/commits/master)

### Changed

- Modified model and access code to work with SQLAlchemy version 2 (Issue #1)
- Updated packaging information files per PEP 517, PEP 518 (Issue #2)
- Restricted Python minimum working version to 3.7 or higher to align with SQLAlchemy 2 (Issue #1)
- Fixed behavior of get_current_user function throwing a None error when executed (Issue #3)

## [1.0.0](https://github.com/python-social-auth/social-app-webpy/releases/tag/1.0.0) - 2017-01-22

### Added

- Added partial pipeline db storage solution

### Changed

- Remove usage of set/get current strategy methods
- Allow apps to have any type of user_id field (port of [#1040](https://github.com/omab/python-social-auth/pull/1040)
  by prmtl)

## [0.0.1](https://github.com/python-social-auth/social-app-webpy/releases/tag/0.0.1) - 2016-11-27

### Changed

- Split from the monolitic [python-social-auth](https://github.com/omab/python-social-auth)
  codebase

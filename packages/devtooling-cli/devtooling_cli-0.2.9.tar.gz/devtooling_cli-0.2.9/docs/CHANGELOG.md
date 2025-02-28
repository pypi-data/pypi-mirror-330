
`CHANGELOG.md`:
```markdown
# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.9] - 2024-02-27

### Added
- Added comprehensive test suite:
  - Core tests for ProjectDetector (98% coverage)
  - Feature tests for TreeVisualizer (93% coverage)
  - Configuration tests (90% coverage)
  - Test documentation and coverage tracking
- Added testing documentation and guidelines
- Added testing patterns and best practices

### Changed
- Enhanced configuration system with better testing support
- Improved error handling in core components
- Updated project structure for better testability
- Enhanced mock support for production environment

### Fixed
- Fixed configuration handling in development environment
- Fixed directory structure visualization edge cases
- Fixed project type detection accuracy
- Fixed config path resolution in testing environment

### Testing Coverage
- Core modules: 98% coverage
- Feature modules: 93% coverage
- Utils modules: 65% coverage average
  - config.py: 90% coverage
  - logger.py: 34% coverage
  - updater.py: 36% coverage

### Technical Debt
- Pending CLI argument handler tests (18% coverage)
- Pending UI component tests (0% coverage)
- Pending file handler tests (0% coverage)
- Known issues with production environment mocking

## [0.2.6] - 2024-02-18

### Added
- Added clear configuration command: `devtool projects --clear`
- Added persistent configuration storage using appdirs
- Added automatic config initialization for compiled version

### Changed
- Modified low-level scanning to properly handle nested projects
- Improved configuration file handling in compiled version
- Enhanced project detection to avoid unnecessary deep scanning
- Updated configuration system to use user-specific directories
- Enhanced build process with better dependency handling
- Improved PyInstaller build process

### Fixed
- Fixed configuration persistence in compiled version
- Fixed low-level scanning to properly detect projects in subfolders
- Fixed project detection in complex directory structures
- Fixed PyInstaller build process to include default configuration
- Fixed configuration storage location in compiled executables

## [0.2.5] - 2024-02-17

### Added
- Added projects management system
  - Watch folders for projects detection
  - Support for low-level and deep scanning modes
  - Automatic project type detection in watched folders
  - Project navigation feature with new terminal
  - Projects listing with detailed information

- Added command line interface for projects management:
  - `devtool projects --folders-add PATH [--low-level]`
  - `devtool projects --folders-remove PATH`
  - `devtool projects --list`
  - `devtool projects --refresh-folders`
  - `devtool projects --go PROJECT_NAME`
  - `devtool go PROJECT_NAME` (shortcut command)
  
- Added interactive menu for projects management

### Changed
- Enhanced CLI with better command documentation
- Improved project detection efficiency
- Updated menu structure to include projects management

## [0.2.2] - 2024-02-17

### Added
- Added support for arguments on the command line instead of just having a CLI

### Fixed

- Fixed the structure view on manual mode

## [0.2.1] - 2024-02-16

### Added
- Added build script for PyInstaller

### Changed
- Replaced the use of PyFiglet for an simplified ASCII art banner

## [0.2.0] - 2024-02-16

### Added
- Added support for more frameworks and technologies
- Fully organized project structure
- Added logging system

### Changed
- Replaced the ignore_rules.json file with a more flexible configuration in detection_rules.json
- Changed the menu options to allow more functionalities in the future
- Replaced the FileIgnorer file with a more flexible ProjectDetector

### Fixed
- Fixed the detection of simultaneous project types
- Fixed the detection of nested projects
- Fixed the manage of invalid routes
- Fixed the visualization of directory structure (After the CLI was reset before of generate the structure)
- Other minor fixes and improvements

## [0.1.0] - 2024-02-02

### Added
- Base system of project detection
- Visualization of directory structure
- Improved JSON configuration
- Intelligent detection of project types
- Command-line basic interface

### Changed
- Improved the project detection logic
- Optimized the ignore directories system

### Fixed
- Fixed the detection of nested projects
- Fixed the manage of invalid routes

## [0.1.0] - 2024-02-01

### Added
- Initial project structure
- Basic detection system
- JSON Configuration files
- Initial documentation
- Basic CLI interface

### Changed
- Reorganized project structure
- Improved logging system

## Type of changes
- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.
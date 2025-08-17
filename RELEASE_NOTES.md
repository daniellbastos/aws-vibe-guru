# Release Notes

## [0.0.1] - 2024-02-16

First release of AWS Toolbelt, a CLI tool for AWS metrics extraction and resource management.

### Added

#### Core Features
- Basic CLI structure using Typer and Rich
- AWS credentials handling (file and environment variables)
- Comprehensive documentation (README, ROADMAP)
- Development tools setup (UV, Ruff, pytest)

#### SQS Commands
- `sqs-list-queues`: List queues with optional name filtering
- `sqs-get-attributes`: Get queue attributes in a friendly format
- `sqs-get-metrics`: Get message volume metrics with ASCII charts
  - Daily message volume tracking
  - Customizable time range (--days option)
  - ASCII bar chart visualization
  - Friendly number formatting
- `sqs-get-oldest-message`: Monitor oldest message age
  - Current and historical age tracking
  - Maximum age in period
  - Hourly breakdown

#### Development Features
- Makefile for common development tasks
- Ruff configuration for linting and formatting
- VS Code integration
- Test infrastructure with pytest
- AWS mocking with moto

### Technical Details

#### Dependencies
- Python >=3.8.1
- boto3 for AWS integration
- Typer for CLI framework
- Rich for terminal formatting
- UV for package management
- Ruff for linting/formatting
- pytest and moto for testing

#### Configuration
- AWS credentials via `~/.aws/credentials` or environment variables
- VS Code settings for development
- Ruff rules for code quality

### Documentation
- README.md with installation and usage instructions
- ROADMAP.md with development plans
- Inline documentation and docstrings
- Type hints via docstrings

### Notes
- This is the initial release focusing on SQS metrics
- Future releases will add more AWS services and features
- Feedback and contributions are welcome

### Contributors
- Daniel Bastos (@daniellbastos)
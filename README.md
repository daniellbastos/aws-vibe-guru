# AWS Vibe Guru 🔧

A powerful command-line interface (CLI) tool for managing AWS resources and extracting metrics. Currently supports Amazon SQS queue monitoring and Amazon S3 bucket operations.

## ✨ Quick Overview

**AWS Vibe Guru** provides intuitive commands to interact with AWS services directly from your terminal, with beautiful visual output and comprehensive analytics.

### Current Features

- **📊 SQS Monitoring**: Queue management, message volume tracking, age monitoring, and advanced analytics
- **📦 S3 Operations**: Bucket management, object listing, file reading with JSON formatting
- **🎨 Beautiful Output**: Rich terminal formatting with colors, charts, and panels
- **📈 Analytics**: Statistical analysis with charts, trends, and comparisons

## 🚀 Quick Start

### Installation

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone https://github.com/daniellbastos/aws-vibe-guru.git
cd aws-vibe-guru
uv sync
```

### Basic Usage

```bash
aws-vibe-guru sqs-list-queues
aws-vibe-guru sqs-analyze-volume "my-queue" --days 30

aws-vibe-guru s3-list-buckets
aws-vibe-guru s3-read-object "my-bucket" "config.json" --json
```

### AWS Credentials

Configure credentials via `~/.aws/credentials` file or environment variables:

```bash
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_DEFAULT_REGION="us-east-1"
```

## 📚 Complete Documentation

For detailed information about all commands, parameters, return values, and examples:

**👉 [Read the Full Technical Reference](docs/REFERENCE.md)**

The reference documentation includes:
- All 9 available commands (5 SQS + 4 S3)
- Detailed parameter descriptions
- Usage examples for each command
- Return value structures
- AWS permissions required
- Configuration guide

## 📋 Available Commands

### SQS Commands
- `sqs-list-queues` - List all SQS queues with optional filtering
- `sqs-get-attributes` - Get comprehensive queue attributes
- `sqs-get-metrics` - Get message volume metrics with charts
- `sqs-get-oldest-message` - Monitor oldest message age
- `sqs-analyze-volume` - Advanced statistical analysis

### S3 Commands
- `s3-list-buckets` - List all S3 buckets
- `s3-list-objects` - List objects in a bucket (with prefix filter and summary mode)
- `s3-get-object` - Get detailed object information
- `s3-read-object` - Read and display file content (with JSON formatting)

Run `aws-vibe-guru --help` to see all available commands.

## 🎥 Demo

https://github.com/user-attachments/assets/1ad28f09-05c4-4dc6-b2ef-9e174da47b08

## 🛠️ Development

```bash
git clone https://github.com/daniellbastos/aws-vibe-guru.git
cd aws-vibe-guru
uv sync --extra dev
make pre-commit-install
make quality
```

### Development Commands
- `make quality` - Run linting and formatting
- `make lint` - Check code with Ruff
- `make format` - Format code with Ruff

## 📦 Requirements

- Python 3.8.1 or higher
- AWS credentials configured
- UV package manager (recommended)

## 🙏 Built With

- [boto3](https://boto3.amazonaws.com/) - AWS SDK for Python
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [UV](https://github.com/astral-sh/uv) - Package manager
- [Ruff](https://github.com/astral-sh/ruff) - Linter and formatter

## 📄 Documentation & Release Notes

- **[Technical Reference](docs/REFERENCE.md)** - Complete command documentation
- **[Release Notes](RELEASE_NOTES.md)** - Version history and features

## 📄 License

MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Repository](https://github.com/daniellbastos/aws-vibe-guru)
- [Issues](https://github.com/daniellbastos/aws-vibe-guru/issues)

---

**Made with ❤️**

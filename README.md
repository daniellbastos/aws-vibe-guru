# AWS Vibe Guru 🔧

A command-line interface (CLI) tool for extracting AWS metrics and managing cloud resources. Initially focused on Amazon SQS queue monitoring.

## 🚀 Features

### 📊 SQS Monitoring & Analysis
- **Queue Management**: List and filter SQS queues
- **Attribute Analysis**: Get comprehensive queue attributes
- **Message Volume Tracking**: Monitor message volume with beautiful ASCII charts
- **Age Monitoring**: Track oldest message age over time
- **Advanced Analytics**: Statistical analysis with mean, median, and percentage comparisons
- **Multi-Queue Support**: Analyze multiple queues simultaneously

### 🎨 Visual Enhancements
- **Rich Terminal Output**: Beautiful colors, panels, and formatting
- **ASCII Charts**: Dynamic bar charts for data visualization
- **Day-of-Week Indicators**: `[Mon] 2024-01-01: 1,200 messages`
- **Formatted Numbers**: Thousands separators for readability
- **Color-coded Output**: Consistent color scheme throughout
- **Peak Day Highlighting**: Top 3 days marked with asterisk (*) for easy identification

### 🛠️ Development Features
- **Pre-commit Hooks**: Automated code quality checks
- **Comprehensive Testing**: Full test suite with AWS mocking
- **Modern Tooling**: UV package manager, Ruff linting/formatting
- **Type Safety**: Complete type annotations
- **Documentation**: Detailed help and usage examples

## 📋 Requirements

- Python 3.8.1 or higher
- UV package manager (recommended)
- AWS credentials configured (either in `~/.aws/credentials` or environment variables)

## 🛠️ Installation

### Using UV (Recommended)

```bash
# Install UV if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/daniellbastos/aws-vibe-guru.git
cd aws-vibe-guru

# Install dependencies
uv sync
```

## 🚀 Usage

### 📋 Available Commands

```bash
# List SQS queues
aws-vibe-guru sqs-list-queues
aws-vibe-guru sqs-list-queues --name "prod-"

# Get queue attributes
aws-vibe-guru sqs-get-attributes "my-queue"

# Get message volume metrics (with ASCII chart)
aws-vibe-guru sqs-get-metrics "my-queue"
aws-vibe-guru sqs-get-metrics "my-queue" --days 30

# Get oldest message age
aws-vibe-guru sqs-get-oldest-message "my-queue"
aws-vibe-guru sqs-get-oldest-message "my-queue" --days 14

# Advanced volume analysis
aws-vibe-guru sqs-analyze-volume "my-queue"
aws-vibe-guru sqs-analyze-volume "queue1" "queue2" "queue3"
aws-vibe-guru sqs-analyze-volume "my-queue" --days 60
```

### 📊 Example Output

```
Queue: my-queue
───────

Total messages received: 15,420

Daily breakdown (top 3 days highlighted):
[Mon] 2024-01-01: 1,200 messages
[Tue] 2024-01-02: 1,350 messages
[Wed] 2024-01-03: 1,800 messages *

Message Volume Chart:
   1,800 ┬  █
   1,440 ┤  █
   1,080 ┤  █       █
    720 ┤  █       █
    360 ┤  █       █
      0 ┴  █       █
         01-01   01-02   01-03

Volume Analysis:
• Peak Volume Day:
  - Date: 2024-01-03
  - Volume: 1,800 messages
• Comparison with Mean:
  - Mean Volume: 1,450 messages
  - Percentage Above Mean: 24.1%
```

### AWS Credentials

The tool supports two ways to provide AWS credentials:

1. **AWS Credentials File** (`~/.aws/credentials`):
   ```ini
   [default]
   aws_access_key_id = your_access_key
   aws_secret_access_key = your_secret_key
   region = us-east-1
   ```

2. **Environment Variables**:
   ```bash
   export AWS_ACCESS_KEY_ID="your_access_key"
   export AWS_SECRET_ACCESS_KEY="your_secret_key"
   export AWS_DEFAULT_REGION="us-east-1"
   ```

### Project Structure

```
aws-vibe-guru/
├── src/aws_vibe_guru/
│   ├── __init__.py          # Version and author information
│   ├── cli.py               # Main CLI with all commands
│   ├── cli_helpers.py       # Helpers for Rich formatting
│   ├── aws_sqs.py           # AWS SQS functions and metrics
├── tests/
│   └── __init__.py
├── Makefile                 # Development commands
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## 🛠️ Development

### 🛠️ Development

#### Quick Start
```bash
# Clone and setup
git clone https://github.com/daniellbastos/aws-vibe-guru.git
cd aws-vibe-guru
uv sync --extra dev
make pre-commit-install

# Check code quality
make quality
```

#### Development Commands
```bash
# Install dependencies
uv sync --extra dev

# Check code quality
make quality      # Run linting and formatting
make lint         # Check code with Ruff
make format       # Format code with Ruff

# Install pre-commit hooks
make pre-commit-install

# Run pre-commit manually
make pre-commit-run
```

### Code Quality

This project uses **Ruff** for linting and formatting, which is fast and modern:

```bash
# Check code quality
make lint           # Run linter
make format         # Format code
make quality        # Run both lint and format

# Development helpers
make install-dev    # Install dev dependencies
make clean         # Clean cache files
```

## 📚 Documentation

- [RELEASE_NOTES.md](RELEASE_NOTES.md) - Detailed release notes and features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Technologies Used

- [boto3](https://boto3.amazonaws.com/) - AWS SDK for Python
- [Typer](https://typer.tiangolo.com/) - Framework for building CLIs
- [Rich](https://rich.readthedocs.io/) - Rich text and beautiful formatting in the terminal
- [UV](https://github.com/astral-sh/uv) - Fast Python package manager
- [Ruff](https://github.com/astral-sh/ruff) - Fast Python linter and formatter

## 🔗 Links

- [Repository](https://github.com/daniellbastos/aws-vibe-guru)
- [Issues](https://github.com/daniellbastos/aws-vibe-guru/issues)

---

**Made with ❤️ as a vibe coding test**

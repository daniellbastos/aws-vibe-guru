# AWS Toolbelt 🔧

A command-line interface (CLI) tool for extracting AWS metrics and managing cloud resources. Initially focused on Amazon SQS queue monitoring.

## 🚀 Current Features

- **Basic CLI**: Command-line interface with colorful output using Rich
- **Hello Command**: Example command to test the CLI
- **AWS SQS Commands**:
  - List queues with optional name filtering
  - Get queue attributes in a friendly format
  - Get message volume metrics with ASCII charts
  - Monitor oldest message age
- **AWS Base**: Base structure for AWS services integration using boto3
- **Extensible Architecture**: Ready to add support for other AWS services

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
git clone https://github.com/daniellbastos/aws-toolbelt.git
cd aws-toolbelt

# Install dependencies
uv sync
```

## 🚀 Current Usage

### Available Commands

```bash
# Hello command (for testing)
uv run python -m aws_toolbelt.cli
# Or using the Makefile
make hello

# Hello command with custom name
uv run python -m aws_toolbelt.cli --name "Developer"
# or
make hello-name

# List SQS queues
uv run python -m aws_toolbelt.cli sqs-list-queues
# List queues with name prefix
uv run python -m aws_toolbelt.cli sqs-list-queues --name "dev-"

# Get queue attributes
uv run python -m aws_toolbelt.cli sqs-get-attributes "queue-name"

# Get queue message volume metrics (with ASCII chart)
uv run python -m aws_toolbelt.cli sqs-get-metrics "queue-name"
# Get metrics for a specific period
uv run python -m aws_toolbelt.cli sqs-get-metrics "queue-name" --days 14

# Get oldest message age metrics
uv run python -m aws_toolbelt.cli sqs-get-oldest-message "queue-name"
# Get age metrics for a specific period
uv run python -m aws_toolbelt.cli sqs-get-oldest-message "queue-name" --days 14
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
aws-toolbelt/
├── src/aws_toolbelt/
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

### How to Contribute

1. **Clone the repository**:
   ```bash
   git clone https://github.com/daniellbastos/aws-toolbelt.git
   cd aws-toolbelt
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Test your changes**:
   ```bash
   # Basic commands
   make hello
   uv run python -m aws_toolbelt.cli --name "Test"

   # SQS commands
   uv run python -m aws_toolbelt.cli sqs-list-queues
   uv run python -m aws_toolbelt.cli sqs-get-metrics "your-queue-name"
   ```

4. **Make your changes and test**

5. **Check code quality**:
   ```bash
   make quality      # Run linting and formatting
   make lint         # Check code with Ruff
   make format       # Format code with Ruff
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

### Next Development Steps

See the `ROADMAP.md` file for details about the next planned features.

## 📚 Documentation

- [ROADMAP.md](ROADMAP.md) - Project roadmap and planned features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Technologies Used

- [boto3](https://boto3.amazonaws.com/) - AWS SDK for Python
- [Typer](https://typer.tiangolo.com/) - Framework for building CLIs
- [Rich](https://rich.readthedocs.io/) - Rich text and beautiful formatting in the terminal
- [UV](https://github.com/astral-sh/uv) - Fast Python package manager
- [Ruff](https://github.com/astral-sh/ruff) - Fast Python linter and formatter

## 🔗 Links

- [Repository](https://github.com/daniellbastos/aws-toolbelt)
- [Issues](https://github.com/daniellbastos/aws-toolbelt/issues)

---

**Made with ❤️**

# Release Notes

## [0.1.1] - 2025-10-01

### 🆕 New Features

#### S3 Folder Reading Command
- **`s3-read-folder`**: New command to read all files from a folder in S3 bucket
- **Batch File Display**: Shows header with folder path and total files count
- **Simplified Output**: Lists each file with full path + content in a clean format
- **JSON Formatting**: Support for `--json` flag to format JSON content with 2-space indentation
- **Encoding Support**: Configurable text encoding with `--encoding` parameter
- **Limit Control**: Optional `--max` parameter to limit number of files to read
- **Binary Detection**: Automatically detects and skips binary files
- **Error Handling**: Continues reading even if individual files fail

### 🐛 Bug Fixes

#### S3 Pagination Fix
- **Fixed Critical Pagination Bug**: Resolved issue where `list_bucket_objects` was not paginating correctly through all S3 objects
- **Root Cause**: The function was using `MaxKeys` incorrectly, causing it to stop after the first page of results
- **Impact**: Files in subsequent pages were not being found or listed
- **Solution**: Implemented proper pagination logic that iterates through all pages regardless of total object count

### 🔧 Technical Improvements

#### Unlimited Results by Default
- **`s3-list-objects`**: Changed default `max_results` from 1000 to unlimited
- **`s3-read-object`**: Removed 100-object limit when using `--prefix` search
- **`s3-read-folder`**: Changed default `max_files` from 100 to unlimited
- **User Control**: Users can still limit results using `--max` parameter when needed
- **Performance**: Uses S3's optimal page size of 1000 objects per request

#### Pagination Logic
- **New `list_bucket_objects` Behavior**:
  - No longer sets `MaxKeys` in API request (uses S3 default of 1000 per page)
  - Properly iterates through all pages using `ContinuationToken`
  - Only applies `max_keys` limit after collecting objects
  - Checks limit both within pages and between pages

### 📚 Documentation Updates
- Updated help text for all S3 commands to reflect "unlimited" default behavior
- Added examples for `s3-read-folder` command usage
- Updated technical documentation with new command details

---

## [0.0.2] - 2024-12-19

### 🎯 New Features

#### Peak Day Highlighting
- **Top 3 Days Highlighting**: Daily breakdown now highlights the top 3 days with highest message volume using asterisk (*)
- **Improved User Experience**: Easier identification of peak days in volume analysis
- **Enhanced Visual Feedback**: Clear visual distinction for high-volume days

### 🔧 Technical Improvements
- **Code Organization**: Moved datetime import to top of file for better organization
- **Function Enhancement**: Added `number_of_days_to_highlight` parameter to `create_daily_breakdown` function
- **Reusable Feature**: Highlighting functionality can be customized for different use cases

---

## [0.0.1] - 2024-12-19

First stable release of AWS Vibe Guru, a comprehensive CLI tool for AWS metrics extraction and resource management with focus on SQS monitoring and analysis.

### 🚀 Core Features

#### CLI Framework
- **Typer-based CLI**: Modern command-line interface with auto-completion
- **Rich Integration**: Beautiful terminal output with colors, panels, and formatting
- **Help System**: Comprehensive help documentation with usage examples
- **Error Handling**: Graceful error handling with user-friendly messages

#### AWS Integration
- **Credentials Management**: Support for AWS credentials file and environment variables
- **boto3 Integration**: Full AWS SDK integration for service access
- **CloudWatch Metrics**: Automated metrics collection and analysis
- **Multi-Region Support**: Configurable AWS region support

### 📊 SQS Commands

#### `sqs-list-queues`
- List all SQS queues with optional name filtering
- Display queue names and URLs
- Support for prefix-based filtering
- Clean, formatted output

#### `sqs-get-attributes`
- Get comprehensive queue attributes in friendly format
- Display queue configuration details
- Support for FIFO and standard queues
- Formatted attribute presentation

#### `sqs-get-metrics`
- **Message Volume Analysis**: Track daily message volume with customizable time range
- **ASCII Charts**: Beautiful bar chart visualization of message trends
- **Daily Breakdown**: Detailed daily statistics with day-of-week indicators
- **Total Statistics**: Summary of total messages received
- **Customizable Periods**: Configurable analysis periods (default: 7 days)

#### `sqs-get-oldest-message`
- **Age Monitoring**: Track oldest message age over time
- **Historical Analysis**: Compare current vs. historical maximum ages
- **Time-based Tracking**: Monitor age trends with customizable periods
- **Formatted Output**: Human-readable age formatting (days, hours, minutes)

#### `sqs-analyze-volume`
- **Advanced Volume Analysis**: Comprehensive volume trend analysis
- **Statistical Comparisons**: Mean, median, and peak volume analysis
- **Percentage Analysis**: Detailed percentage-based comparisons
- **Multi-Queue Support**: Analyze multiple queues simultaneously
- **Visual Charts**: ASCII bar charts for each queue
- **Daily Breakdown**: Detailed daily statistics with day-of-week indicators

### 🎨 Visual Enhancements

#### Chart System
- **ASCII Bar Charts**: Beautiful terminal-based chart visualization
- **Dynamic Scaling**: Automatic chart scaling for large numbers
- **Centered Bars**: Properly centered bar alignment
- **Large Number Support**: Handles numbers >1M without alignment issues

#### Text Formatting
- **Styled Text Class**: Custom Text class with default styling
- **Panel System**: Custom Panel class for consistent UI
- **Color Coding**: Consistent color scheme throughout the application
- **Rich Formatting**: Professional terminal output

### 🛠️ Development Features

#### Code Quality
- **Pre-commit Hooks**: Automated code quality checks before commits
- **Ruff Integration**: Fast linting and formatting with Ruff
- **Type Hints**: Comprehensive type annotations
- **Documentation**: Detailed docstrings with usage examples

#### Testing
- **pytest Framework**: Comprehensive test suite
- **AWS Mocking**: Mocked AWS services for testing
- **Test Coverage**: High test coverage for core functionality

#### Development Tools
- **UV Package Manager**: Fast Python package management
- **Makefile**: Convenient development commands
- **VS Code Integration**: Optimized development environment
- **Git Hooks**: Automated quality checks

### 📋 Technical Details

#### Dependencies
- **Python >=3.8.1**: Modern Python support
- **boto3 >=1.26.0**: AWS SDK integration
- **typer >=0.9.0**: CLI framework
- **rich >=13.0.0**: Terminal formatting
- **ruff >=0.1.0**: Linting and formatting
- **pytest >=7.0.0**: Testing framework

#### Configuration
- **AWS Credentials**: File-based (`~/.aws/credentials`) or environment variables
- **Region Support**: Configurable AWS regions
- **Error Handling**: Graceful error handling with user feedback

### 📚 Documentation

#### Command Examples
```bash
# List all queues
aws-vibe-guru sqs-list-queues

# List queues with prefix
aws-vibe-guru sqs-list-queues --name "prod-"

# Get queue attributes
aws-vibe-guru sqs-get-attributes "my-queue"

# Get metrics for last 7 days (default)
aws-vibe-guru sqs-get-metrics "my-queue"

# Get metrics for last 30 days
aws-vibe-guru sqs-get-metrics "my-queue" --days 30

# Get oldest message age
aws-vibe-guru sqs-get-oldest-message "my-queue"

# Analyze volume for single queue
aws-vibe-guru sqs-analyze-volume "my-queue"

# Analyze multiple queues
aws-vibe-guru sqs-analyze-volume "queue1" "queue2" "queue3"

# Analyze with custom period
aws-vibe-guru sqs-analyze-volume "my-queue" --days 60
```

#### Output Features
- **Day-of-Week Indicators**: `[Mon] 2024-01-01: 1,200 messages`
- **Formatted Numbers**: Thousands separators for readability
- **Color-coded Output**: Consistent color scheme
- **ASCII Charts**: Visual representation of data trends
- **Statistical Analysis**: Mean, median, and percentage comparisons

### 🔧 Development Commands

```bash
# Install dependencies
uv sync --extra dev

# Run tests
make test

# Check code quality
make quality

# Format code
make format

# Install pre-commit hooks
make pre-commit-install
```

### 🎯 Key Improvements

#### Code Organization
- **Modular Architecture**: Well-organized, maintainable code structure
- **Reusable Components**: Shared utilities for charts and formatting
- **Consistent Patterns**: Standardized coding patterns throughout
- **Clean Imports**: Organized and efficient import structure

#### User Experience
- **Comprehensive Help**: Detailed help documentation for all commands
- **Usage Examples**: Practical examples for all features
- **Error Messages**: Clear, actionable error messages
- **Visual Feedback**: Rich, informative terminal output

#### Performance
- **Efficient AWS Calls**: Optimized CloudWatch API usage
- **Fast Processing**: Quick data processing and visualization
- **Memory Efficient**: Optimized memory usage for large datasets

### 🚀 Future Roadmap

- **Additional AWS Services**: Support for more AWS services
- **Export Features**: Data export to various formats
- **Real-time Monitoring**: Live monitoring capabilities
- **Advanced Analytics**: More sophisticated analysis features
- **Plugin System**: Extensible plugin architecture

### 📄 License

This project is licensed under the MIT License.

### 👥 Contributors

- **Daniel Bastos** (@daniellbastos) - Lead Developer

---

**AWS Toolbelt** - Making AWS monitoring simple and beautiful! 🎉

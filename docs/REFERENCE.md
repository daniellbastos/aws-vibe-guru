# AWS Vibe Guru - Technical Reference

## Overview

**AWS Vibe Guru** is a Python CLI tool for extracting metrics and managing AWS resources. Currently supports Amazon SQS queue monitoring and Amazon S3 bucket management, providing visual analytics and detailed statistics through the terminal.

### Core Technologies
- **boto3**: AWS SDK for Python
- **Typer**: CLI framework
- **Rich**: Terminal formatting and visualization
- **CloudWatch**: AWS metrics collection

## Project Structure

```
src/aws_vibe_guru/
├── __init__.py          # Version and metadata
├── cli.py               # CLI commands (user interface)
├── cli_helpers.py       # Formatting helper functions
├── aws_sqs.py           # AWS SQS and metrics functions
└── aws_s3.py            # AWS S3 functions
```

### Modules

#### `aws_sqs.py`
Contains core functions for interacting with AWS SQS and CloudWatch:
- `read_aws_credentials()`: Reads AWS credentials
- `create_sqs_connection()`: Creates SQS connection
- `list_sqs_queues()`: Lists SQS queues
- `get_queue_attributes()`: Gets queue attributes
- `get_queue_metrics()`: Gets CloudWatch metrics
- `get_queue_oldest_message()`: Gets oldest message age
- `analyze_queue_volume()`: Analyzes volume trends

#### `aws_s3.py`
Contains core functions for interacting with AWS S3:
- `create_s3_connection()`: Creates S3 connection
- `list_buckets()`: Lists all S3 buckets
- `list_bucket_objects()`: Lists objects in a bucket with pagination
- `get_object_info()`: Gets detailed object information
- `read_object_content()`: Reads and decodes object content
- `read_folder_contents()`: Reads all files from a folder

#### `cli_helpers.py`
Formatting and visualization functions:
- `create_daily_breakdown()`: Creates formatted daily breakdown
- `create_bar_chart()`: Creates ASCII charts
- `Text`: Class for formatted text
- `Panel`: Class for formatted panels

#### `cli.py`
Defines available CLI commands for users.

## Available Commands

### SQS Commands

### 1. `sqs-list-queues`

**Description**: Lists all SQS queues available in the AWS account.

**Usage**:
```bash
aws-vibe-guru sqs-list-queues
aws-vibe-guru sqs-list-queues --name "prod-"
aws-vibe-guru sqs-list-queues -n "dev-"
```

**Parameters**:
- `--name, -n` (optional): Prefix to filter queues by name

**Return**:
- List of queues containing:
  - `name`: Queue name
  - `url`: Full queue URL

**Example Output**:
```
Name: production-orders-queue
URL: https://sqs.us-east-1.amazonaws.com/123456789/production-orders-queue

Name: production-notifications-queue
URL: https://sqs.us-east-1.amazonaws.com/123456789/production-notifications-queue
```

---

### 2. `sqs-get-attributes`

**Description**: Gets all configuration attributes of a specific queue.

**Usage**:
```bash
aws-vibe-guru sqs-get-attributes "my-queue"
aws-vibe-guru sqs-get-attributes "my-fifo-queue.fifo"
```

**Parameters**:
- `queue_name` (required): Queue name

**Return**:
Dictionary with queue attributes:
- `Created`: Creation timestamp
- `Messages Available`: Number of available messages
- `Messages In Flight`: Messages being processed
- `Messages Delayed`: Messages with delay
- `Message Retention Period (days)`: Retention period
- `Maximum Message Size (KB)`: Maximum message size
- `Visibility Timeout (seconds)`: Visibility timeout
- `Receive Message Wait Time (seconds)`: Wait time to receive messages
- `Dead Letter Target`: DLQ configuration
- `KMS Master Key`: Encryption key
- `Content Based Deduplication`: Content-based deduplication
- `FIFO Queue`: Whether it's a FIFO queue
- `Policy`: Access policy

**Example Output**:
```
Created: 1640995200
Messages Available: 150
Messages In Flight: 5
Messages Delayed: 0
Message Retention Period (days): 4.0
Maximum Message Size (KB): 256.0
Visibility Timeout (seconds): 30
Receive Message Wait Time (seconds): 0
Dead Letter Target: None
FIFO Queue: False
```

---

### 3. `sqs-get-metrics`

**Description**: Gets CloudWatch message volume metrics with ASCII chart visualization.

**Usage**:
```bash
aws-vibe-guru sqs-get-metrics "my-queue"
aws-vibe-guru sqs-get-metrics "my-queue" --days 14
aws-vibe-guru sqs-get-metrics "my-queue" -d 30
```

**Parameters**:
- `queue_name` (required): Queue name
- `--days, -d` (optional, default=7): Number of days for analysis

**Return**:
Dictionary containing:
- `queue_name`: Queue name
- `metric`: Metric name (NumberOfMessagesReceived)
- `period`: Analyzed period
- `total`: Total messages received
- `daily_data`: List of dictionaries with:
  - `date`: Date in YYYY-MM-DD format
  - `value`: Number of messages

**Example Output**:
```
Total messages received: 15,420

Daily breakdown:
[Mon] 2024-01-01: 1,200 messages
[Tue] 2024-01-02: 1,350 messages
[Wed] 2024-01-03: 1,800 messages

Message Volume Chart:
   1,800 ┬  █
   1,440 ┤  █
   1,080 ┤  █       █
    720 ┤  █       █
    360 ┤  █       █
      0 ┴  █       █
         01-01   01-02   01-03
```

---

### 4. `sqs-get-oldest-message`

**Description**: Monitors the oldest message age in the queue over time.

**Usage**:
```bash
aws-vibe-guru sqs-get-oldest-message "my-queue"
aws-vibe-guru sqs-get-oldest-message "my-queue" --days 14
aws-vibe-guru sqs-get-oldest-message "my-queue" -d 1
```

**Parameters**:
- `queue_name` (required): Queue name
- `--days, -d` (optional, default=7): Number of days for analysis

**Return**:
Dictionary containing:
- `queue_name`: Queue name
- `metric`: Metric name (ApproximateAgeOfOldestMessage)
- `period`: Analyzed period
- `current_max_age`: Current oldest message age (formatted)
- `period_max_age`: Maximum age in period (formatted)
- `hourly_data`: List of hourly measurements with:
  - `timestamp`: Measurement date and time
  - `age`: Oldest message age

**Age Format**:
- `Xd Yh Zm`: X days, Y hours, Z minutes
- `Xh Ym`: X hours, Y minutes
- `Xm`: X minutes

**Example Output**:
```
Summary:
Current oldest message age: 2h 15m
Maximum age in period: 5d 3h 42m
```

---

### 5. `sqs-analyze-volume`

**Description**: Advanced message volume analysis with comparative statistics. Supports simultaneous analysis of multiple queues.

**Usage**:
```bash
aws-vibe-guru sqs-analyze-volume "my-queue"
aws-vibe-guru sqs-analyze-volume "queue1" "queue2" "queue3"
aws-vibe-guru sqs-analyze-volume "my-queue" --days 30
aws-vibe-guru sqs-analyze-volume "prod-queue" "dev-queue" -d 60
```

**Parameters**:
- `queue_names` (required): List of queue names
- `--days, -d` (optional, default=15): Number of days for analysis

**Return**:
For each queue, dictionary containing:
- `daily_data`: Daily volume data
- `max_volume_day`: Date of highest volume day
- `max_volume`: Maximum recorded volume
- `second_max_day`: Date of second highest volume
- `second_max_volume`: Second highest volume
- `volume_difference`: Difference between 1st and 2nd places
- `volume_increase_percent`: Percentage increase
- `mean_volume`: Mean volume for the period
- `mean_difference`: Peak difference from mean
- `mean_increase_percent`: Percentage above mean
- `median_volume`: Median volume
- `median_difference`: Peak difference from median
- `median_increase_percent`: Percentage above median

**Example Output**:
```
Queue: production-orders
───────────────────────

Total messages received: 45,600

Daily breakdown (top 3 days highlighted):
[Mon] 2024-01-01: 2,400 messages
[Tue] 2024-01-02: 3,200 messages *
[Wed] 2024-01-03: 3,800 messages *
[Thu] 2024-01-04: 2,100 messages
[Fri] 2024-01-05: 4,200 messages *

Message Volume Chart:
   4,200 ┬        █
   3,360 ┤    █   █
   2,520 ┤█   █   █
   1,680 ┤█   █   █
    840 ┤█   █   █
      0 ┴█   █   █
        01-01  01-03  01-05

Volume Analysis:
• Peak Volume Day:
  - Date: 2024-01-05
  - Volume: 4,200 messages

• Comparison with Second Highest:
  - Second Highest Day: 2024-01-03
  - Second Highest Volume: 3,800 messages
  - Volume Difference: +400 messages
  - Percentage Increase: 10.5%

• Comparison with Mean:
  - Mean Volume: 3,060 messages
  - Difference from Mean: +1,140 messages
  - Percentage Above Mean: 37.3%

• Comparison with Median:
  - Median Volume: 2,900 messages
  - Difference from Median: +1,300 messages
  - Percentage Above Median: 44.8%
```

---

## S3 Commands

### 6. `s3-list-buckets`

**Description**: Lists all S3 buckets in the AWS account.

**Usage**:
```bash
aws-vibe-guru s3-list-buckets
```

**Parameters**:
- None

**Return**:
- List of buckets containing:
  - `name`: Bucket name
  - `creation_date`: Bucket creation date and time

**Example Output**:
```
Total buckets: 3

Name: my-production-bucket
Created: 2023-05-15 14:32:18 UTC

Name: my-staging-bucket
Created: 2023-06-20 10:15:45 UTC

Name: my-logs-bucket
Created: 2023-08-01 08:22:33 UTC
```

---

### 7. `s3-list-objects`

**Description**: Lists all objects in a specific S3 bucket with optional prefix filtering.

**Usage**:
```bash
aws-vibe-guru s3-list-objects "my-bucket"
aws-vibe-guru s3-list-objects "my-bucket" --prefix "logs/"
aws-vibe-guru s3-list-objects "my-bucket" -p "data/2024/"
aws-vibe-guru s3-list-objects "my-bucket" --max 500
aws-vibe-guru s3-list-objects "my-bucket" -m 100
aws-vibe-guru s3-list-objects "my-bucket" --prefix "reports/" --max 50
aws-vibe-guru s3-list-objects "my-bucket" --summary
aws-vibe-guru s3-list-objects "my-bucket" -s
```

**Parameters**:
- `bucket_name` (required): Bucket name
- `--prefix, -p` (optional): Filter objects by prefix (file path)
- `--max, -m` (optional, default=unlimited): Maximum number of objects to return
- `--summary, -s` (optional, default=False): Show only summary information (bucket, filter, total)

**Return**:
Dictionary containing:
- `bucket_name`: Bucket name
- `prefix`: Applied prefix filter or "all"
- `total_objects`: Total number of objects found
- `objects`: List of objects with:
  - `key`: Object key (path)
  - `size`: Size in bytes
  - `size_mb`: Size in MB (formatted)
  - `last_modified`: Last modification timestamp
  - `storage_class`: Storage class (STANDARD, GLACIER, etc.)

**Example Output (Full)**:
```
Bucket: my-production-bucket
Filter: logs/
Total objects: 45

Objects:

Key: logs/2024-01-01.log
Size: 2,456,789 bytes (2.34 MB)
Last Modified: 2024-01-01 23:59:45 UTC
Storage Class: STANDARD

Key: logs/2024-01-02.log
Size: 1,234,567 bytes (1.18 MB)
Last Modified: 2024-01-02 23:59:45 UTC
Storage Class: STANDARD
```

**Example Output (Summary Mode)**:
```
Bucket: my-production-bucket
Filter: logs/
Total objects: 45
```

---

### 8. `s3-get-object`

**Description**: Gets detailed information about a specific object in an S3 bucket.

**Usage**:
```bash
aws-vibe-guru s3-get-object "my-bucket" "file.txt"
aws-vibe-guru s3-get-object "my-bucket" "logs/2024/app.log"
aws-vibe-guru s3-get-object "data-bucket" "data/users/export.csv"
```

**Parameters**:
- `bucket_name` (required): Bucket name
- `object_key` (required): Object key (path)

**Return**:
Dictionary containing:
- `bucket`: Bucket name
- `key`: Object key
- `size`: Size in bytes
- `size_mb`: Size in MB (formatted)
- `last_modified`: Last modification timestamp
- `content_type`: MIME content type
- `etag`: Object ETag
- `storage_class`: Storage class
- `version_id`: Version ID (if versioning enabled)
- `metadata`: Custom metadata dictionary

**Example Output**:
```
Object Details:
──────────────────────────────────────────────────

Bucket: my-production-bucket
Key: data/reports/2024-Q1.pdf
Size: 5,678,901 bytes (5.42 MB)
Last Modified: 2024-03-31 15:22:10 UTC
Content Type: application/pdf
ETag: d41d8cd98f00b204e9800998ecf8427e
Storage Class: STANDARD
Version ID: N/A

Metadata:
  department: finance
  year: 2024
  quarter: Q1
```

---

### 9. `s3-read-object`

**Description**: Reads and displays the content of a text file from an S3 bucket directly in the terminal. Can search by prefix or read a specific file.

**Usage**:
```bash
aws-vibe-guru s3-read-object "my-bucket" "file.txt"
aws-vibe-guru s3-read-object "my-bucket" "logs/2024/app.log"
aws-vibe-guru s3-read-object "my-bucket" --prefix "config/"
aws-vibe-guru s3-read-object "my-bucket" "file.txt" --encoding "latin-1"
aws-vibe-guru s3-read-object "my-bucket" "data.json" --json
```

**Parameters**:
- `bucket_name` (required): Bucket name
- `object_key` (optional): Object key (path) - required if --prefix not provided
- `--prefix, -p` (optional): Search for objects by prefix (lists matching objects)
- `--encoding, -e` (optional, default="utf-8"): Text encoding to use when reading file
- `--json, -j` (optional, default=False): Format JSON content with 2-space indentation

**Return**:
Dictionary containing:
- `bucket`: Bucket name
- `key`: Object key
- `size`: Size in bytes
- `content_type`: MIME content type
- `is_binary`: Boolean indicating if file is binary
- `encoding`: Encoding used (if text file)
- `content`: File content as string (if text file)

**Behavior**:
- If `--prefix` is provided and finds exactly 1 file: automatically reads that file
- If `--prefix` is provided and finds multiple files: lists files and asks user to specify exact key
- If `--prefix` is provided and finds no files: displays error message
- Detects binary files and displays warning instead of content
- Supports custom text encoding for non-UTF-8 files
- With `--json` flag: parses and formats JSON with 2-space indentation (shows warning if not valid JSON)

**Example Output (Text File)**:
```
Bucket: my-production-bucket
Key: config/app.json
Size: 1,234 bytes
Content Type: application/json
────────────────────────────────────────────────────────────────────────────────

{
  "app_name": "My Application",
  "version": "1.0.0",
  "environment": "production",
  "database": {
    "host": "db.example.com",
    "port": 5432
  }
}
```

**Example Output (JSON with --json flag)**:
```
Bucket: my-production-bucket
Key: config/settings.json
Size: 456 bytes
Content Type: application/json
────────────────────────────────────────────────────────────────────────────────

{
  "app_name": "My Application",
  "version": "2.0.1",
  "environment": "production",
  "features": {
    "logging": true,
    "metrics": true,
    "cache": false
  },
  "database": {
    "host": "db.example.com",
    "port": 5432,
    "pool_size": 20
  }
}
```

**Example Output (Binary File)**:
```
Bucket: my-production-bucket
Key: images/logo.png
Size: 45,678 bytes
Content Type: image/png
────────────────────────────────────────────────────────────────────────────────

⚠️  This file appears to be binary and cannot be displayed as text.
File size: 45,678 bytes
```

**Example Output (Search by Prefix - Multiple Files)**:
```
Found 3 object(s):

Multiple objects found. Please specify the exact object_key:
  - config/app.json
  - config/database.json
  - config/features.json
```

**Example Output (Search by Prefix - Single File)**:
```
Found 1 object(s):

Reading: config/app.json

Bucket: my-production-bucket
Key: config/app.json
Size: 1,234 bytes
Content Type: application/json
────────────────────────────────────────────────────────────────────────────────

{
  "app_name": "My Application",
  ...
}
```

---

### 10. `s3-read-folder`

**Description**: Reads all files from a folder (prefix) in an S3 bucket and displays their contents in a simplified format. Shows a header with folder information and total files, then lists each file with its full path and content.

**Usage**:
```bash
aws-vibe-guru s3-read-folder "my-bucket" "logs/2024/"
aws-vibe-guru s3-read-folder "my-bucket" "config/"
aws-vibe-guru s3-read-folder "my-bucket" "config/" --json
aws-vibe-guru s3-read-folder "my-bucket" "data/" --max 50
aws-vibe-guru s3-read-folder "my-bucket" "files/" --encoding "latin-1"
```

**Parameters**:
- `bucket_name` (required): Bucket name
- `prefix` (required): Folder prefix/path to read
- `--encoding, -e` (optional, default="utf-8"): Text encoding to use
- `--max, -m` (optional, default=unlimited): Maximum number of files to read
- `--json, -j` (optional, default=False): Format JSON content with 2-space indentation

**Return**:
Dictionary containing:
- `bucket`: Bucket name
- `prefix`: Folder prefix
- `total_files`: Total number of files read
- `files`: List of files with:
  - `key`: Object key (full path)
  - `size`: Size in bytes
  - `is_binary`: Boolean indicating if file is binary
  - `content`: File content as string (if text file)
  - `error`: Error message (if read failed)

**Behavior**:
- Reads ALL files from the specified folder by default (no pagination limit)
- Displays a header showing folder path and total files count
- For each file:
  - Shows the full path (key)
  - Displays the content (or skips if binary)
  - Continues to next file even if one fails
- With `--json` flag: parses and formats JSON files with 2-space indentation
- Binary files are detected and skipped with a warning
- Errors on individual files are displayed but don't stop the process

**Example Output**:
```
Reading folder: logs/2024-01/
Bucket: my-production-bucket
Total files: 3
================================================================================

File: logs/2024-01/app-01.log
--------------------------------------------------------------------------------
[2024-01-01 10:00:00] INFO Starting application
[2024-01-01 10:00:01] INFO Connected to database
[2024-01-01 10:00:02] INFO Server listening on port 8080

File: logs/2024-01/app-02.log
--------------------------------------------------------------------------------
[2024-01-02 10:00:00] INFO Starting application
[2024-01-02 10:00:01] INFO Connected to database
[2024-01-02 10:00:02] INFO Server listening on port 8080

File: logs/2024-01/config.json
--------------------------------------------------------------------------------
{
  "app_name": "My Application",
  "version": "1.0.0",
  "environment": "production"
}
```

**Example Output (with --json flag)**:
```
Reading folder: config/
Bucket: my-production-bucket
Total files: 2
================================================================================

File: config/app.json
--------------------------------------------------------------------------------
{
  "app_name": "My Application",
  "version": "2.0.1",
  "features": {
    "logging": true,
    "metrics": true
  }
}

File: config/database.json
--------------------------------------------------------------------------------
{
  "host": "db.example.com",
  "port": 5432,
  "pool_size": 20
}
```

**Example Output (Binary File)**:
```
File: images/logo.png
--------------------------------------------------------------------------------
⚠️  Binary file (skipped)
```

---

## AWS Configuration

### Credentials

The system supports two authentication methods:

#### 1. Credentials File (`~/.aws/credentials`)
```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
region = us-east-1
```

#### 2. Environment Variables
```bash
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
export AWS_DEFAULT_REGION="us-east-1"
```

### Required Permissions

The AWS user/role needs the following permissions:

**SQS**:
- `sqs:ListQueues`
- `sqs:GetQueueAttributes`
- `sqs:GetQueueUrl`

**S3**:
- `s3:ListAllMyBuckets`
- `s3:ListBucket`
- `s3:GetObject`
- `s3:GetObjectMetadata`

**CloudWatch**:
- `cloudwatch:GetMetricStatistics`

---

## Core Technical Functions

### `read_aws_credentials()`
**Return**: `dict` with `access_key`, `secret_key`, `region`

### `create_sqs_connection(access_key, secret_key, region)`
**Return**: `boto3.client` (SQS client)

### `list_sqs_queues(queue_name_prefix, max_results)`
**Return**: `list[dict]` with `name` and `url`

### `get_queue_attributes(queue_url)`
**Return**: `dict` with formatted queue attributes

### `get_queue_metrics(queue_url, days)`
**Return**: `dict` with daily volume metrics

### `get_queue_oldest_message(queue_url, days)`
**Return**: `dict` with message age metrics

### `analyze_queue_volume(queue_url, days)`
**Return**: `dict` with complete statistical analysis

### `create_s3_connection(access_key, secret_key, region)`
**Return**: `boto3.client` (S3 client)

### `list_buckets()`
**Return**: `list[dict]` with `name` and `creation_date`

### `list_bucket_objects(bucket_name, prefix, max_keys)`
**Return**: `dict` with bucket info and list of objects

### `get_object_info(bucket_name, object_key)`
**Return**: `dict` with detailed object information

### `read_object_content(bucket_name, object_key, encoding)`
**Return**: `dict` with object content and metadata (detects binary files)

### `read_folder_contents(bucket_name, prefix, encoding, max_files)`
**Return**: `dict` with folder info and list of files with their contents

### `create_daily_breakdown(data, value_key, date_key, message_suffix, number_of_days_to_highlight)`
**Return**: `list[Text]` with formatted breakdown lines

### `create_bar_chart(data, value_key, label_key, title, height, date_width, y_axis_width)`
**Return**: `list[str]` with ASCII chart lines

---

## Constants

- `ONE_DAY_IN_SECONDS = 86400`: One day in seconds
- `ONE_HOUR_IN_SECONDS = 3600`: One hour in seconds

---

## Error Handling

All core functions raise `ValueError` when:
- AWS credentials are invalid
- Connection to AWS fails
- Queue not found
- Bucket or object not found
- CloudWatch/SQS/S3 API error

---

## Future Implementations

To add new features, consider:

1. **New CLI Commands**: Add in `cli.py` using `@app.command()` decorator
2. **New SQS/S3 Features**: Add functions in `aws_sqs.py` or `aws_s3.py`
3. **New AWS Services**: Create new modules (e.g., `aws_ec2.py`, `aws_lambda.py`, `aws_dynamodb.py`)
4. **Visualizations**: Add helpers in `cli_helpers.py`

### Structure for New Command

```python
@app.command()
def new_command(
    parameter: str = typer.Argument(..., help="Description"),
    option: int = typer.Option(10, "--option", "-o", help="Description")
) -> None:
    panel_content = Text(f"Executing: {parameter}")
    panel = Panel(panel_content, "Title")
    console.print(panel)

    result = module_function(parameter, option)

    for item in result:
        console.print(Text(f"Item: {item}"))
```

### Structure for New AWS Function

```python
def new_aws_function(parameter, days=7):
    try:
        client = create_sqs_connection()

        response = client.aws_operation(
            Parameter=parameter
        )

        data = response.get("Data", [])

        result = {
            "key1": value1,
            "key2": value2,
        }

        return result

    except ClientError as e:
        raise ValueError(f"Operation error: {e}") from e
```

---

## Important Notes

- All CloudWatch metrics are obtained in UTC
- Analysis periods use `datetime.datetime.utcnow()` as reference
- ASCII charts have default height of 8 characters
- Numbers are formatted with thousands separators (`,`)
- Top 3 days highlighted with asterisk (`*`) in breakdown
- Days of week are displayed in abbreviated format: `[Mon]`, `[Tue]`, etc.

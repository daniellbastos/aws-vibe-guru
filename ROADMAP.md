# AWS Toolbelt - Roadmap 🗺️

This document presents the simplified roadmap for AWS Toolbelt, focused on iterative development.

## 🎯 Vision

Create a simple and efficient CLI tool to extract AWS metrics, starting with SQS queues.

## 📋 Current Status

**Version**: 0.3.0 (SQS Metrics)
**Status**: ✅ Basic SQS Commands and Metrics
**Focus**: Queue metrics visualization and monitoring

---

## ✅ Version 0.1.0 - Functional Base

### Completed
- [x] Basic project structure with UV
- [x] Functional CLI with Typer and Rich
- [x] `hello` command for testing
- [x] Formatting helpers (cli_helpers.py)
- [x] Makefile to facilitate execution
- [x] Configured pyproject.toml
- [x] Updated README.md

---

## ✅ Version 0.2.0 - First SQS Functionality

### Completed
- [x] **`sqs-list-queues` Command**
  - List SQS queues from AWS account
  - Formatted output with Rich
  - Filter support with name prefix
- [x] **`sqs-get-attributes` Command**
  - Get detailed attributes of a specific queue
  - Friendly output format
  - Support for queue name lookup
- [x] **AWS Configuration**
  - AWS credentials file support
  - Environment variables support
  - Default region handling

---

## ✅ Version 0.3.0 - Queue Metrics (Current)

### Completed
- [x] **Message Volume Metrics**
  - Number of messages over time
  - Daily breakdown with totals
  - ASCII chart visualization
  - Customizable time range
- [x] **Message Age Monitoring**
  - Track oldest message age
  - Historical age data
  - Maximum age tracking
- [x] **Rich Formatting**
  - ASCII bar charts
  - Friendly number formatting
  - Clear data presentation

---

## 🚧 Version 0.4.0 - Advanced Metrics

**Focus**: Enhanced metrics and monitoring

### Planned
- [ ] **Additional Metrics**
  - Message processing rates
  - Error rates and DLQ tracking
  - Queue latency analysis
  - Cost estimation

- [ ] **Enhanced Visualization**
  - Multiple metrics in one view
  - Trend analysis
  - Comparative metrics
  - Custom time ranges

- [ ] **Alerting**
  - Define thresholds
  - Alert on anomalies
  - Notification integration

### Planned Commands
```bash
aws-toolbelt sqs-get-processing-rates "queue-name"  # Get processing metrics
aws-toolbelt sqs-get-error-rates "queue-name"      # Get error metrics
aws-toolbelt sqs-compare-queues "queue1" "queue2"  # Compare queues
```

---

## 🔮 Version 0.5.0 - Queue Management

**Focus**: Queue operations and maintenance

### Planned
- [ ] **Queue Management**
  - Create/delete queues
  - Update queue attributes
  - Purge queue contents
  - Move messages between queues

- [ ] **Testing Tools**
  - Send test messages
  - Simulate load
  - Validate queue settings

- [ ] **Maintenance**
  - Queue cleanup
  - DLQ management
  - Cost optimization

### Planned Commands
```bash
aws-toolbelt sqs-create "queue-name"          # Create new queue
aws-toolbelt sqs-update "queue-name"          # Update settings
aws-toolbelt sqs-move-messages "src" "dest"   # Move messages
aws-toolbelt sqs-test-load "queue-name"       # Load testing
```

---

## 🎯 Development Strategy

### Principles
1. **Iterative**: Small functionalities at a time
2. **Simple**: Keep code clean and simple
3. **Testable**: Each functionality should be testable
4. **Useful**: Each version should add real value

### Immediate Next Steps
1. Implement processing rate metrics
2. Add error rate tracking
3. Create comparative analysis
4. Improve visualization options

### Success Criteria by Version

#### v0.4.0
- [ ] Comprehensive metrics collection
- [ ] Enhanced visualization options
- [ ] Trend analysis capabilities
- [ ] Alert system foundation

#### v0.5.0
- [ ] Full queue management features
- [ ] Testing and validation tools
- [ ] Maintenance automation
- [ ] Cost optimization features

---

## 🤝 How to Contribute

1. **Choose a feature** from the current roadmap
2. **Create a branch** for your feature
3. **Implement simply** and testably
4. **Test locally** with available commands
5. **Open a Pull Request** with clear description

## 📊 Progress

- ✅ **v0.1.0**: Functional base (100%)
- ✅ **v0.2.0**: SQS Commands (100%)
- ✅ **v0.3.0**: Queue Metrics (100%)
- 🚧 **v0.4.0**: Advanced Metrics (0%)
- 📋 **v0.5.0**: Queue Management (0%)

---

**Last Update**: Current version 0.3.0
**Next Goal**: Implement advanced metrics in v0.4.0

# VM Health Monitor
A Python-based monitoring project that connects to a remote Ubuntu VM using SSH, collects system health metrics, parses application logs, checks alert thresholds, and stores monitoring data in SQLite.
The project combines Python, Linux, SSH, monitoring, alerting, log parsing, and database concepts in one end-to-end workflow.

## Features
* Connects to an Ubuntu VM using SSH
* Collects CPU, memory, disk, load average and uptime
* Parses application logs
* Checks warning and critical thresholds
* Stores metrics in SQLite
* Shows alerts on screen
* Supports email alerts

## Project Structure
* `main.py` - Runs the complete monitoring flow
* `ssh_client.py` - Connects to the Ubuntu VM and runs commands
* `metrics.py` - Collects system metrics
* `log_parser.py` - Parses application logs
* `alerting.py` - Checks thresholds and generates alerts
* `database.py` - Stores and reads metrics using SQLite
* `config.yaml` - Stores server details, thresholds and log path

## How to Run
1. Activate the virtual environment:

```bash
source .venv/bin/activate
```

2. Run the project:
```bash
python main.py
```

The program will connect to the VM, collect metrics, parse logs, save metrics to SQLite and check alerts.

## Configuration
Update `config.yaml` with:

* VM host
* Username
* SSH port
* SSH key path
* Metric thresholds
* Application log path

## Dependencies
* Python 3
* Paramiko
* PyYAML
* SQLite

## Security
Do not upload sensitive information such as:

* Private SSH keys
* Passwords
* Email credentials
* `.env` files

## Sample Output
A sample terminal output screenshot is available in the `screenshots` folder.





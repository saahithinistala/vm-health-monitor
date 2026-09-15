import yaml
from yaml import safe_load
from metrics import metrics_dict
import smtplib
from email.message import EmailMessage
import os

check_alerts = []
email_alerts = []

def check_cpu_alert():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

        if metrics_dict['cpu_used'] == "Error":
            result = "ERROR: CPU Usage metric could not be collected"
        else:
            if metrics_dict['cpu_used'] >= config['metrics']['cpu_usage_critical']:
                result = f"CRITICAL: CPU Usage is {metrics_dict['cpu_used']}% (threshold: {config['metrics']['cpu_usage_critical']}%)"
            elif metrics_dict['cpu_used'] >= config['metrics']['cpu_usage_warning']:
                result = f"WARNING: CPU Usage is {metrics_dict['cpu_used']}% (threshold: {config['metrics']['cpu_usage_warning']}%)"
            else:
                result = "OK"

        check_alerts.append(result)

def check_memory_alert():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

        if metrics_dict['memory_used'] == "Error":
            result = "ERROR: Memory Usage metric could not be collected"
        else:
            if metrics_dict['memory_used'] >= config['metrics']['memory_usage_critical']:
                result = f"CRITICAL: Memory Usage is {metrics_dict['memory_used']}% (threshold: {config['metrics']['memory_usage_critical']}%)"
            elif metrics_dict['memory_used'] >= config['metrics']['memory_usage_warning']:
                result = f"WARNING: Memory Usage is {metrics_dict['memory_used']}% (threshold: {config['metrics']['memory_usage_warning']}%)"
            else:
                result = "OK"

        check_alerts.append(result)

def check_disk_alert():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

        if metrics_dict['disk_used'] == "Error":
            result = "ERROR: Disk Usage metric could not be collected"
        else:
            if metrics_dict['disk_used'] >= config['metrics']['disk_usage_critical']:
                result = f"CRITICAL: Disk Usage is {metrics_dict['disk_used']}% (threshold: {config['metrics']['disk_usage_critical']}%)"
            elif metrics_dict['disk_used'] >= config['metrics']['disk_usage_warning']:
                result = f"WARNING: Disk Usage is {metrics_dict['disk_used']}% (threshold: {config['metrics']['disk_usage_warning']}%)"
            else:
                result = "OK"

        check_alerts.append(result)

def check_load_alert():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

        if metrics_dict['load_average'] == "Error":
            result = "ERROR: Load Average metric could not be collected"
        else:
            if float(metrics_dict['load_average']) >= config['metrics']['load_average_critical']:
                result = f"CRITICAL: Load Average is {metrics_dict['load_average']} (threshold: {config['metrics']['load_average_critical']})"
            elif float(metrics_dict['load_average']) >= config['metrics']['load_average_warning']:
                result = f"WARNING: Load Average is {metrics_dict['load_average']} (threshold: {config['metrics']['load_average_warning']})"
            else:
                result = "OK"

        check_alerts.append(result)

def send_email_alert():
    app_password = os.getenv("GMAIL_APP_PASSWORD")
    with open("config.yaml", "r") as file:
        config = safe_load(file)
        sender = config['email']['sender']
        receiver = config['email']['receiver']
        port = config['email']['port']
        mail_server = config['email']['mail_server']

        smtp_server = smtplib.SMTP_SSL(mail_server, port)

        #--Login into mail server through the SMTP Connection
        if app_password is None:
            print("Mail Server Password is not set")
            return

        smtp_server.login(sender, app_password)

        message = EmailMessage()
        message["From"] = sender
        message["To"] = receiver
        message["Subject"] = "VM Health Alert"
        message.set_content("\n".join(email_alerts))

        smtp_server.send_message(message)

        #--Close the SMTP Connection
        smtp_server.quit()


def vm_health_alerting():
    #--Clearing the list
    check_alerts.clear()
    email_alerts.clear()

    #--Calling functions to check thresholds
    check_cpu_alert()
    check_memory_alert()
    check_disk_alert()
    check_load_alert()

    count = 0
    for value in check_alerts:
        if "OK" not in value:
            count += 1
            print(value)
            email_alerts.append(value)

    if count == 0:
        print("No alerts detected")
    else:
        send_email_alert()
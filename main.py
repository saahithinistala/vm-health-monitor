import ssh_client
from metrics import collect_metrics
from alerting import vm_health_alerting
from log_parser import vm_log_parsing
from database import connect_database, save_metrics, view_metrics

#--Establish SSH Connection with the Ubuntu Server
ssh_client.ssh_connect()

#--Metrics collection
print("===== VM HEALTH METRICS =====")
collect_metrics()
print("\n")

#--Log Parsing
print("===== VM LOG PARSING =====")
vm_log_parsing()

#--Database
print("===== VM Database=====")
connect_database()
save_metrics()
view_metrics()
print("\n")

#--Alerting
print("===== VM HEALTH ALERTS =====")
vm_health_alerting()

ssh_client.ssh_close()
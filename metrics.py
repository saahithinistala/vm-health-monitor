import ssh_client

metrics_dict = {}

def cpu_usage():
    output, error = ssh_client.exec_command("top -bn1 | grep \"Cpu(s)\"")

    if len(error) > 0:
        print("CPU metrics collection failed")
        result = "Error"
    else:
        idle_percentage = ""
        for value in output.split(","):
            if " id" in value:
                idle_percentage = value.split()[0]

        if len(idle_percentage) > 0:
            cpu_used = round(100 - float(idle_percentage), 2)
            result = cpu_used
        else:
            print("Idle percentage in CPU metrics collection is empty")
            result = "Error"

    metrics_dict['cpu_used'] = result

def memory_usage():
    output, error = ssh_client.exec_command("free -m | grep \"Mem:\"")
    if len(error) > 0:
        print("Memory metrics collection failed")
        result = "Error"
    else:
        total = int(output.split()[1])
        available = int(output.split()[6])
        memory_used = round(((total - available) / total) * 100 , 2)
        result = memory_used

    metrics_dict['memory_used'] = result

def disk_usage():
    output, error = ssh_client.exec_command("df -h / | tail -1")
    if len(error) > 0:
        print("Disk Usage metrics collection failed")
        result = "Error"
    else:
        result = output.split()[4]
        result = int(result.replace("%", ""))

    metrics_dict['disk_used'] = result

def load_average():
    output, error = ssh_client.exec_command("uptime")
    if len(error) > 0:
        print("Load average metrics collection failed")
        result = "Error"
    else:
        result = "Error"
        for value in output.split(","):
            if " load average:" in value:
                result = value.split(":")[1]
                result = result.strip()

    metrics_dict['load_average'] = result

def uptime():
    output, error = ssh_client.exec_command("uptime -p")
    if len(error) > 0:
        print("uptime metrics collection failed")
        result = "Error"
    else:
        output = output.removeprefix("up ")
        result = output.replace(",","").strip()

    metrics_dict['uptime'] = result


def collect_metrics():
    cpu_usage()
    memory_usage()
    disk_usage()
    load_average()
    uptime()

    print(f"CPU Usage: {metrics_dict['cpu_used']}%")
    print(f"Memory Usage: {metrics_dict['memory_used']}%")
    print(f"Disk Usage: {metrics_dict['disk_used']}%")
    print(f"Load Average: {metrics_dict['load_average']}")
    print(f"Uptime: {metrics_dict['uptime']}")
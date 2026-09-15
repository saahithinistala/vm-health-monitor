import ssh_client
from yaml import safe_load

log_levels = {
    "CRITICAL": 0,
    "ERROR": 0,
    "WARNING": 0
}

log_level_summary = []

def line_parse(line):
    log_level_dict = {}
    parts = line.split()
    timestamp = parts[0] + " " + parts[1]
    severity = parts[2]
    message = " ".join(parts[3:])

    log_level_dict['timestamp'] = timestamp
    log_level_dict['severity'] = severity
    log_level_dict['message'] = message

    return log_level_dict

def vm_log_parsing():
    #--Reset values
    for key in log_levels:
        log_levels[key] = 0
    log_level_summary.clear()

    with open("config.yaml", "r") as file:
        config = safe_load(file)
        application_log = config['logs']['application_log']

        output, error = ssh_client.exec_command(f"tail -n 50 {application_log}")
        if len(error) > 0:
            print("ERROR: Log file reading failed")
        else:
            for line in output.splitlines():
                if "CRITICAL" in line:
                    log_levels["CRITICAL"] += 1
                    log_level_dict = line_parse(line)
                    log_level_summary.append(log_level_dict)
                elif "ERROR" in line:
                    log_levels["ERROR"] += 1
                    log_level_dict = line_parse(line)
                    log_level_summary.append(log_level_dict)
                elif "WARNING" in line:
                    log_levels["WARNING"] += 1
                    log_level_dict = line_parse(line)
                    log_level_summary.append(log_level_dict)

            print("Log Summary:")
            for key, value in log_levels.items():
                print(f"{key}: {value}")

            print("\n")
            print("Parsed Log Events:")
            for each_entry in log_level_summary:
                for key, value in each_entry.items():
                    print(f"{key.capitalize()}: {value}")
                print("\n")

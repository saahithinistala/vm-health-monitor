import paramiko
import yaml

#--Create an SSHClient object
client = paramiko.SSHClient()

#--Load trusted SSH host keys from the local system
client.load_system_host_keys()

def ssh_connect():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
        host = config['ssh']['host']
        username = config['ssh']['username']
        port = config['ssh']['port']
        key_filename = config['ssh']['key_filename']
    try:
        client.connect(
            hostname=host,
            username=username,
            port=port,
            key_filename=key_filename
        )
        print("SSH connection successful")
    except paramiko.AuthenticationException:
        print("SSH Authentication Failed")

    except paramiko.SSHException:
        print("SSH Connection Error")

    except OSError:
        print("Unable to reach Server")

def exec_command(command):
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode().strip()
    error = stderr.read().decode().strip()
    return output, error

#--Close the SSH Connection
def ssh_close():
    client.close()
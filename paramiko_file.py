import paramiko
import pandas as pd
import logging
import socket

def setup_logging():
    logging.basicConfig(
        filename="./execution_logs.txt",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

def execute_unix_commands(ssh, commands):
    for command in commands:
        command = command.strip()
        if command:
            logging.info(f"Executing Unix command: {command}")
            stdin, stdout, stderr = ssh.exec_command(command)
            logging.info(stdout.read().decode('utf-8'))
            logging.error(stderr.read().decode('utf-8'))

def execute_wintel_commands(ssh, commands):
    for command in commands:
        command = command.strip()
        if command:
            # Execute Wintel command logic here
            logging.info(f"Executing Wintel command: {command}")
            # Replace with your Wintel-specific execution logic

def execute_commands(hostname, port, username, password, commands_file, operating_system, timeout=120):
    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    logging.info("Inside execute_commands method:")
    logging.info("Trying to connect to the server:")
    try:
        logging.info("Hostname: {} \n Port: {} \n username: {} \n commands_file: {}".format(hostname, port, username, commands_file))
        ssh.connect(hostname, port=port, username=username, password=password)
        logging.info("Connected to the server")
    except (paramiko.AuthenticationException, paramiko.SSHException, socket.error) as e:
        logging.error("An error occurred while connecting: {}".format(e))
        return

    try:
        # Read commands from the file
        with open(commands_file, 'r') as f:
            commands = f.readlines()
        logging.info("Commands to execute: {}".format(commands))
        
        if operating_system == 'Unix':
            execute_unix_commands(ssh, commands)
        elif operating_system == 'Wintel':
            execute_wintel_commands(ssh, commands)
        else:
            logging.error("Unknown operating system: {}".format(operating_system))
        
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        # Close the SSH connection
        ssh.close()

def main():
    setup_logging()

    excel_file = "process_and_command_mapping.xlsx"
    ip_to_lookup = "192.168.43.19"
    process_to_lookup = "test"

    # Read the Excel file
    df = pd.read_excel(excel_file)

    # Convert 'ip' and 'port' columns to appropriate types
    df['ip'] = df['ip'].astype(str)
    df['port'] = df['port'].astype(int)

    # Filter rows based on IP and Process_Name
    filtered_rows = df[(df['ip'] == ip_to_lookup) & (df['process_name'] == process_to_lookup)]
    print("Filtered rows are:")
    print(filtered_rows)

    if filtered_rows.empty:
        logging.info("No matching records found.")
        return
    
    for index, row in filtered_rows.iterrows():
        hostname = row['hostname']
        port = int(row['port'])
        username = row['username']
        password = row['password']
        commands_file = row['command_file']
        operating_system = row['OS']  # Get the operating system from the 'OS' column
        print("Hostname: {} \n Port: {} \n username: {} \n commands_file: {} \n OS: {}".format(hostname, port, username, commands_file, operating_system))
        
        execute_commands(hostname, port, username, password, commands_file, operating_system)

if __name__ == "__main__":
    main()

import subprocess
import os

score = 0
host = '10.22.198.100'  # IP address of the second computer
# List of correct commands
correct_commands = ['touch', 'ping', 'python tt_new.py', 'clear']

history_file = os.path.expanduser('~/.zsh_history')
# history_file = os.path.expanduser('~/.bash_history')


def check_ping(host):
    try:
        # Execute the ping command with a count of 1 and a timeout of 2 seconds
        command = ['ping', '-c', '1', '-W', '2', host]
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=5)

        # Check the return code of the ping command
        if result.returncode == 0:
            return True  # Ping was successful
        else:
            return False  # Ping failed

    except subprocess.TimeoutExpired:
        return False  # Ping command timed out

    except Exception:
        return False  # Other exceptions occurred during ping command execution


def check_correct_commands(history_file, correct_commands):
    global score
    with open(history_file, 'r') as file:
        history_lines = file.readlines()

    executed_commands = []
    for line in history_lines:
        command = line.strip()
        if command not in executed_commands:
            executed_commands.append(command)
            # print(command)

    # Check if executed commands match the correct commands
    print(executed_commands)
    for command in correct_commands:
        if command in executed_commands:
            score += 10


def clear_bash_history():
    try:
        # Clear the Bash command history
        # subprocess.run('history -c', shell=True, check=True)

        # Remove the Bash history file
        subprocess.run('rm ~/.zsh_history', shell=True, check=True)

        # Start a new Bash session
        subprocess.run('touch ~/.zsh_history', shell=True, check=True)

        subprocess.run('zsh', shell=True, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


# Check ping success
is_ping_successful = check_ping(host)
if is_ping_successful:
    score += 20

check_correct_commands(history_file, correct_commands)

print("\nScore - " + str(score)+"\n")

# clear_bash_history()

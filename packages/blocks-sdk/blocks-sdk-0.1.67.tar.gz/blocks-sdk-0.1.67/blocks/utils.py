import subprocess

def bash(cmd_string, suppress_exception=False):
    """
    Run a shell command, streaming its output in real time as if it were executed directly in the terminal.
    It merges stdout and stderr to preserve the natural order of messages.
    """
    process = subprocess.Popen(
        cmd_string,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,  # Merge stderr into stdout
        stdin=subprocess.DEVNULL,
        bufsize=1,
        text=True
    )

    # Read and print output line by line
    for line in iter(process.stdout.readline, ''):
        print(line, end='', flush=True)  # `end=''` prevents double newlines

    process.stdout.close()
    returncode = process.wait()  # Ensure process completion

    if returncode != 0 and not suppress_exception:
        raise subprocess.CalledProcessError(returncode, cmd_string)

    return returncode  # Or return None if you don't care about it
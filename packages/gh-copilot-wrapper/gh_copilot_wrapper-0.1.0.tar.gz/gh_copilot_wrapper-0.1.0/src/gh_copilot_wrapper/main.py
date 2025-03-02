import os
import subprocess
import sys
import pyperclip
from rich.console import Console
console = Console()


def main(promt: str = 'create a zsh function to execute a command and print its output. All stderr output should be suppressed'):
    proc_env_vars = os.environ.copy()
    proc_stdout = subprocess.PIPE
    command = f'gh copilot suggest -t shell {promt}'
    console.print(f'[green]Running command:[/green] {command}')

    process = subprocess.Popen(
        command,
        shell=True,
        stdout=proc_stdout,
        stderr=proc_stdout,
        env=proc_env_vars,
        cwd=os.getcwd()
    )

    lines_read = []

    while True:
        output = process.stdout.readline()
        if output:
            lines_read.append(output.decode())
        option_index = next((index for index, line in enumerate(lines_read) if "? Select an option" in line), None)
        suggestion_index = next((index for index, line in enumerate(lines_read) if " # Suggestion:" in line), None)
        if option_index:
            suggestion = lines_read[suggestion_index+1:option_index-1]
            suggestion_join = ''.join([x.lstrip() for x in suggestion])
            print(suggestion_join)
            pyperclip.copy(suggestion_join)
            exit(0)
        if process.returncode is not None:
            exit(process.returncode)
        # if suggestion_index and len(lines_read) > suggestion_index+2:
        #     suggestion = lines_read[suggestion_index+2]
        #     suggestion = suggestion.lstrip().rstrip()
        #
        #     print(suggestion)
        #     pyperclip.copy(suggestion)
        #     process.kill()
        #     break
        #
        # if process.poll() is not None:
        #     break


if __name__ == "__main__":
    args = sys.argv[1:]
    joined_args = ' '.join(args)
    main(joined_args)

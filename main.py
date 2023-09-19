import time, sys, os, subprocess, readline
from user_config import username, pcname, defaultdirectory, homealias
from colorama import Fore, Back, Style, init
init(autoreset=True)
# username2 = subprocess.check_output('echo $USER', shell=True, text=True)

text = Fore
bg = Back
style = Style
version = '[SourceCode] (No version, testing right now.)'
readline.parse_and_bind("tab: complete")
readline.set_history_length(1000)

def get_last_command():
    try:
        return readline.get_history_item(readline.get_current_history_length())
    except IndexError:
        return None

def prints(text, delay=0.08):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

def run(cmd):
    try:
        result = subprocess.check_output(cmd, shell=True, text=True)
        print(result)
    except:
        pass

def clear():
    if os.name == 'posix':  # For UNIX-based systems (Linux, macOS)
        os.system('clear')
    elif os.name == 'nt':  # For Windows
        os.system('cls')
    else:
        print("Sorry, clearing the terminal is not supported on your system.")
        sys.exit(0)
while True:
    cmd = ''
    cmd = input(f"{style.BRIGHT}{username}:& {Style.RESET_ALL}") # The prompt
    if cmd == '^[[A':
        last_command = get_last_command()
        if last_command:
            print(f"Last command: {last_command}")
        else:
            print("No command history available.")
    if cmd == '':
        pass
    elif cmd.startswith(' '):
        pass
    elif cmd == "help":
        print('''           > HELP MENU <
clear - Clears nSH Terminal.
nte - nSH Text Editor.
exit - Exits nSH.
ls - Returns list of items in the current directory.
about - Returns about info.
run - Runs a file.
cpm - Installs a package with nSH's default package manager - Codec Package Manager. (Front-end for APT)''')
    elif cmd == 'clear':
        clear()
    elif cmd == 'exit':
        sys.exit(0)
    elif cmd == 'nte':
        clear()
        print("""           > NTE <
----------------------------------------------------
Type 'exit' to exit NTE.
""")
        text = ""
        while True:
            line = input()
            if line == 'exit':
                break
            text += line + '\n'
        print("Exiting NTE...")
        clear()
    elif cmd.startswith('ls'):
        directory = cmd[len('ls '):]
        if directory == '':
            run(f'ls {defaultdirectory}')
        else:
            run(f'ls {directory}')

    elif cmd == 'about':
        prints(f"Hi. This is nSH (Noer SHell) coded in Python 3.11." + '\n')
        print(f"You're running Python Version: '{sys.version}'\nYou're running nSH version {version}")
        input(bg.RED + "ENTER to exit this command." + style.RESET_ALL)
    elif cmd.startswith("run"):
        userfile = cmd[len('run '):]
        if userfile == '':
            print("Not a valid file.")
            pass
        else:
            try:
                run(userfile)
            except subprocess.CalledProcessError:
                print("Error! Not a valid file.")
    elif cmd.startswith("cpm"):
        flags = cmd[len('cpm '):]
        args = cmd.split()
        if len(args) < 3:
            print("Usage: cpm [-i (install) / -u (uninstall) / -p (purge)]\n* This installs with apt-get, please expect it to not work on other distros or windows or mac.")
        else:
            if args[1] == '-i':
                package_name = args[2]
                print(f"Installing package: {package_name}")
                try:
                    # Use 'sudo apt' to install packages on Debian-based systems
                    run(f'sudo apt-get install {package_name}')
                except subprocess.CalledProcessError as e:
                    print(f"Error installing {package_name}: {e}")
            elif args[1] == '-u':
                run(f'sudo apt-get remove {package_name}')
            elif args[1] == '-p':
                run(f'sudo apt-get purge {package_name}')
# scripting laterrrr
    else:
        print(text.RED + "Invalid command.")

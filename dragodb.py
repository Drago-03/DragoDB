import cmd
import time
import threading
from collections import defaultdict
import random
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class DragoDB:
    def __init__(self):
        self.data = {}
        self.expiry = {}
        self.lock = threading.Lock()

    def set(self, key, value):
        with self.lock:
            self.data[key] = value
            if key in self.expiry:
                del self.expiry[key]

    def get(self, key):
        with self.lock:
            if key in self.expiry and time.time() > self.expiry[key]:
                del self.data[key]
                del self.expiry[key]
                return None
            return self.data.get(key)

    def delete(self, key):
        with self.lock:
            if key in self.data:
                del self.data[key]
            if key in self.expiry:
                del self.expiry[key]

    def expire(self, key, seconds):
        with self.lock:
            if key in self.data:
                self.expiry[key] = time.time() + seconds
                return True
            return False

class DragoDBShell(cmd.Cmd):
    intro = f"""{Fore.RED}
    ____                       ____  ____
   / __ \_________ _____ ____  / __ \/ __ )
  / / / / ___/ __ `/ __ `/ _ \/ / / / __  |
 / /_/ / /  / /_/ / /_/ /  __/ /_/ / /_/ /
/_____/_/   \__,_/\__, /\___/_____/_____/
                 /____/
{Fore.YELLOW}Welcome to DragoDB! Type 'help' for a list of commands.
{Style.RESET_ALL}"""
    prompt = f"{Fore.GREEN}DragoDB> {Style.RESET_ALL}"

    def __init__(self):
        super().__init__()
        self.db = DragoDB()

    def do_set(self, arg):
        "Set a key-value pair: SET key value"
        args = arg.split()
        if len(args) != 2:
            print(f"{Fore.RED}Error: SET requires exactly two arguments{Style.RESET_ALL}")
            return
        key, value = args
        self.db.set(key, value)
        print(f"{Fore.GREEN}OK{Style.RESET_ALL}")

    def do_get(self, arg):
        "Get the value of a key: GET key"
        key = arg.strip()
        if not key:
            print(f"{Fore.RED}Error: GET requires a key{Style.RESET_ALL}")
            return
        value = self.db.get(key)
        if value is None:
            print(f"{Fore.YELLOW}(nil){Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}{value}{Style.RESET_ALL}")

    def do_del(self, arg):
        "Delete a key: DEL key"
        key = arg.strip()
        if not key:
            print(f"{Fore.RED}Error: DEL requires a key{Style.RESET_ALL}")
            return
        self.db.delete(key)
        print(f"{Fore.GREEN}OK{Style.RESET_ALL}")

    def do_expire(self, arg):
        "Set a key's time to live in seconds: EXPIRE key seconds"
        args = arg.split()
        if len(args) != 2:
            print(f"{Fore.RED}Error: EXPIRE requires a key and number of seconds{Style.RESET_ALL}")
            return
        key, seconds = args
        try:
            seconds = int(seconds)
        except ValueError:
            print(f"{Fore.RED}Error: Invalid number of seconds{Style.RESET_ALL}")
            return
        if self.db.expire(key, seconds):
            print(f"{Fore.GREEN}OK{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}(key not found){Style.RESET_ALL}")

    def do_dragon(self, arg):
        "Display a random dragon ASCII art"
        dragons = [
            r"""
      /\___/\
     (  o o  )
     /   V   \
    /(  \^/  )\
   /  \     /  \
  /    )___( __ \
 /    (     )    \
/    (  \  /  )   \
(     )  \/  (     )
 \    (    )    /
  \   /    \   /
   \ /      \ /
    V        V
    """,
            r"""
        _____
    .-'`     '.
 __/  __       \
/  \ /  \       |
|  | \__/ __   _/
|  |    .'  '. |
 \  \  /  __  \/
  \  \/  /  \  \
   \    /    \  \
    \__/      \__\
    """,
            r"""
      <>=======()
    (/\___   /|\\          ()==========<>_
          \_/ | \\        //|\   ______/ \)
            \_|  \\      // | \_/
              \|\/|\_   //  /\/
               (oo)\ \_//  /
              //_/\_\/ /  |
             @@/  |=\  \  |
                  \_=\_ \ |
                    \==\ \|\_ 
                 __(\===\(  )\
                (((~) __(_/   |
                     (((~) \  /
                     ______/ /
                     '------'
    """
        ]
        print(f"{Fore.RED}{random.choice(dragons)}{Style.RESET_ALL}")

    def do_exit(self, arg):
        "Exit DragoDB"
        print(f"{Fore.YELLOW}Farewell, brave adventurer! May your data always be safe and your queries swift.{Style.RESET_ALL}")
        return True

    def default(self, line):
        print(f"{Fore.RED}Unknown command. Type 'help' for a list of commands.{Style.RESET_ALL}")

if __name__ == "__main__":
    DragoDBShell().cmdloop()
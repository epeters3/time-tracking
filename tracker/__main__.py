import re
import sys
import typing as t
from datetime import datetime, timedelta


class Tracker:
    command_map = {
        "start": {"s", "start", "r", "resume"},
        "add": {"a", "add"},
        "check": {"check", "c"},
        "pause": {"p", "pause"},
        "end": {"end", "e"},
        "help": {"help", "h"},
        "quit": {"q", "quit", "exit"}
    }

    def __init__(self) -> None:
        self.total_time = timedelta()
        self.start_time = None
        self.is_tracking = False

    def start(self, _) -> None:
        """
        Begin tracking time.
        """
        self.start_time = datetime.now()
        self.is_tracking = True
        print(f"Started timer at {datetime.now()}")

    def check(self, _) -> None:
        """
        Check how much time you've tracked so far.
        """
        if not self.is_tracking:
            print("You need to start a timer before you can check it.")
            return

        print(
            f"You've tracked {self.total_time + (datetime.now() - self.start_time)} time so far."
        )

    def pause(self, _) -> None:
        """
        Pause the time tracker.
        """
        if not self.is_tracking:
            print("You need to start a timer before you can pause it.")
            return

        self.total_time += datetime.now() - self.start_time
        self.start_time = None
        self.is_tracking = False
        print(f"Tracker paused. You've tracked {self.total_time} time so far.")

    @staticmethod
    def end(_) -> None:
        """
        Pause, save, and quit the time tracking process.
        """
        print("This command is not implemented yet.")

    def help(self, _) -> None:
        """
        Print a description of the time tracker's commands.
        """
        for cmd, names in self.command_map.items():
            print(f"{cmd} (aliases={names}): {getattr(self, cmd).__doc__}")

    def add(self, args: t.List[str]):
        if len(args) != 1:
            raise AssertionError("add only accepts one argument")
        time_str = args[0]
        m = re.match("(\d+):(\d\d)", args[0])
        if not m:
            raise AssertionError("add's argument must be of the form hh:mm")
        hours = int(m.group(1))
        minutes = int(m.group(2))
        self.total_time += timedelta(hours=hours, minutes=minutes)
        print(f"added {time_str} to timer. You've tracked {self.total_time} time so far.")

    @staticmethod
    def quit(_):
        sys.exit(0)

    def _process_user_input(self, user_input: str):
        """
        Execute the command associated with `user_input`.
        """
        if " " in user_input:
            args = user_input.split(" ")
            user_cmd, args = args[0], args[1:]
        else:
            user_cmd = user_input
            args = []
        command = None
        for cmd, names in self.command_map.items():
            if user_cmd in names:
                command = cmd

        if command is None:
            print(f"invalid user input {user_input}")
        else:
            getattr(self, command)(args)

    def interact(self) -> None:
        print("Welcome to time tracking, please enter a command (press 'h' for help).")
        while True:
            user_input = input(">>> ")
            self._process_user_input(user_input)


if __name__ == "__main__":
    tracker = Tracker()
    tracker.interact()

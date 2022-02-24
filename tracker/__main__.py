import re
import sys
import typing as t
from datetime import datetime, timedelta

from color import Color


class Tracker:
    command_map = {
        "start": {"s", "start", "begin", "r", "resume"},
        "add": {"a", "add"},
        "check": {"check", "c"},
        "pause": {"p", "pause"},
        "help": {"help", "h"},
        "quit": {"q", "quit", "exit"}
    }

    def __init__(self):
        self.total_time = timedelta()
        self.last_check = datetime.now()
        self.is_tracking = False

    def start(self, _):
        """Begin tracking time."""
        self.is_tracking = True
        return "Started timer."

    def check(self, _):
        """Check how much time you've tracked so far."""
        pass

    def pause(self, _):
        """Pause the time tracker."""
        self.is_tracking = False
        return "Tracker paused."

    def help(self, _):
        """Print a description of the time tracker's commands."""
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
        return f"Added {time_str} to timer."

    @staticmethod
    def quit(_):
        sys.exit(0)

    def _tick(self):
        """Updates the tracked time."""
        now = datetime.now()
        if self.is_tracking:
            self.total_time += now - self.last_check
        self.last_check = now

    def _get_header_str(self, command: t.Optional[str]):
        """
        Creates a header string to display at the beginning of each response to user input. `command` is the user's
        command. If it is `None`, it is assumed that their command was invalid, and an error status is included in the
        header string.
        """
        now = datetime.now().strftime("%m-%d-%Y %I:%M:%S %p")
        if command:
            cmd_str = f"{Color.OKGREEN}[{command.upper()}]{Color.ENDC}"
        else:
            cmd_str = f"{Color.FAIL}[ERROR]{Color.ENDC}"
        return f"{cmd_str} {Color.OKBLUE}[{now}] [{self.total_time}]{Color.ENDC}"

    def _process_user_input(self, user_input: str):
        """Execute the command associated with `user_input`."""
        args = user_input.split(" ")
        user_cmd, args = args[0], args[1:]

        command = None
        for cmd, names in self.command_map.items():
            if user_cmd in names:
                command = cmd

        if command is None:
            msg = f"Invalid user input \"{user_input}\""
        else:
            msg = getattr(self, command)(args)

        return command, msg

    def interact(self):
        print("Welcome to time tracking, please enter a command (press 'h' for help).")
        while True:
            user_input = input(">>> ")
            self._tick()
            command, msg = self._process_user_input(user_input)
            output = self._get_header_str(command)
            if msg:
                output += f" {msg}"
            print(output)


if __name__ == "__main__":
    tracker = Tracker()
    tracker.interact()

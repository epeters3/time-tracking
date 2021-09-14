from datetime import datetime, timedelta


class Tracker:
    quits = {"q", "quit", "exit"}
    command_map = {
        "start": {"s", "start"},
        "check": {"check", "c"},
        "pause": {"p", "pause"},
        "end": {"end", "e"},
        "help": {"help", "h"},
    }

    def __init__(self) -> None:
        self.total_time = timedelta()
        self.start_time = None
        self.is_tracking = False

    def start(self) -> None:
        """
        Begin tracking time.
        """
        self.start_time = datetime.now()
        self.is_tracking = True
        print(f"Started timer at {datetime.now()}")

    def check(self) -> None:
        """
        Check how much time you've tracked so far.
        """
        if not self.is_tracking:
            print("You need to start a timer before you can check it.")
            return

        print(
            f"You've tracked {self.total_time + (datetime.now() - self.start_time)} time so far."
        )

    def pause(self) -> None:
        """
        Pause the time tracker.
        """
        if not self.is_tracking:
            print("You need to start a timer before you can pause it.")
            return

        self.total_time += datetime.now() - self.start_time
        self.start_time = None
        self.is_tracking = False
        print(f"You've tracked {self.total_time} time so far.")

    def end(self) -> None:
        """
        Pause, save, and quit the time tracking process.
        """
        print("This command is not implemented yet.")

    def process_user_input(self, user_input: str) -> str:
        """
        Return the command associated with `user_input`.
        """
        command = None
        for cmd, names in self.command_map.items():
            if user_input in names:
                command = cmd

        if command is None:
            print(f"invalid user input {user_input}")
        else:
            getattr(self, command)()

    def help(self) -> None:
        """
        Print a description of the time tracker's commands.
        """
        for cmd, names in self.command_map.items():
            print(f"{cmd} (aliases={names}): {getattr(self, cmd).__doc__}")

    def interact(self) -> None:
        print("Welcome to time tracking, please enter a command.")
        user_input = ""
        while True:
            user_input = input(">>> ")
            if user_input in self.quits:
                break
            self.process_user_input(user_input)


if __name__ == "__main__":
    tracker = Tracker()
    tracker.interact()

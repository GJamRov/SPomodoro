import tkinter as tk
from tkinter import messagebox
import time
import os
from mouseJiggler import MouseJiggler

LOG_FILE = "pomodoro_log.txt"

class PomodoroApp:
    def __init__(self, master, mouse_jiggler=None):
        self.root = master.winfo_toplevel()  # new: get top-level window
        self.root.title("Pomodoro Timer")     # set title on the top-level window
        self.master = master                   # preserve the passed-in master for layout
        self.is_running = False
        self.session_type = None  # "Work" or "Break"
        self.cycle_count = 0
        self.timer_id = None
        self.remaining_time = 0  # in seconds
        self.mouse_jiggler = mouse_jiggler  # dependency injection

        # ...existing UI creation removed; UI elements are linked externally...

    def set_on_top(self):
        self.root.attributes("-topmost", self.always_on_top.get())  # changed: use self.root

    def log_session(self, success):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        status = "SUCCESS" if success else "FAILURE"
        entry = f"{now} - {self.session_type} session - {status}\n"
        with open(LOG_FILE, "a") as f:
            f.write(entry)

    def start_timer(self):
        if self.is_running:
            return

        try:
            self.work_minutes = int(self.work_entry.get())
            self.short_break_minutes = int(self.break_entry.get())
            self.long_break_minutes = int(self.long_break_entry.get())
            self.cycles_until_long = int(self.cycles_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Make sure all durations and cycles are valid integers.")
            return

        self.is_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.cycle_count = 0
        self.start_work_session()

    def start_work_session(self):
        self.session_type = "Work"
        self.remaining_time = self.work_minutes * 60
        # Stop mouse jiggler on work sessions.
        if self.mouse_jiggler:
            self.mouse_jiggler.stop()
        self.update_timer()

    def start_break_session(self):
        self.session_type = "Break"
        if self.cycle_count % self.cycles_until_long == 0:
            # Use long break after specified cycles
            self.remaining_time = self.long_break_minutes * 60
        else:
            self.remaining_time = self.short_break_minutes * 60
        # Start mouse jiggler on break sessions.
        if self.mouse_jiggler:
            self.mouse_jiggler.start()
        self.update_timer()

    def update_timer(self):
        mins, secs = divmod(self.remaining_time, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")

        if self.remaining_time <= 0:
            # Session ended
            finished_session = True
            if self.session_type == "Work":
                # Count as a successful work block if completed
                self.log_session(success=True)
                self.cycle_count += 1
                self.start_break_session()
            else:
                self.log_session(success=True)
                self.start_work_session()
        else:
            self.remaining_time -= 1
            self.timer_id = self.master.after(1000, self.update_timer)

    def stop_timer(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None

        # If stopping in the middle of a work session, log as failure.
        if self.session_type == "Work" and self.remaining_time > 0:
            self.log_session(success=False)

        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.timer_label.config(text="00:00")

# New main entry point using the GUI class
if __name__ == "__main__":
    from gui import PomodoroGUI
    app = PomodoroGUI()
    app.run()
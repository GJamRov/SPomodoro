import tkinter as tk
from tkinter import messagebox
from main import PomodoroApp
from mouseJiggler import MouseJiggler

class PomodoroGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SPomodoro")
        # Set fixed window size to 600x600.
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        # Create shared MouseJiggler instance.
        self.mouse_jiggler = MouseJiggler()
        
        # Setup Options menu with an "Options" dropdown.
        self.auto_inactivity = tk.IntVar(value=0)  # off by default (0), enabled will be 2.
        menubar = tk.Menu(self.root)
        options_menu = tk.Menu(menubar, tearoff=0)
        options_menu.add_command(label="Edit Timer Parameters", command=self.open_options)
        options_menu.add_checkbutton(label="Auto Inactivity Detection", variable=self.auto_inactivity, 
                                     onvalue=2, offvalue=0, command=self.update_jiggler_status)
        menubar.add_cascade(label="Options", menu=options_menu)
        self.root.config(menu=menubar)
        
        # Main frame with centered layout.
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True)
        
        # Timer display in the center.
        self.timer_label = tk.Label(self.main_frame, text="00:00", font=("Helvetica", 72))
        self.timer_label.pack(pady=20)
        
        # Start and Stop buttons below timer.
        btn_frame = tk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        self.start_button = tk.Button(btn_frame, text="Start", command=self.pomodoro_start, width=10)
        self.start_button.grid(row=0, column=0, padx=10)
        self.stop_button = tk.Button(btn_frame, text="Stop", command=self.pomodoro_stop, state="disabled", width=10)
        self.stop_button.grid(row=0, column=1, padx=10)
        
        # Display message for auto inactivity detection.
        self.jiggler_status = tk.Label(self.main_frame, text="Auto Inactivity: Disabled", font=("Arial", 12))
        self.jiggler_status.pack(pady=10)
        
        # Instantiate PomodoroApp with shared mouse jiggler.
        self.pomodoro_app = PomodoroApp(self.main_frame, mouse_jiggler=self.mouse_jiggler)
        # Set default timer parameters.
        self.pomodoro_app.work_minutes = 20
        self.pomodoro_app.short_break_minutes = 5
        self.pomodoro_app.long_break_minutes = 15
        self.pomodoro_app.cycles_until_long = 4
        # Link timer label and control buttons.
        self.pomodoro_app.timer_label = self.timer_label
        self.pomodoro_app.start_button = self.start_button
        self.pomodoro_app.stop_button = self.stop_button

    def open_options(self):
        # Open a new Toplevel window to edit parameters.
        opt_win = tk.Toplevel(self.root)
        opt_win.title("Timer Options")
        tk.Label(opt_win, text="Work (min):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        work_entry = tk.Entry(opt_win, width=5)
        work_entry.insert(0, str(self.pomodoro_app.work_minutes))
        work_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(opt_win, text="Short Break (min):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        break_entry = tk.Entry(opt_win, width=5)
        break_entry.insert(0, str(self.pomodoro_app.short_break_minutes))
        break_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(opt_win, text="Long Break (min):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        long_break_entry = tk.Entry(opt_win, width=5)
        long_break_entry.insert(0, str(self.pomodoro_app.long_break_minutes))
        long_break_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(opt_win, text="Cycles until long break:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        cycles_entry = tk.Entry(opt_win, width=5)
        cycles_entry.insert(0, str(self.pomodoro_app.cycles_until_long))
        cycles_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Auto inactivity detection toggle in options.
        auto_var = tk.BooleanVar(value=self.auto_inactivity.get())
        auto_chk = tk.Checkbutton(opt_win, text="Enable Auto Inactivity Detection", variable=auto_var)
        auto_chk.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        
        def save_options():
            try:
                self.pomodoro_app.work_minutes = int(work_entry.get())
                self.pomodoro_app.short_break_minutes = int(break_entry.get())
                self.pomodoro_app.long_break_minutes = int(long_break_entry.get())
                self.pomodoro_app.cycles_until_long = int(cycles_entry.get())
            except ValueError:
                messagebox.showerror("Invalid input", "Please enter valid integers for parameters.")
                return
            self.auto_inactivity.set(auto_var.get())
            self.update_jiggler_status()
            opt_win.destroy()
        
        save_btn = tk.Button(opt_win, text="Save", command=save_options)
        save_btn.grid(row=5, column=0, columnspan=2, pady=10)
        
    def update_jiggler_status(self):
        # Update status label for auto inactivity detection.
        status = "Enabled" if self.auto_inactivity.get() == 2 else "Disabled"
        self.jiggler_status.config(text=f"Auto Inactivity: {status}")
        # Pass the flag to the mouse jiggler.
        self.mouse_jiggler.auto_detection = (self.auto_inactivity.get() == 2)
        
    def pomodoro_start(self):
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.pomodoro_app.cycle_count = 0
        self.pomodoro_app.start_work_session()

    def pomodoro_stop(self):
        self.pomodoro_app.stop_timer()
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.timer_label.config(text="00:00")

    def run(self):
        self.root.mainloop()

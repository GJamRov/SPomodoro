# SPomodoro

SPomodoro is a Pomodoro timer application built with Python and Tkinter. It assists users in structuring their work and break sessions while also preventing screen inactivity through a Mouse Jiggler feature.

## Features

- Fixed window size of 600x600 pixels.
- Customizable timer parameters (work minutes, short break, long break, and cycles until a long break).
- Auto Inactivity Detection: Uses a Mouse Jiggler to prevent the computer from entering an inactive state. When enabled, the app detects user inactivity for over 3 minutes and triggers a jiggle.
- Clean and straightforward GUI with an options menu to edit timer parameters and toggle auto inactivity detection.

## Dependencies

- Python 3.x
- Tkinter (comes with standard Python distribution)
- PyAutoGUI
- ctypes
- threading
- random

## Usage

1. Run the application by executing the main entry point.  
   Example:
   ```
   python Main.py
   ```

2. Use the "Edit Timer Parameters" option to set your desired work time, break durations, and cycle count.

3. Toggle "Auto Inactivity Detection" from the options menu. When enabled (value set to 2), the Mouse Jiggler ensures that your computer does not enter inactivity mode when idle for over 3 minutes.

4. Start your Pomodoro session and follow the on-screen timer.

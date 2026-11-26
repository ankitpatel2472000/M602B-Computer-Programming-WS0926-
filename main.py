import tkinter as tk
from gui import WeatherAppGUI

API_KEY = "6ac68749b8779314794173f254228edd"

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherAppGUI(root, API_KEY)
    root.mainloop()
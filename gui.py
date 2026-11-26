import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models import WeatherFetcher
from storage import FavoritesStorage

class WeatherAppGUI:
    def __init__(self, root: tk.Tk, api_key: str):
        self.root = root
        self.root.title("Weather Dashboard")
        self.root.geometry("820x650")

        self.fetcher = WeatherFetcher(api_key)
        self.storage = FavoritesStorage()

        self._build_interface()
        self._load_saved_favorites()

    def _build_interface(self):
        # Controls Frame
        top_frame = ttk.LabelFrame(self.root, text="Search & Favorites", padding=10)
        top_frame.pack(fill=tk.X, padx=12, pady=8)

        ttk.Label(top_frame, text="City Name:").grid(row=0, column=0, padx=5, sticky=tk.W)
        self.city_entry = ttk.Entry(top_frame, width=20)
        self.city_entry.grid(row=0, column=1, padx=5)

        ttk.Button(top_frame, text="Fetch Weather", command=self.handle_search).grid(row=0, column=2, padx=5)
        ttk.Button(top_frame, text="Save to Favorites", command=self.handle_save_favorite).grid(row=0, column=3, padx=5)

        ttk.Label(top_frame, text="Saved:").grid(row=0, column=4, padx=5)
        self.favorites_combo = ttk.Combobox(top_frame, state="readonly", width=15)
        self.favorites_combo.grid(row=0, column=5, padx=5)
        self.favorites_combo.bind("<<ComboboxSelected>>", self.handle_select_favorite)

        # Weather Metrics Frame
        self.info_frame = ttk.LabelFrame(self.root, text="Current Conditions", padding=10)
        self.info_frame.pack(fill=tk.X, padx=12, pady=4)

        self.info_label = ttk.Label(self.info_frame, text="Search for a city to display weather metrics.", font=("Helvetica", 10))
        self.info_label.pack(anchor=tk.W)

        # Matplotlib Canvas
        chart_frame = ttk.LabelFrame(self.root, text="24-Hour Temperature Trend", padding=10)
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=8)

        self.figure = Figure(figsize=(7, 3.5), dpi=100)
        self.plot_axis = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _load_saved_favorites(self):
        saved = self.storage.load_favorites()
        self.favorites_combo["values"] = saved
        if saved:
            self.favorites_combo.current(0)

    def handle_search(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a valid city name.")
            return
        self.update_weather_display(city)

    def handle_select_favorite(self, event=None):
        selected = self.favorites_combo.get()
        if selected:
            self.city_entry.delete(0, tk.END)
            self.city_entry.insert(0, selected)
            self.update_weather_display(selected)

    def handle_save_favorite(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Enter a city before saving.")
            return
        if self.storage.save_favorite(city):
            self._load_saved_favorites()
            messagebox.showinfo("Saved", f"'{city.title()}' added to favorites.")
        else:
            messagebox.showinfo("Info", f"'{city.title()}' is already in favorites.")

    def update_weather_display(self, city: str):
        try:
            report = self.fetcher.get_current_weather(city)
            self.info_label.config(
                text=f"{report.city}, {report.country} | Temp: {report.temp:.1f} °C (Feels like {report.feels_like:.1f} °C) | "
                     f"{report.condition}\nHumidity: {report.humidity}% | Pressure: {report.pressure} hPa | Wind: {report.wind_speed} m/s"
            )

            times, temps = self.fetcher.get_forecast(city)
            self.plot_axis.clear()
            self.plot_axis.plot(times, temps, marker="o", color="#1f77b4", linewidth=2)
            self.plot_axis.set_title(f"Next 24h Temperature (°C) - {report.city}")
            self.plot_axis.set_ylabel("Celsius")
            self.plot_axis.grid(True, linestyle="--", alpha=0.5)
            self.figure.tight_layout()
            self.canvas.draw()

        except (ValueError, ConnectionError) as err:
            messagebox.showerror("Error", str(err))
import tkinter as tk
from tkinter import ttk, messagebox
import math
import time
from datetime import datetime


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator with Clock")
        self.root.geometry("500x700")
        self.root.resizable(False, False)

        self.current_input = tk.StringVar(value="0")
        self.operation = ""
        self.first_number = 0
        self.clock_type = tk.StringVar(value="digital")
        self.theme = tk.StringVar(value="light")
        self.mode = tk.StringVar(value="standard")
        self.max_digits = 14
        self.rad_mode = False

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12))

        self.create_menu_frame()
        self.create_clock_frame()
        self.create_display_frame()
        self.create_buttons_frame()

        self.apply_theme()
        self.update_clock()

        self.root.bind("<Key>", self.key_press)

    def create_menu_frame(self):
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(menu_frame, text="Clock Type:").pack(side=tk.LEFT, padx=5)
        clock_menu = ttk.OptionMenu(menu_frame, self.clock_type, "digital", "digital", "analog",
                                    command=lambda _: self.update_clock())
        clock_menu.pack(side=tk.LEFT, padx=5)

        tk.Label(menu_frame, text="Theme:").pack(side=tk.LEFT, padx=5)
        theme_menu = ttk.OptionMenu(menu_frame, self.theme, "light", "light", "dark", "blue", "green",
                                    command=lambda _: self.apply_theme())
        theme_menu.pack(side=tk.LEFT, padx=5)

        tk.Label(menu_frame, text="Mode:").pack(side=tk.LEFT, padx=5)
        mode_menu = ttk.OptionMenu(menu_frame, self.mode, "standard", "standard", "engineering",
                                   command=lambda _: self.change_calculator_mode())
        mode_menu.pack(side=tk.LEFT, padx=5)

        self.rad_button = ttk.Button(menu_frame, text="DEG", width=5,
                                     command=self.toggle_angle_mode)
        self.rad_button.pack(side=tk.RIGHT, padx=5)

    def create_display_frame(self):
        self.display_frame = tk.Frame(self.root, height=80)
        self.display_frame.pack(fill=tk.X, padx=10, pady=15)
        self.display_frame.pack_propagate(False)

        self.display = tk.Label(self.display_frame, textvariable=self.current_input,
                                font=("Arial", 36), anchor="e", bg="white")
        self.display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_clock_frame(self):
        self.clock_frame = tk.Frame(self.root, height=100, width=100)
        self.clock_frame.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=5)
        self.clock_frame.pack_propagate(False)

        self.digital_clock = tk.Label(self.clock_frame, font=("Arial", 16), text="")

        self.analog_clock = tk.Canvas(self.clock_frame, width=100, height=100, bg="white")

    def create_buttons_frame(self):
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.standard_buttons = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3),
            ("0", 3, 0), (".", 3, 1), ("=", 3, 2), ("+", 3, 3),
            ("C", 4, 0), ("CE", 4, 1), ("√", 4, 2), ("±", 4, 3)
        ]

        self.engineering_buttons = [
            ("sin", 0, 0), ("cos", 0, 1), ("tan", 0, 2), ("π", 0, 3), ("e", 0, 4),
            ("asin", 1, 0), ("acos", 1, 1), ("atan", 1, 2), ("log", 1, 3), ("ln", 1, 4),
            ("x²", 2, 0), ("x³", 2, 1), ("xʸ", 2, 2), ("10ˣ", 2, 3), ("eˣ", 2, 4),
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("/", 3, 3), ("(", 3, 4),
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("*", 4, 3), (")", 4, 4),
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("-", 5, 3), ("1/x", 5, 4),
            ("0", 6, 0), (".", 6, 1), ("=", 6, 2), ("+", 6, 3), ("√", 6, 4),
            ("C", 7, 0), ("CE", 7, 1), ("Del", 7, 2), ("±", 7, 3), ("mod", 7, 4)
        ]

        self.current_buttons = []
        self.display_standard_buttons()

    def display_standard_buttons(self):
        for button in self.current_buttons:
            button.destroy()
        self.current_buttons = []

        for i in range(5):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.buttons_frame.grid_columnconfigure(i, weight=1)

        for (text, row, col) in self.standard_buttons:
            button = ttk.Button(self.buttons_frame, text=text, style="TButton")
            button.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            button.bind("<Button-1>", self.button_click)
            self.current_buttons.append(button)

    def display_engineering_buttons(self):
        for button in self.current_buttons:
            button.destroy()
        self.current_buttons = []

        for i in range(8):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.buttons_frame.grid_columnconfigure(i, weight=1)

        for (text, row, col) in self.engineering_buttons:
            button = ttk.Button(self.buttons_frame, text=text, style="TButton")
            button.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            button.bind("<Button-1>", self.button_click)
            self.current_buttons.append(button)

    def change_calculator_mode(self):
        if self.mode.get() == "standard":
            self.display_standard_buttons()
        else:
            self.display_engineering_buttons()

    def button_click(self, event):
        button_text = event.widget["text"]

        if button_text in "0123456789.":
            self.handle_number_input(button_text)
        elif button_text in "+-*/()":
            self.handle_operation(button_text)
        elif button_text == "=":
            self.calculate_result()
        elif button_text == "C":
            self.current_input.set("0")
            self.operation = ""
            self.first_number = 0
        elif button_text == "CE":
            self.current_input.set("0")
        elif button_text == "Del":
            self.delete_last_char()
        elif button_text == "√":
            self.handle_square_root()
        elif button_text == "±":
            self.toggle_sign()
        elif button_text == "π":
            self.handle_constant(math.pi)
        elif button_text == "e":
            self.handle_constant(math.e)
        elif button_text == "sin":
            self.handle_trig_function(math.sin)
        elif button_text == "cos":
            self.handle_trig_function(math.cos)
        elif button_text == "tan":
            self.handle_trig_function(math.tan)
        elif button_text == "asin":
            self.handle_trig_function(math.asin)
        elif button_text == "acos":
            self.handle_trig_function(math.acos)
        elif button_text == "atan":
            self.handle_trig_function(math.atan)
        elif button_text == "log":
            self.handle_log(10)
        elif button_text == "ln":
            self.handle_log(math.e)
        elif button_text == "x²":
            self.handle_power(2)
        elif button_text == "x³":
            self.handle_power(3)
        elif button_text == "xʸ":
            self.handle_operation("^")
        elif button_text == "10ˣ":
            self.handle_exp_function(10)
        elif button_text == "eˣ":
            self.handle_exp_function(math.e)
        elif button_text == "1/x":
            self.handle_reciprocal()
        elif button_text == "mod":
            self.handle_operation("%")

    def handle_number_input(self, digit):
        current = self.current_input.get()

        if current == "0" and digit != ".":
            self.current_input.set(digit)
        elif digit == "." and "." in current:
            pass
        elif len(current) < self.max_digits or (current == "0" and digit == "."):
            self.current_input.set(current + digit)

        self.format_display()

    def handle_operation(self, op):
        self.first_number = float(self.current_input.get())
        self.operation = op
        self.current_input.set("0")

    def calculate_result(self):
        if not self.operation:
            return

        second_number = float(self.current_input.get())
        result = 0

        try:
            if self.operation == "+":
                result = self.first_number + second_number
            elif self.operation == "-":
                result = self.first_number - second_number
            elif self.operation == "*":
                result = self.first_number * second_number
            elif self.operation == "/":
                if second_number == 0:
                    messagebox.showerror("Error", "Cannot divide by zero!")
                    self.current_input.set("0")
                    return
                result = self.first_number / second_number
            elif self.operation == "^":
                result = self.first_number ** second_number
            elif self.operation == "%":
                result = self.first_number % second_number

            self.display_result(result)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.current_input.set("0")

        self.operation = ""

    def handle_square_root(self):
        try:
            number = float(self.current_input.get())
            if number < 0:
                messagebox.showerror("Error", "Nie można obliczyć pierwiastka z liczby ujemnej!")
                return

            result = math.sqrt(number)

            if result == int(result):
                self.current_input.set(str(int(result)))
            else:
                self.current_input.set(str(result))

        except Exception as e:
            messagebox.showerror("Error", f"Wystąpił błąd: {str(e)}")

    def toggle_sign(self):
        try:
            number = float(self.current_input.get())
            result = -number
            self.display_result(result)

        except Exception as e:
            messagebox.showerror("Error", f"Wystąpił błąd: {str(e)}")

    def delete_last_char(self):
        current = self.current_input.get()
        if len(current) > 1:
            self.current_input.set(current[:-1])
        else:
            self.current_input.set("0")

    def format_display(self):
        current = self.current_input.get()

        if len(current) > self.max_digits and "." not in current:
            self.current_input.set(current[:self.max_digits])
        elif "." in current and len(current) > self.max_digits + 1:
            decimal_pos = current.find(".")
            decimal_places = max(1, self.max_digits - decimal_pos)
            try:
                formatted = float(current)
                self.current_input.set(f"{formatted:.{decimal_places}f}")
            except:
                pass

    def display_result(self, result):
        if result == int(result):
            result_str = str(int(result))
        else:
            result_str = str(result)

        if len(result_str) > self.max_digits:
            self.current_input.set(f"{result:.{self.max_digits - 6}e}")
        else:
            self.current_input.set(result_str)

    def handle_constant(self, value):
        self.display_result(value)

    def handle_trig_function(self, func):
        try:
            value = float(self.current_input.get())

            if not self.rad_mode and func in [math.sin, math.cos, math.tan]:
                value = math.radians(value)

            result = func(value)
            self.display_result(result)

        except Exception as e:
            messagebox.showerror("Error", f"Błąd funkcji trygonometrycznej: {str(e)}")

    def handle_log(self, base):
        try:
            value = float(self.current_input.get())
            if value <= 0:
                messagebox.showerror("Error", "Argument logarytmu musi być dodatni!")
                return

            if base == math.e:
                result = math.log(value)
            else:
                result = math.log10(value)

            self.display_result(result)

        except Exception as e:
            messagebox.showerror("Error", f"Błąd funkcji logarytmicznej: {str(e)}")

    def handle_power(self, exponent):
        try:
            value = float(self.current_input.get())
            result = value ** exponent
            self.display_result(result)

        except Exception as e:
            messagebox.showerror("Error", f"Błąd potęgowania: {str(e)}")

    def handle_exp_function(self, base):
        try:
            exponent = float(self.current_input.get())
            result = base ** exponent
            self.display_result(result)

        except Exception as e:
            messagebox.showerror("Error", f"Błąd funkcji wykładniczej: {str(e)}")

    def handle_reciprocal(self):
        try:
            value = float(self.current_input.get())
            if value == 0:
                messagebox.showerror("Error", "Nie można dzielić przez zero!")
                return

            result = 1 / value
            self.display_result(result)

        except Exception as e:
            messagebox.showerror("Error", f"Błąd obliczania odwrotności: {str(e)}")

    def toggle_angle_mode(self):
        self.rad_mode = not self.rad_mode
        if self.rad_mode:
            self.rad_button.config(text="RAD")
        else:
            self.rad_button.config(text="DEG")

    def update_clock(self):
        current_time = datetime.now()

        if self.clock_type.get() == "digital":
            self.update_digital_clock(current_time)
        else:
            self.update_analog_clock(current_time)

        self.root.after(1000, self.update_clock)

    def update_digital_clock(self, current_time):
        formatted_time = current_time.strftime("%H:%M:%S")
        self.digital_clock.config(text=formatted_time)

        self.analog_clock.pack_forget()
        self.digital_clock.pack(expand=True)

    def update_analog_clock(self, current_time):
        self.digital_clock.pack_forget()
        self.analog_clock.pack(expand=True)

        self.analog_clock.delete("all")

        width, height = 100, 100
        center_x, center_y = width // 2, height // 2
        radius = min(center_x, center_y) - 10

        theme = self.theme.get()
        if theme == "dark":
            hour_color = "white"
            minute_color = "#8EB8E5"
            second_color = "#FF6B6B"
            text_color = "white"
            outline_color = "white"
            center_dot_color = "white"
        else:
            hour_color = "black"
            minute_color = "blue"
            second_color = "red"
            text_color = "black"
            outline_color = "black"
            center_dot_color = "black"

        self.analog_clock.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            outline=outline_color, width=2
        )

        for i in range(12):
            angle = math.radians(i * 30)
            x = center_x + (radius - 10) * math.sin(angle)
            y = center_y - (radius - 10) * math.cos(angle)
            self.analog_clock.create_text(x, y, text=str(i if i else 12), font=("Arial", 8), fill=text_color)

        hour = current_time.hour % 12
        minute = current_time.minute
        second = current_time.second

        hour_angle = math.radians((hour * 30) + (minute / 2))
        hour_x = center_x + (radius * 0.5) * math.sin(hour_angle)
        hour_y = center_y - (radius * 0.5) * math.cos(hour_angle)
        self.analog_clock.create_line(
            center_x, center_y, hour_x, hour_y,
            width=3, fill=hour_color
        )

        minute_angle = math.radians(minute * 6)
        minute_x = center_x + (radius * 0.7) * math.sin(minute_angle)
        minute_y = center_y - (radius * 0.7) * math.cos(minute_angle)
        self.analog_clock.create_line(
            center_x, center_y, minute_x, minute_y,
            width=2, fill=minute_color
        )

        second_angle = math.radians(second * 6)
        second_x = center_x + (radius * 0.8) * math.sin(second_angle)
        second_y = center_y - (radius * 0.8) * math.cos(second_angle)
        self.analog_clock.create_line(
            center_x, center_y, second_x, second_y,
            width=1, fill=second_color
        )

        self.analog_clock.create_oval(
            center_x - 3, center_y - 3,
            center_x + 3, center_y + 3,
            fill=center_dot_color
        )

    def apply_theme(self):
        theme = self.theme.get()

        if theme == "light":
            bg_color = "#f0f0f0"
            fg_color = "black"
            button_bg = "#e0e0e0"
            display_bg = "white"
        elif theme == "dark":
            bg_color = "#333333"
            fg_color = "white"
            button_bg = "#555555"
            display_bg = "#222222"
        elif theme == "blue":
            bg_color = "#e6f2ff"
            fg_color = "#003366"
            button_bg = "#b3d9ff"
            display_bg = "#f0f8ff"
        elif theme == "green":
            bg_color = "#e6ffe6"
            fg_color = "#006600"
            button_bg = "#b3ffb3"
            display_bg = "#f0fff0"

        self.root.config(bg=bg_color)

        self.style.configure("TButton", background=button_bg, foreground=fg_color)

        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg=bg_color)
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=bg_color, fg=fg_color)

        self.display.config(bg=display_bg, fg=fg_color)

        self.digital_clock.config(bg=bg_color, fg=fg_color)
        self.analog_clock.config(bg=display_bg)

        self.update_clock()

    def key_press(self, event):
        key = event.char

        if key in "0123456789.":
            self.handle_number_input(key)
        elif key in "+-*/()%^":
            self.handle_operation(key)
        elif event.keysym == "Return":
            self.calculate_result()
        elif event.keysym == "Escape":
            self.current_input.set("0")
            self.operation = ""
            self.first_number = 0
        elif event.keysym == "BackSpace":
            self.delete_last_char()
        elif key == "r":
            self.handle_square_root()
        elif key == "s":
            self.toggle_sign()
        elif key == "p":
            self.handle_constant(math.pi)
        elif key == "1":
            if event.state & 0x04:
                self.handle_trig_function(math.sin)
        elif key == "2":
            if event.state & 0x04:
                self.handle_trig_function(math.cos)
        elif key == "3":
            if event.state & 0x04:
                self.handle_trig_function(math.tan)


if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
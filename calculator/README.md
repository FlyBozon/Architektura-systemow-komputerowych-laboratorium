## Task 1
Using any programming language for PC-standard computers, write an application that utilizes graphical user interface (GUI) techniques. The interface should interactively communicate with the user via a monitor, keyboard, and mouse.

The application’s purpose can be freely chosen. Suggested ideas include a simple interactive game or a calculator with a clock. In both cases, it is recommended that some graphic elements be customizable by the user — e.g., selecting a "skin" for the calculator or choosing the colors and display type of the clock (analog or digital).

---

# Calculator with Clock (Tkinter GUI)

This project is a **graphical calculator application** built using **Python's Tkinter library**. It supports both **standard** and **engineering** (scientific) modes and includes a **real-time clock** that can be displayed in **digital** or **analog** format. Additionally, users can customize the calculator’s **theme** and **angle mode (DEG/RAD)**.

---

## Features

### Calculator Functions

- **Standard mode**:
  - Basic arithmetic: `+`, `-`, `*`, `/`
  - Additional ops: `±`, `√`, `%`, `^`, `1/x`, `C`, `CE`, `Del`
  - Decimal support, sign toggle, and result formatting

- **Engineering mode**:
  - Trigonometric functions: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`
  - Logarithmic: `log`, `ln`
  - Constants: `π`, `e`
  - Power operations: `x²`, `x³`, `xʸ`, `10ˣ`, `eˣ`
  - Modular arithmetic: `mod`
  - Parentheses support

### Clock Display

- **Digital Clock** – shows current system time in HH:MM:SS format
- **Analog Clock** – animated, stylized clock with moving hour, minute, and second hands

### Themes

Switch between:
- Light (default)
- Dark
- Blue
- Green

Each theme adjusts the background, button colors, text colors, and display panel for better user experience.

### Mode Switching

- **Standard** vs **Engineering** calculator layout
- **DEG/RAD Toggle** for trigonometric function input (Degrees by default)

### Keyboard Shortcuts

- `0-9`, `.`, `+`, `-`, `*`, `/`, `^`, `%` → standard input
- `Enter` → calculate result
- `Esc` → clear
- `Backspace` → delete last digit
- `r` → square root
- `s` → toggle sign
- `p` → insert π
- `Ctrl+1`, `Ctrl+2`, `Ctrl+3` → `sin`, `cos`, `tan`

---

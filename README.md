# Keystroke Diagnostics & Typing Analysis Logger

A lightweight, event-driven Python tool designed for local typing diagnostics, ergonomics analysis, and input habit monitoring. Built for educational exploration, typing speed evaluation, and hackathon demonstrations.

---

## Features

- **Real-Time Key Capture**: Monitors and logs user input events with millisecond-accurate timestamps.
- **Special Key Normalization**: Translates non-printable and navigation keys (`[SPACE]`, `[ENTER]`, `[BACKSPACE]`, `[SHIFT]`, `[CTRL]`, arrows, etc.) into clean human-readable tags.
- **Ergonomics & Typing Performance**:
  - **Estimated WPM**: Words Per Minute calculation based on standard formula `(characters / 5) / minutes`.
  - **Backspace Error Rate**: Calculates error correction percentage to evaluate typing accuracy and fatigue.
  - **Active Session Runtime**: Tracks exact active elapsed time.
- **Top 5 Key Frequency Analytics**: Visual terminal breakdown of the top 5 most frequently pressed keys.
- **Immediate Disk Flushing**: Flushes file buffers with `os.fsync` after each keystroke to prevent data loss on unexpected exits.
- **Local Storage Encryption**: Includes a custom XOR cipher that encrypts the session log (`keystrokes.log.enc`) upon session termination.
- **Clean Exit Mechanisms**: Stop the listener safely without leaving orphaned background threads by pressing `ESC`, `Ctrl + Shift + Q`, or `Ctrl + C`.

---

## Project Structure

```text
keylogger/
├── keylogger.py       # Main diagnostic listener & analytics script
├── requirements.txt   # Python package dependencies
├── .gitignore         # Ignores generated logs, bytecode, and virtual envs
└── README.md          # Project documentation
```

---

## Prerequisites

- **Python**: 3.8 or newer
- **Operating System**: Windows, Linux, or macOS *(Note: on Linux/macOS, accessibility/input monitoring permissions may be required)*

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/keylogger.git
   cd keylogger
   ```

2. **(Optional) Set up a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run the main script from your terminal:

```bash
python keylogger.py
```

### Controls

| Action | Key Combination |
|---|---|
| **Stop & Summarize** | `ESC` |
| **Alternative Exit** | `Ctrl` + `Shift` + `Q` |
| **Terminal Interrupt** | `Ctrl` + `C` |

---

## Sample Session Summary

When exiting, the application prints a comprehensive session summary:

```text
==================================================
         SESSION DIAGNOSTICS & SUMMARY
==================================================
Total Keystrokes   : 142
Active Runtime     : 24.50 seconds
Estimated WPM      : 69.6 WPM
Backspace Error Rate: 4.2%
--------------------------------------------------
Top 5 Most Pressed Keys:
  1. [SPACE]      :   28 presses  ####################
  2. e            :   18 presses  #############
  3. t            :   14 presses  ##########
  4. a            :   11 presses  ########
  5. [BACKSPACE]  :    6 presses  ####
==================================================
[+] Encrypted log created : keystrokes.log.enc (Custom XOR Cipher)
[✔] Done! Session completed safely.
```

---

## Output Files

| File | Description |
|---|---|
| `keystrokes.log` | Plaintext timestamped session log (ignored by Git) |
| `keystrokes.log.enc` | Encrypted output generated via custom XOR cipher (ignored by Git) |

---

## Security & Ethical Disclaimer

> [!IMPORTANT]
> **Educational & Authorized Use Only**
> This software is intended strictly for personal typing ergonomics analysis, accessibility diagnostics, educational research, and authorized developer testing. 
> 
> - Do **not** use this software on any system or machine where you do not have explicit authorization and consent.
> - Capturing keystrokes without user knowledge and consent violates privacy laws and computer crime regulations.
> - The author is not responsible for any misuse, unauthorized deployment, or damages resulting from the use of this software.

---

## License

This project is licensed under the [MIT License](LICENSE).

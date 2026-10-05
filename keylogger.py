"""
Local Keystroke Diagnostics & Typing Analysis Logger
Built for Hackathon / Learning & Vibe Coding

Requirements covered:
1. Log typed keys to 'keystrokes.log' with precise timestamps.
2. Translate non-printable keys ([SPACE], [ENTER], [BACKSPACE], [SHIFT], etc.).
3. Clean exit (Press ESC or Ctrl+Shift+Q or Ctrl+C) with stats summary.
4. Ergonomics: WPM (Words Per Minute) and Backspace Error Rate.
5. Analytics: Top 5 most pressed keys breakdown.
6. Local storage encryption: Custom XOR Cipher from scratch.
"""

import os
import sys
import time
from collections import Counter
from datetime import datetime
from pynput import keyboard

LOG_FILE = "keystrokes.log"
ENCRYPTED_FILE = "keystrokes.log.enc"

# Mapping for special/non-printable keys
SPECIAL_KEYS = {
    keyboard.Key.space: "[SPACE]",
    keyboard.Key.enter: "[ENTER]",
    keyboard.Key.backspace: "[BACKSPACE]",
    keyboard.Key.tab: "[TAB]",
    keyboard.Key.shift: "[SHIFT]",
    keyboard.Key.shift_l: "[SHIFT]",
    keyboard.Key.shift_r: "[SHIFT]",
    keyboard.Key.ctrl: "[CTRL]",
    keyboard.Key.ctrl_l: "[CTRL]",
    keyboard.Key.ctrl_r: "[CTRL]",
    keyboard.Key.alt: "[ALT]",
    keyboard.Key.alt_l: "[ALT]",
    keyboard.Key.alt_r: "[ALT]",
    keyboard.Key.alt_gr: "[ALT]",
    keyboard.Key.caps_lock: "[CAPS_LOCK]",
    keyboard.Key.delete: "[DELETE]",
    keyboard.Key.esc: "[ESC]",
    keyboard.Key.up: "[UP]",
    keyboard.Key.down: "[DOWN]",
    keyboard.Key.left: "[LEFT]",
    keyboard.Key.right: "[RIGHT]",
    keyboard.Key.home: "[HOME]",
    keyboard.Key.end: "[END]",
    keyboard.Key.page_up: "[PAGE_UP]",
    keyboard.Key.page_down: "[PAGE_DOWN]",
    keyboard.Key.insert: "[INSERT]",
}

# State variables for session statistics
key_counter = Counter()
total_keystrokes = 0
backspace_count = 0
start_time = None
log_handle = None
active_keys = set()


def get_key_name(key):
    """Translates a pynput key object into a clean readable string."""
    if key in SPECIAL_KEYS:
        return SPECIAL_KEYS[key]
    
    # Check if printable character
    if hasattr(key, "char") and key.char is not None:
        return key.char
    
    # Fallback for other special keys
    clean_name = str(key).replace("Key.", "").upper()
    return f"[{clean_name}]"


def encrypt_log_file(src_path, dst_path, secret_key="hackathon2026"):
    """
    Brownie Point: Custom XOR Cipher implementation from scratch.
    Takes the plaintext log file and creates an encrypted version.
    """
    try:
        with open(src_path, "rb") as f:
            data = f.read()

        key_bytes = secret_key.encode("utf-8")
        encrypted = bytearray()
        for i, byte in enumerate(data):
            encrypted.append(byte ^ key_bytes[i % len(key_bytes)])

        with open(dst_path, "wb") as f:
            f.write(encrypted)
        return True
    except Exception as e:
        print(f"Encryption failed: {e}")
        return False


def display_stats():
    """Prints typing diagnostics, WPM, error rate, and top keys."""
    global start_time, total_keystrokes, backspace_count, key_counter

    runtime = time.time() - start_time if start_time else 0
    minutes = runtime / 60.0 if runtime > 0 else 0

    # Standard WPM formula: (total characters / 5) / minutes
    wpm = (total_keystrokes / 5) / minutes if minutes > 0 else 0
    error_rate = (backspace_count / total_keystrokes * 100) if total_keystrokes > 0 else 0

    print("\n" + "=" * 50)
    print("         SESSION DIAGNOSTICS & SUMMARY")
    print("=" * 50)
    print(f"Total Keystrokes   : {total_keystrokes}")
    print(f"Active Runtime     : {runtime:.2f} seconds")
    print(f"Estimated WPM      : {wpm:.1f} WPM")
    print(f"Backspace Error Rate: {error_rate:.1f}%")
    print("-" * 50)
    print("Top 5 Most Pressed Keys:")
    top5 = key_counter.most_common(5)
    if top5:
        for rank, (k, count) in enumerate(top5, 1):
            bar = "#" * min(count, 25)
            print(f"  {rank}. {k:<12} : {count:>4} presses  {bar}")
    else:
        print("  No keystrokes recorded.")
    print("=" * 50)

    # Encrypt log file (Brownie point)
    if os.path.exists(LOG_FILE):
        if encrypt_log_file(LOG_FILE, ENCRYPTED_FILE):
            print(f"[+] Encrypted log created : {ENCRYPTED_FILE} (Custom XOR Cipher)")


def on_press(key):
    """Callback triggered on every keypress."""
    global start_time, total_keystrokes, backspace_count, log_handle

    # Initialize start time on first press
    if start_time is None:
        start_time = time.time()

    # Track active keys for combinations
    active_keys.add(key)

    # Exit sequence: ESC key OR Ctrl + Shift + Q
    is_ctrl = keyboard.Key.ctrl in active_keys or keyboard.Key.ctrl_l in active_keys or keyboard.Key.ctrl_r in active_keys
    is_shift = keyboard.Key.shift in active_keys or keyboard.Key.shift_l in active_keys or keyboard.Key.shift_r in active_keys
    is_q = False
    if hasattr(key, "char") and key.char and key.char.lower() == "q":
        is_q = True

    if key == keyboard.Key.esc or (is_ctrl and is_shift and is_q):
        print("\n[*] Clean exit triggered. Flushing buffers and stopping...")
        return False  # Stops the pynput listener

    # Format key and timestamp
    key_name = get_key_name(key)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    # Update stats
    total_keystrokes += 1
    key_counter[key_name] += 1
    if key_name == "[BACKSPACE]":
        backspace_count += 1

    # Write to local file with immediate buffer flush
    entry = f"[{timestamp}] {key_name}\n"
    log_handle.write(entry)
    log_handle.flush()
    try:
        os.fsync(log_handle.fileno())
    except Exception:
        pass

    # Live terminal display so user sees immediate feedback
    print(f"[{timestamp}] Logged: {key_name}")


def on_release(key):
    """Remove key from active keys set when released."""
    active_keys.discard(key)


def main():
    global log_handle, start_time

    print("=" * 55)
    print("  LOCAL KEYSTROKE MONITOR & TYPING DIAGNOSTICS")
    print("=" * 55)
    print(f"[i] Output Log     : {os.path.abspath(LOG_FILE)}")
    print("[i] Exit Hotkey    : Press ESC or Ctrl+Shift+Q at any time")
    print("[i] Status         : RUNNING & LISTENING...")
    print("=" * 55)
    print("Type anywhere on your system to test. Keystrokes will show below:\n")

    start_time = time.time()

    # Open log file in append mode
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        log_handle = f
        log_handle.write(f"\n--- SESSION STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        log_handle.flush()

        try:
            with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()
        except KeyboardInterrupt:
            print("\n[*] Interrupted via Ctrl+C.")
        finally:
            log_handle.write(f"--- SESSION ENDED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
            log_handle.flush()

    # Display session summary
    display_stats()
    print("[✔] Done! Session completed safely.\n")


if __name__ == "__main__":
    main()
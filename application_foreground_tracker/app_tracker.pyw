import sys
import subprocess
import importlib


# ==============================
# Install libraries if necessary
# ==============================

def install_if_missing(package, import_name=None):

    if import_name is None:
        import_name = package

    try:
        importlib.import_module(import_name)

    except ImportError:

        print(f"Installing {package}...")

        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            package
        ])


install_if_missing("pywin32", "win32gui")
install_if_missing("psutil")


# ==============================
# Imports
# ==============================

import csv
import time
from datetime import datetime

import win32gui
import win32process
import psutil


CSV_FILE = "app_usage.csv"
CHECK_INTERVAL = 0.5


# ==============================
# Get foreground application
# ==============================

def get_foreground_app():

    hwnd = win32gui.GetForegroundWindow()

    if not hwnd:
        return "Unknown"

    try:

        _, pid = win32process.GetWindowThreadProcessId(hwnd)

        process = psutil.Process(pid)

        return process.name()

    except (psutil.NoSuchProcess, psutil.AccessDenied):

        return "Unknown"


# ==============================
# Create CSV if necessary
# ==============================

def create_csv():

    try:

        with open(
            CSV_FILE,
            "x",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "application",
                "start_time",
                "end_time"
            ])

    except FileExistsError:

        pass


# ==============================
# Save completed session
# ==============================

def save_session(app, start_time, end_time):

    with open(
        CSV_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            app,
            start_time.strftime("%Y-%m-%d %H:%M:%S"),
            end_time.strftime("%Y-%m-%d %H:%M:%S")
        ])


# ==============================
# Main
# ==============================

def main():

    create_csv()

    print("Application tracker started.")
    print("Press Ctrl+C to stop.\n")

    # Get initial application
    current_app = get_foreground_app()

    # Start its session
    session_start = datetime.now()

    print(
        f"{session_start.strftime('%H:%M:%S')} "
        f"START: {current_app}"
    )


    try:

        while True:

            time.sleep(CHECK_INTERVAL)

            new_app = get_foreground_app()


            # ==============================
            # Foreground app changed
            # ==============================

            if new_app != current_app:

                session_end = datetime.now()


                # Save old application session
                save_session(
                    current_app,
                    session_start,
                    session_end
                )


                print(
                    f"{session_end.strftime('%H:%M:%S')} "
                    f"END:   {current_app}"
                )


                # Start new application session
                current_app = new_app

                session_start = session_end


                print(
                    f"{session_start.strftime('%H:%M:%S')} "
                    f"START: {current_app}\n"
                )


    except KeyboardInterrupt:

        # Save the session that was still running
        session_end = datetime.now()

        save_session(
            current_app,
            session_start,
            session_end
        )

        print("\nTracker stopped.")


if __name__ == "__main__":
    main()

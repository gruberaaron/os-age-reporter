#!/usr/bin/env python3
"""
OS Age Reporter

Description:
    This script calculates and reports the age of the operating system installation
    based on the creation time of the root directory. It can display the age in a
    human-readable format and optionally send this information via email.

Usage:
    ./os-age-reporter.py
    
    The script requires a configuration file at ~/.config/os-age-report/config.json
    with the following structure:
    {
        "email_subject": "OS Age Report",
        "email_sender": "sender@example.com",
        "email_recipient": ["recipient@example.com"],
        "smtp_server": "smtp.example.com",
        "smtp_port": 587,
        "smtp_username": "username",
        "smtp_password": "password"
    }

Author: 
    Aaron (Maintainer)

Date:
    2025-07-29

Changelog:
    2025-07-29 - Added documentation header with usage information, author, date, and changelog
    [Initial version] - Created script to report OS installation age
"""

import os
import json
import smtplib
import datetime
from email.message import EmailMessage


def load_config() -> dict:
    """
    Loads configuration from ~/.config/os-age-report/config.json.
    """
    home_dir = os.path.expanduser("~")
    # Construct the path to the configuration directory
    config_dir = os.path.join(home_dir, ".config", "os-age-report")
    config_path = os.path.join(config_dir, "config.json")

    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_path}")
        print("Please ensure the directory and file exist and are configured.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not parse {config_path}. Please check for syntax errors.")
        exit(1)

def get_install_date() -> datetime.datetime:
    """Gets the installation date of the OS."""
    try:
        install_timestamp = os.path.getmtime('/')
        return datetime.datetime.fromtimestamp(install_timestamp)
    except FileNotFoundError:
        print("Error: Could not determine the creation time of the root directory '/'.")
        exit(1)


def get_os_age_string(install_date: datetime.datetime) -> str:
    """Calculates the time difference and formats it into a readable string."""
    delta = datetime.datetime.now() - install_date
    total_seconds = int(delta.total_seconds())

    ss = total_seconds % 60
    mm = (total_seconds // 60) % 60
    hh = (total_seconds // 3600) % 24
    total_days = total_seconds // 86400

    months = total_days // 30
    weeks = (total_days % 30) // 7
    days = (total_days % 30) % 7

    return f"{months} Months {weeks} Weeks {days} Days {hh} Hours {mm} Minutes {ss} Seconds Since Install"


def check_and_send_email(message: str, config: dict):
    """Checks the timer and sends an email using the provided configuration."""
    home_dir = os.path.expanduser("~")
    timestamp_file = os.path.join(home_dir, ".os_age_last_email.txt")

    should_send = False
    try:
        with open(timestamp_file, 'r') as f:
            last_email_ts = float(f.read())
        if (datetime.datetime.now().timestamp() - last_email_ts) > (24 * 3600):
            should_send = True
    except (FileNotFoundError, ValueError):
        should_send = True

    if not should_send:
        print("Skipping email: An email has been sent in the last 24 hours.")
        return

    print("Attempting to send email...")
    try:
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = config['email_subject']
        msg['From'] = config['email_sender']
        msg['To'] = ", ".join(config['email_recipient'])

        with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
            server.starttls()
            server.login(config['smtp_username'], config['smtp_password'])
            server.send_message(msg)
            print("Email sent successfully!")

        with open(timestamp_file, 'w') as f:
            f.write(str(datetime.datetime.now().timestamp()))

    except Exception as e:
        print(f"Error: Failed to send email. {e}")


def main():
    """Main function to run the script."""
    config = load_config()
    install_date = get_install_date()
    age_message = get_os_age_string(install_date)

    check_and_send_email(age_message, config)

    print("\n--- OS Installation Age ---")
    print(age_message)
    print("---------------------------\n")

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
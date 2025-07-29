# OS Age Reporter

A Python utility that calculates and reports the age of your operating system installation based on the creation time of the root directory. The tool displays the age in a human-readable format and can optionally send this information via email.

## Features

- **OS Age Calculation**: Determines how long your operating system has been installed by checking the creation time of the root directory
- **Human-Readable Format**: Displays the age in months, weeks, days, hours, minutes, and seconds
- **Email Reporting**: Can send the OS age information via email
- **Rate Limiting**: Prevents sending emails more than once per 24 hours

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/gruberaaron/os-age-report.git
   cd os-age-report
   ```

2. Ensure you have Python 3 installed:
   ```
   python3 --version
   ```

3. Set up the configuration file:
   ```
   mkdir -p ~/.config/os-age-report
   cp config.json ~/.config/os-age-report/
   ```

4. Edit the configuration file with your email settings:
   ```
   nano ~/.config/os-age-report/config.json
   ```

## Usage

Run the script directly:

```
./os-age-reporter.py
```

The script will:
1. Calculate your OS installation age
2. Display it in the terminal
3. Optionally send this information via email (if configured)

## Configuration

The script requires a configuration file at `~/.config/os-age-report/config.json` with the following structure:

```json
{
  "email_subject": "OS Age Report",
  "email_sender": "sender@example.com",
  "email_recipient": "recipient@example.com",
  "smtp_server": "smtp.example.com",
  "smtp_port": 587,
  "smtp_username": "username",
  "smtp_password": "password"
}
```

### Configuration Parameters

| Parameter | Description |
|-----------|-------------|
| `email_subject` | Subject line for the email report |
| `email_sender` | Email address used as the sender |
| `email_recipient` | Email address(es) to receive the report |
| `smtp_server` | SMTP server address for sending email |
| `smtp_port` | SMTP server port |
| `smtp_username` | Username for SMTP authentication |
| `smtp_password` | Password for SMTP authentication |

## Author

Aaron (Maintainer)

## License

This project is open source and available under the [GNU General Public License v3.0](./LICENSE).

## Changelog

See the [CHANGELOG][changelog] file for details.

[changelog]: ./CHANGELOG.md
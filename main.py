import argparse
import smtplib
import yaml
from email.mime.text import MIMEText


# Configuration class to store email settings
class EmailConfig:
    def __init__(self, subject, body, sender, password, recipients):
        self.subject = subject
        self.body = body
        self.sender = sender
        self.password = password
        self.recipients = recipients

    @classmethod
    def from_yaml(cls, config_file):
        """Loads email configuration from a YAML file."""
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)['EmailConfig']
        return cls(
            config['Subject'],
            config['Body'],
            config['Sender'],
            config['Password'],
            config.get('DefaultRecipients', [])
        )


def send_email(config, recipients):
    """Sends an email using the provided configuration and recipients."""
    msg = MIMEText(config.body)
    msg['Subject'] = config.subject
    msg['From'] = config.sender
    msg['To'] = ', '.join(recipients)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 587) as smtp_server:
            smtp_server.login(config.sender, config.password)
            smtp_server.sendmail(config.sender, recipients, msg.as_string())
        print("Message sent!")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--recipient", required=True, type=str)
    # args = parser.parse_args()

    config = EmailConfig.from_yaml('configuration.yaml')
    # config.recipients.append(args.recipient)
    # config.recipients = list(set(config.recipients))  # Remove duplicates

    send_email(config, config.recipients)

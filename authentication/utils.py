from typing import Tuple, List
import re

email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


def check_emails(emails: List[str]) -> Tuple[List[str], List[str]]:
    emails = list(filter(None, emails))
    correct_emails = [
        email for email in emails if bool(re.fullmatch(email_regex, email))
    ]
    incorrect_emails = [email for email in emails if email not in correct_emails]

    return (correct_emails, incorrect_emails)

import csv
from gmail import SendMessage
import datetime
import html2text

def get_send_list(file):
    out = []
    with open(file, mode="r") as csvfile:
        reader = csv.reader(csvfile)
        for name, email in reader:
            out.append((name, email))
    return out

def get_appointments():
    return [
        ("July 4, 2023", "12:00pm", "123 Main St."),
        ("July 4, 2023", "2:00pm", "123 Main St."),
        ("July 5, 2023", "11:00am", "123 Main St."),
        ("July 5, 2023", "11:00am", "123 Main St."),
        ("September 21, 2023", "11:00am", "123 Main St."),
        ]

class Message():
    def __init__(self, subject, email, name, appointments, message_contents:str) -> None:
        appt_table = "<table><tr><th>Date</th><th>Time</th><th>Location</th></tr>"
        appt_table_plain = "Date        \tTime   \tLocation"

        for date, time, location in appointments:
            appt_table += f"<tr><td>{date}</td><td>{time}</td><td>{location}</td></tr>"
            appt_table_plain += f"\n{date:<12}\t{time:<7}\t{location}"
        appt_table += "</table>"
        appt_table_plain += "\n"

        self.subject = subject
        self.recipient = email
        self.html = message_contents.format(name=name, appt_table=appt_table)
        self.plain = html2text.html2text(self.html)
        # self.plain = f"Hello {name}, \nThis is a reminder about ... blah\n{appt_table_plain}"
    


def send_messages(sender, messages:list[Message]):

    for message in messages:
        SendMessage(sender, message.recipient, message.subject, message.html, message.plain)

def main():
    send_list = get_send_list("./send_list.csv")
    appointments = get_appointments()
    subject = f"Reminder {datetime.datetime.now()}"
    message_contents = """
Dear {name},<br>
<br>
I'm reaching out to let you know what appointment times are available over the next week.<br>
{appt_table}
You can schedule an appointment by clicking the links in the above table or by visiting my <a href="">website</a>.
<br><br>
Best,<br>
Will"""
    messages = []
    for recipient_name, recipient_email in send_list:
        messages.append(Message(subject, recipient_email, recipient_name, appointments, message_contents))
    send_messages("jack0york.dev@gmail.com", messages)

if __name__ == '__main__':
    main()
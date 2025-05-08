text = """
send_email(to_email="ghiripdkt2017@gmail.com", subject="Notification about schedule adjustment", content="Dear Ghiri,

I trust this message finds you well. I am writing to inform you that due to unforeseen circumstances, I will be unable to attend our scheduled meeting tomorrow.

I apologize for any inconvenience caused and appreciate your understanding in this matter. I will make sure to reschedule at a time that is suitable for both of us.

Please accept my sincere apologies once again. I look forward to speaking with you soon.

Best regards,
[Your Name]")


"""
import re

match = re.search(r'content\s*=\s*"((?:.|\n)*?)(?:Best regards,)', text)
print(match.group(1))
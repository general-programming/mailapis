import re
import hashlib
import os
import requests

def push_mail(mail_image, mail_raw, subject="[Blank subject]", sender="[Blank sender]", sent=None):
    # Sent date
    if not sent:
        sent = "[Missing mail time]"
    else:
        sent = str(sent)

    # Gravatar URL
    emails = re.findall(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", sender)

    if not emails:
        from_hash = "00000000000000000000000000000000"
    else:
        from_hash = hashlib.md5(emails[-1].encode("utf8").lower()).hexdigest()

    avatar_url = "https://www.gravatar.com/avatar/{from_hash}?default=identicon&s=256"

    r = requests.post(os.environ["DISCORD_WEBHOOK"], json={
        "avatar_url": avatar_url,
        "embeds": [
            {
                # Ass bleach pink
                "color": 0xffb9ec,
                "title": subject,
                "url": mail_raw,
                "author": {
                    "name": sender,
                    "url": mail_raw
                },
                "image": {
                    "url": mail_image,
                    "width": 1024
                },
                "footer": {
                    "text": sent
                }
            }
        ]
    })

    return r.status_code, r.text

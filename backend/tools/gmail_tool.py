class GmailTool:

    def __init__(self):
        self.emails = [
            {
                "email_id": "EMAIL-001",
                "customer": "ABC Ltd",
                "sender": "sales@abcltd.com",
                "subject": "Quotation Request",
                "body": "Please send us a quotation.",
                "attachment": "quotation.pdf"
            }
        ]

    def read_email(self):

        print("\n📧 Gmail Mock")
        print("Reading latest customer email...")

        if not self.emails:
            return {
                "success": False,
                "error": "No emails found."
            }

        email = self.emails[0]

        print(f"   Sender: {email['sender']}")
        print(f"   Subject: {email['subject']}")
        print(f"   Attachment: {email['attachment']}")

        return {
            "success": True,
            "email_id": email["email_id"],
            "customer": email["customer"],
            "sender": email["sender"],
            "subject": email["subject"],
            "body": email["body"],
            "attachment": email["attachment"]
        }

    def download_attachment(self, filename):

        print("\n📎 Gmail Mock")
        print(f"Downloading attachment: {filename}")

        return {
            "success": True,
            "filename": filename,
            "status": "downloaded",
            "path": f"/mock_workspace/{filename}"
        }
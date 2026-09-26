class SlackTool:
    def __init__(self):
        self.messages = []

    def send_message(self, channel, message):

        print("\n💬 Slack Mock")
        print("Channel:", channel)
        print("Message:", message)

        self.messages.append({
            "channel": channel,
            "message": message
        })

        return {
            "success": True,
            "channel": channel,
            "status": "sent",
            "message": message
        }
from backend.workflow.repetition_detector import RepetitionDetector

print("Starting repetition detector test...")


sessions = [
    [
        "application_focus",
        "open_email",
        "mouse_click",
        "download_attachment",
        "search_customer",
        "update_customer",
        "send_slack"
    ],

    [
        "open_email",
        "keyboard_type",
        "download_attachment",
        "crm_find_customer",
        "crm_edit_customer",
        "slack_message"
    ],

    [
        "gmail_open_email",
        "gmail_download",
        "crm_search_customer",
        "crm_update_customer",
        "slack_send_message"
    ],

    [
        "open_email",
        "reply_email",
        "send_email"
    ]
]


print("Creating detector...")

detector = RepetitionDetector(
    min_repetitions=2,
    similarity_threshold=0.70
)


print("Detecting...")


result = detector.detect(sessions)


print("\nRESULT:")
print(result)


if result:
    detector.display_result(result)
else:
    print("\n❌ No repeated workflow detected.")
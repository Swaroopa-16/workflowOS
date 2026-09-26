from backend.tools.gmail_tool import GmailTool
from backend.tools.crm_tool import CRMTool
from backend.tools.slack_tool import SlackTool


print("\n" + "=" * 60)
print("🧪 TESTING WORKFLOWOS MOCK APPLICATIONS")
print("=" * 60)


# Gmail
gmail = GmailTool()

email = gmail.read_email()

print("\nGmail Result:")
print(email)

attachment = gmail.download_attachment(
    "quotation.pdf"
)

print("\nAttachment Result:")
print(attachment)


# CRM
crm = CRMTool()

customer = crm.search_customer(
    "ABC Ltd"
)

print("\nCRM Search Result:")
print(customer)


update = crm.update_customer(

    customer_id="CRM-001",

    request="New quotation required",

    attachment="quotation.pdf"
)

print("\nCRM Update Result:")
print(update)


# Slack
slack = SlackTool()

message = slack.send_message(

    channel="#customer-ops",

    message=(
        "Processed quotation request "
        "for ABC Ltd."
    )
)

print("\nSlack Result:")
print(message)


print("\n" + "=" * 60)
print("✅ ALL MOCK APPLICATIONS WORKING")
print("=" * 60)
class CRMTool:

    def __init__(self):

        self.customers = [
            {
                "customer_id": "CRM-001",
                "name": "ABC Ltd",
                "email": "sales@abcltd.com",
                "status": "Active"
            },
            {
                "customer_id": "CRM-002",
                "name": "XYZ Corporation",
                "email": "contact@xyz.com",
                "status": "Active"
            }
        ]

    def search_customer(self, customer):

        print("\n🔎 CRM Mock")
        print(
            f"Searching customer: {customer}"
        )

        for record in self.customers:

            if record["name"].lower() == customer.lower():

                print(
                    f"   ✅ Customer found: "
                    f"{record['customer_id']}"
                )

                return {
                    "success": True,
                    "found": True,
                    "customer_id":
                        record["customer_id"],
                    "customer":
                        record["name"],
                    "email":
                        record["email"]
                }

        print(
            "   ❌ Customer not found."
        )

        return {
            "success": False,
            "found": False,
            "customer": customer,
            "error":
                f"Customer '{customer}' was not found in CRM."
        }

    def update_customer(
        self,
        customer_id,
        request,
        attachment
    ):

        print("\n📝 CRM Mock")

        print(
            f"Updating customer: {customer_id}"
        )

        for record in self.customers:

            if record["customer_id"] == customer_id:

                record["last_request"] = request

                record["attachment"] = attachment

                record["workflow_status"] = (
                    "Quotation Request Processed"
                )

                print(
                    "   ✅ Customer record updated."
                )

                return {
                    "success": True,
                    "customer_id": customer_id,
                    "status": "updated",
                    "request": request,
                    "attachment": attachment
                }

        print(
            "   ❌ Customer ID not found."
        )

        return {
            "success": False,
            "error":
                f"Customer ID '{customer_id}' not found."
        }
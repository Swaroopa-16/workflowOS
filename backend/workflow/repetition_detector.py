import difflib


class RepetitionDetector:

    # Actions that should not influence repetition detection
    NOISE_ACTIONS = {
        "mouse_move",
        "mouse_click",
        "keyboard_input",
        "window_focus",
        "scroll",
        "idle",
    }

    # Equivalent action names
    NORMALIZATION_MAP = {
        "read_email": "gmail_read_email",
        "gmail_read": "gmail_read_email",

        "download_attachment": "gmail_download_attachment",
        "gmail_download": "gmail_download_attachment",

        "search_customer": "crm_search_customer",
        "crm_search": "crm_search_customer",

        "update_customer": "crm_update_customer",
        "crm_update": "crm_update_customer",

        "send_message": "slack_send_message",
        "slack_send": "slack_send_message",
    }

    def normalize_action(self, action):
        """
        Convert different action names into a standard form.
        """

        if not action:
            return None

        action = str(action).strip().lower()

        if action in self.NOISE_ACTIONS:
            return None

        return self.NORMALIZATION_MAP.get(action, action)

    def normalize_session(self, session):
        """
        Extract actions from different session formats.

        Supports:

        [
            "gmail_read_email",
            "crm_search_customer"
        ]

        OR:

        {
            "session_id": "...",
            "activities": [
                {"application": "Gmail", "action": "gmail_read_email"}
            ]
        }
        """

        actions = []

        # -----------------------------------------
        # Session is a dictionary
        # -----------------------------------------
        if isinstance(session, dict):

            # Normal WorkFlowOS observer format
            if "activities" in session:

                activities = session.get("activities", [])

                for activity in activities:

                    if isinstance(activity, dict):

                        action = activity.get("action")

                    else:

                        action = activity

                    normalized = self.normalize_action(action)

                    if normalized:
                        actions.append(normalized)

            # Alternative format
            elif "actions" in session:

                for action in session.get("actions", []):

                    if isinstance(action, dict):
                        action = action.get("action")

                    normalized = self.normalize_action(action)

                    if normalized:
                        actions.append(normalized)

        # -----------------------------------------
        # Session is a list
        # -----------------------------------------
        elif isinstance(session, list):

            for item in session:

                if isinstance(item, dict):
                    action = item.get("action")
                else:
                    action = item

                normalized = self.normalize_action(action)

                if normalized:
                    actions.append(normalized)

        return actions

    def similarity(self, sequence_a, sequence_b):
        """
        Calculate similarity between two action sequences.
        """

        if not sequence_a or not sequence_b:
            return 0.0

        return difflib.SequenceMatcher(
            None,
            sequence_a,
            sequence_b
        ).ratio()

    def find_similar_sessions(
        self,
        sessions,
        similarity_threshold=0.75
    ):
        """
        Find sessions containing similar workflows.
        """

        normalized_sessions = []

        for session in sessions:

            sequence = self.normalize_session(session)

            if sequence:
                normalized_sessions.append(sequence)

        if len(normalized_sessions) < 2:
            return {
                "occurrences": 0,
                "average_similarity": 0.0,
                "sessions": []
            }

        similar_sessions = []

        for i in range(len(normalized_sessions)):

            for j in range(i + 1, len(normalized_sessions)):

                similarity = self.similarity(
                    normalized_sessions[i],
                    normalized_sessions[j]
                )

                if similarity >= similarity_threshold:

                    similar_sessions.append(
                        (
                            normalized_sessions[i],
                            normalized_sessions[j],
                            similarity
                        )
                    )

        if not similar_sessions:

            return {
                "occurrences": 0,
                "average_similarity": 0.0,
                "sessions": []
            }

        average_similarity = sum(
            item[2]
            for item in similar_sessions
        ) / len(similar_sessions)

        # Keep unique sequences
        unique_sessions = []

        for sequence in normalized_sessions:

            if sequence not in unique_sessions:
                unique_sessions.append(sequence)

        return {
            "occurrences": len(similar_sessions) + 1,
            "average_similarity": average_similarity,
            "sessions": unique_sessions
        }

    def detect(self, sessions):

        result = self.find_similar_sessions(sessions)

        if result["occurrences"] < 2:
            return None

        # Use the first repeated sequence as the detected workflow
        sequence = result["sessions"][0]

        return {
            "sequence": sequence,
            "occurrences": result["occurrences"],
            "average_similarity": result["average_similarity"],
            "sessions": result["sessions"]
        }

    def is_repeated(self, sessions):

        result = self.detect(sessions)

        return result is not None

    def display_result(self, result):

        print("\n" + "=" * 60)
        print("🔍 REPETITION DETECTION RESULT")
        print("=" * 60)

        if not result:

            print("\n❌ No repeated workflow detected.")
            return

        print(
            f"\nOccurrences: "
            f"{result['occurrences']}"
        )

        print(
            f"Average Similarity: "
            f"{result['average_similarity']:.2f}"
        )

        print("\nDetected Workflow:")

        for index, action in enumerate(
            result["sequence"],
            start=1
        ):

            print(
                f"  [{index}] {action}"
            )

        print("=" * 60)
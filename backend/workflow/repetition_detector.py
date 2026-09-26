from difflib import SequenceMatcher


class RepetitionDetector:

    NOISE_ACTIONS = {
        "mouse_move",
        "mouse_click",
        "keyboard_type",
        "keyboard_press",
        "window_focus",
        "application_focus",
        "scroll",
        "cursor_move",
    }

    NORMALIZATION_MAP = {
        "open_email": "gmail_read_email",
        "read_email": "gmail_read_email",
        "gmail_open_email": "gmail_read_email",

        "download_attachment": "gmail_download_attachment",
        "gmail_download": "gmail_download_attachment",

        "search_customer": "crm_search_customer",
        "crm_find_customer": "crm_search_customer",

        "update_customer": "crm_update_customer",
        "crm_edit_customer": "crm_update_customer",

        "send_slack": "slack_send_message",
        "slack_message": "slack_send_message",
    }

    def __init__(
        self,
        min_repetitions=2,
        similarity_threshold=0.70
    ):
        self.min_repetitions = min_repetitions
        self.similarity_threshold = similarity_threshold

    def normalize_action(self, action):

        if not action:
            return None

        action = action.strip().lower()

        if action in self.NOISE_ACTIONS:
            return None

        return self.NORMALIZATION_MAP.get(
            action,
            action
        )

    def normalize_session(self, session):

        normalized = []

        for action in session:

            action = self.normalize_action(action)

            if action is None:
                continue

            # Remove consecutive duplicate actions
            if normalized and normalized[-1] == action:
                continue

            normalized.append(action)

        return normalized

    def similarity(self, sequence_a, sequence_b):

        if not sequence_a or not sequence_b:
            return 0.0

        return SequenceMatcher(
            None,
            sequence_a,
            sequence_b
        ).ratio()

    def find_similar_sessions(self, sessions):

        groups = []

        for session in sessions:

            normalized = self.normalize_session(session)

            if not normalized:
                continue

            added_to_group = False

            for group in groups:

                representative = group[0]

                score = self.similarity(
                    normalized,
                    representative
                )

                if score >= self.similarity_threshold:

                    group.append(normalized)
                    added_to_group = True
                    break

            if not added_to_group:
                groups.append([normalized])

        return groups

    def detect(self, sessions):

        if not sessions:
            return None

        groups = self.find_similar_sessions(sessions)

        repeated_groups = [
            group
            for group in groups
            if len(group) >= self.min_repetitions
        ]

        if not repeated_groups:
            return None

        repeated_groups.sort(
            key=len,
            reverse=True
        )

        group = repeated_groups[0]

        representative = group[0]

        similarities = [
            self.similarity(
                representative,
                sequence
            )
            for sequence in group
        ]

        average_similarity = (
            sum(similarities) / len(similarities)
        )

        return {
            "sequence": representative,
            "occurrences": len(group),
            "average_similarity": round(
                average_similarity,
                2
            ),
            "sessions": group,
        }

    def is_repeated(self, sessions):

        return self.detect(sessions) is not None

    def display_result(self, result):

        if not result:
            print("\n❌ No repeated workflow detected.")
            return

        print("\n" + "=" * 55)
        print("🔔 REPEATED WORKFLOW DETECTED")
        print("=" * 55)

        print(
            f"\nOccurrences: {result['occurrences']}"
        )

        print(
            f"Similarity: "
            f"{result['average_similarity'] * 100:.0f}%"
        )

        print("\nDetected workflow:")

        for index, action in enumerate(
            result["sequence"],
            start=1
        ):
            print(f"  {index}. {action}")

        print("\n" + "=" * 55)
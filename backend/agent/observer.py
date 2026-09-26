import json
from pathlib import Path
from datetime import datetime


class ActivityObserver:

    def __init__(self, storage_path=None):

        if storage_path is None:

            root_dir = (
                Path(__file__)
                .resolve()
                .parent
                .parent
                .parent
            )

            storage_path = (
                root_dir
                / "data"
                / "activity_logs.json"
            )

        self.storage_path = Path(
            storage_path
        )

        self.storage_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.current_session = None

        self.sessions = self._load_sessions()

    # ==========================================================
    # LOAD / SAVE
    # ==========================================================

    def _load_sessions(self):

        if not self.storage_path.exists():

            return []

        try:

            with open(
                self.storage_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

                if isinstance(data, list):
                    return data

                if isinstance(data, dict):

                    return data.get(
                        "sessions",
                        []
                    )

        except Exception as error:

            print(
                f"⚠️ Could not load activity logs: "
                f"{error}"
            )

        return []

    def _save_sessions(self):

        with open(
            self.storage_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.sessions,
                file,
                indent=2
            )

    # ==========================================================
    # SESSION
    # ==========================================================

    def start_session(self, session_name=None):

        session = {

            "session_id":
                f"session-{len(self.sessions) + 1}",

            "name":
                session_name or "User Session",

            "started_at":
                datetime.now().isoformat(),

            "ended_at":
                None,

            "activities": []
        }

        self.current_session = session

        print(
            f"\n🟢 Activity session started: "
            f"{session['session_id']}"
        )

        return session

    def end_session(self):

        if self.current_session is None:

            return None

        self.current_session[
            "ended_at"
        ] = datetime.now().isoformat()

        self.sessions.append(
            self.current_session
        )

        self._save_sessions()

        session = self.current_session

        self.current_session = None

        print(
            f"\n🔴 Activity session ended: "
            f"{session['session_id']}"
        )

        return session

    # ==========================================================
    # RECORD ACTIVITY
    # ==========================================================

    def record_activity(
        self,
        application,
        action,
        details=None
    ):

        if self.current_session is None:

            self.start_session()

        activity = {

            "timestamp":
                datetime.now().isoformat(),

            "application":
                application,

            "action":
                action,

            "details":
                details or {}
        }

        self.current_session[
            "activities"
        ].append(activity)

        return activity

    # ==========================================================
    # CONVENIENCE METHODS
    # ==========================================================

    def record_gmail_action(
        self,
        action,
        details=None
    ):

        return self.record_activity(
            "Gmail",
            action,
            details
        )

    def record_crm_action(
        self,
        action,
        details=None
    ):

        return self.record_activity(
            "CRM",
            action,
            details
        )

    def record_slack_action(
        self,
        action,
        details=None
    ):

        return self.record_activity(
            "Slack",
            action,
            details
        )

    # ==========================================================
    # MOCK SESSION
    # ==========================================================

    def load_mock_session(
        self,
        actions
    ):

        session = self.start_session(
            "Mock User Session"
        )

        for item in actions:

            if isinstance(item, str):

                self.record_activity(
                    "Application",
                    item
                )

            elif isinstance(item, dict):

                self.record_activity(

                    item.get(
                        "application",
                        "Application"
                    ),

                    item.get(
                        "action",
                        "unknown"
                    ),

                    item.get(
                        "details",
                        {}
                    )
                )

        return self.end_session()

    # ==========================================================
    # GET ACTIVITIES
    # ==========================================================

    def get_current_session(self):

        return self.current_session

    def get_sessions(self):

        return self.sessions

    def get_action_sequence(
        self,
        session=None
    ):

        session = (
            session
            or self.current_session
        )

        if not session:

            return []

        activities = session.get(
            "activities",
            []
        )

        return [
            activity.get(
                "action"
            )
            for activity in activities
        ]

    def clear(self):

        self.sessions = []

        self.current_session = None

        self._save_sessions()
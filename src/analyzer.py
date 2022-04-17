class Analyzer:
    """
    This class ingests/parses log lines, while keeping the log flow's tail.

    Attributes
    ----------
    _sessions: dict
        list of sessions indexed by the session's id

    Methods
    -------
    ingest_line(line: str) -> None:
        Ingests the line based on a pre-defined log_format.
        TODO:
          - Make the log_format customizable;
          - Split the parser into another class or module;
          - Validate timestamp format;
    get_session(session_id: str) -> dict:
        Gets a single session's tail
    get_all_sessions_string(only_failed: bool = False:
        Gets all the sessions' tail separated by "---" as a string
        TODO:
          - Make the separator a parameter

    """

    _sessions: dict

    def __init__(self):
        self._sessions = {}

    def ingest_line(self, line: str) -> None:
        line_split = line.split(" ", 3)
        line_object = {
            "timestamp": f"{line_split[0]} {line_split[1]}",
            "message": line_split[3],
        }

        session = self._sessions.setdefault(
            line_split[2],
            {
                "failed": False,
                "logs": [],
            },
        )
        session["logs"].append(line_object)

        if line_object["message"].startswith("ERROR:"):
            session["failed"] = True
        if len(session["logs"]) > 4:
            session["logs"].pop(0)

    def get_session(self, session_id: str) -> dict:
        return self._sessions[session_id]

    def get_all_sessions_string(self, only_failed: bool = False):
        result = ""
        for session_id, session in self._sessions.items():
            if not only_failed or session["failed"]:
                """
                    If only_failed is False, this is always True - gets all sessions;
                    If only_failed is True, the session has to be marked as failed
                    for the condition to be True.
                """
                result += "".join(
                    [
                        f"{log['timestamp']} {session_id} {log['message']}"
                        for log in session["logs"]
                    ]
                )
                result += "---\n"
        return result

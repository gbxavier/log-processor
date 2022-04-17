class Parser:

    _sessions: dict

    def __init__(self):
        self._sessions = {}

    def parse_line(self, line: str):
        line_split = line.split(" ", 3)
        session = self._sessions.setdefault(line_split[2], [])
        session.append(
            {
                "timestamp": f"{line_split[0]} {line_split[1]}",
                "message": line_split[3],
            }
        )
        if len(session) > 4:
            session.pop(0)

    def get_session(self, session_id: str):
        return self._sessions[session_id]

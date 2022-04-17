import pytest

from src.analyzer import Analyzer


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "2019-4-02 07:31:30 [007] User1 logs in",
            [{"timestamp": "2019-4-02 07:31:30", "message": "User1 logs in"}],
        ),
        (
            "2019-4-1 13:32:40 [190] User3 logs in",
            [{"timestamp": "2019-4-1 13:32:40", "message": "User3 logs in"}],
        ),
    ],
)
def test_correct_format(test_input, expected):
    p = Analyzer()
    p.ingest_line(test_input)
    assert p.get_session(test_input.split(" ", 3)[2]) == expected


@pytest.mark.parametrize(
    "test_input",
    [
        "",
        "2019-4-02 07:31:30",
    ],
)
def test_fail_incorrect_format(test_input):
    p = Analyzer()
    with pytest.raises(IndexError):
        p.ingest_line(test_input)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            ["2019-4-02 07:31:30 [123] User123 logs in"],
            "2019-4-02 07:31:30 [123] User123 logs in\n---\n",
        ),
        (
            [
                "2019-4-1 13:32:40 [481] User4 logs in",
                "2019-4-1 13:32:40 [481] User4 logs out",
            ],
            "2019-4-1 13:32:40 [481] User4 logs in\n2019-4-1 13:32:40 [481] User4 logs out\n---\n",
        ),
        (
            [
                "2019-4-1 13:32:40 [481] User4 logs in",
                "2019-4-1 13:32:40 [007] User4 logs in",
            ],
            "2019-4-1 13:32:40 [481] User4 logs in\n---\n2019-4-1 13:32:40 [007] User4 logs in\n---\n",
        ),
        (
            [
                "2019-4-1 13:32:40 [481] User4 logs in",
                "2019-4-1 13:32:40 [007] User4 logs in",
                "2019-4-1 13:32:40 [481] User4 logs out",
                "2019-4-1 13:32:40 [007] User4 logs out",
            ],
            (
                "2019-4-1 13:32:40 [481] User4 logs in\n"
                "2019-4-1 13:32:40 [481] User4 logs out\n"
                "---\n"
                "2019-4-1 13:32:40 [007] User4 logs in\n"
                "2019-4-1 13:32:40 [007] User4 logs out\n"
                "---\n"
            ),
        ),
    ],
    ids=[
        "Single line",
        "Multiple lines same session_id",
        "Single Line different sessions",
        "Multiple Lines different sessions",
    ],
)
def test_get_all_sessions_string(test_input, expected):
    p = Analyzer()
    for item in test_input:
        p.ingest_line(item)
    assert p.get_all_sessions_string() == expected

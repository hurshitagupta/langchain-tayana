from trace import summary


def test_summary_success():
    traces = [
        {
            "success": True,
            "total_tokens": 20,
            "ms": 100
        },
        {
            "success": True,
            "total_tokens": 30,
            "ms": 200
        }
    ]

    result = summary(traces)

    assert result["runs"] == 2
    assert result["successful"] == 2
    assert result["total_tokens"] == 50


def test_summary_failure_count():
    traces = [
        {
            "success": True,
            "total_tokens": 20,
            "ms": 100
        },
        {
            "success": False,
            "total_tokens": 0,
            "ms": 50
        }
    ]

    result = summary(traces)

    assert result["failed"] == 1
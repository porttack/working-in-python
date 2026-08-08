OK_FORMAT = True

test = {
    "name": "q_exception",
    "points": None,
    "suites": [
        {
            "cases": [
                {
                    "code": (
                        ">>> safe_divide(1, 0)\n"
                        "Traceback (most recent call last):\n"
                        "    ...\n"
                        "ZeroDivisionError: division by zero\n"
                    ),
                    "hidden": False,
                    "locked": False,
                }
            ],
            "scored": True,
            "setup": "",
            "teardown": "",
            "type": "doctest",
        }
    ],
}

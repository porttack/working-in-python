OK_FORMAT = True

test = {
    "name": "q_multiline",
    "points": None,
    "suites": [
        {
            "cases": [
                {
                    "code": (">>> print(greeting)\n" "Hello,\n" "world!\n"),
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

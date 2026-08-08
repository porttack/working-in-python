OK_FORMAT = True

test = {
    "name": "q_multi_case",
    "points": None,
    "suites": [
        {
            "cases": [
                {
                    "code": ">>> square(3)\n9\n",
                    "hidden": False,
                    "locked": False,
                },
                {
                    "code": ">>> this_name_does_not_exist_anywhere(3)\n9\n",
                    "hidden": False,
                    "locked": False,
                },
                {
                    "code": ">>> square(4)\n16\n",
                    "hidden": False,
                    "locked": False,
                },
            ],
            "scored": True,
            "setup": "",
            "teardown": "",
            "type": "doctest",
        }
    ],
}

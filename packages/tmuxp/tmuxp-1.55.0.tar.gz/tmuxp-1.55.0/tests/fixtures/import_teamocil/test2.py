"""Teamocil data fixtures for import_teamocil tests, 2nd test."""

from __future__ import annotations

from tests.fixtures import utils as test_utils

teamocil_yaml = test_utils.read_workspace_file("import_teamocil/test2.yaml")
teamocil_dict = {
    "windows": [
        {
            "name": "sample-four-panes",
            "root": "~/Code/sample/www",
            "layout": "tiled",
            "panes": [{"cmd": "pwd"}, {"cmd": "pwd"}, {"cmd": "pwd"}, {"cmd": "pwd"}],
        },
    ],
}

expected = {
    "session_name": None,
    "windows": [
        {
            "window_name": "sample-four-panes",
            "layout": "tiled",
            "start_directory": "~/Code/sample/www",
            "panes": [
                {"shell_command": "pwd"},
                {"shell_command": "pwd"},
                {"shell_command": "pwd"},
                {"shell_command": "pwd"},
            ],
        },
    ],
}

from typing import Any

from src.features.discord.keys import MANAGE_GUILD

_STRING = 3
_CHANNEL = 7
_SUB_COMMAND = 1

_TYPE_CHOICES = [
    {"name": "qur'anic", "value": "quranic"},
    {"name": "prophetic", "value": "prophetic"},
    {"name": "athar", "value": "athar"},
    {"name": "custom", "value": "custom"},
]

_CONTENT_CHOICES = [
    {"name": "daily prayer", "value": "daily"},
    {"name": "random prayer", "value": "random"},
    {"name": "from a category", "value": "category"},
]


def command_definitions() -> list[dict[str, Any]]:
    return [
        {"name": "daily", "description": "Show today's prayer of the day"},
        {
            "name": "random",
            "description": "Get a random du'a",
            "options": [
                {
                    "name": "category",
                    "description": "Filter by category",
                    "type": _STRING,
                    "required": False,
                    "autocomplete": True,
                },
                {
                    "name": "type",
                    "description": "Filter by type",
                    "type": _STRING,
                    "required": False,
                    "choices": _TYPE_CHOICES,
                },
            ],
        },
        {
            "name": "search",
            "description": "Search the du'as",
            "options": [
                {
                    "name": "query",
                    "description": "What to search for",
                    "type": _STRING,
                    "required": True,
                },
                {
                    "name": "category",
                    "description": "Filter by category",
                    "type": _STRING,
                    "required": False,
                    "autocomplete": True,
                },
            ],
        },
        {
            "name": "submit",
            "description": "Submit a new du'a for review",
            "options": [
                {
                    "name": "text",
                    "description": "The du'a text",
                    "type": _STRING,
                    "required": True,
                }
            ],
        },
        {"name": "help", "description": "About the ad3oni bot"},
        {
            "name": "setup-daily",
            "description": "Post the prayer of the day to a channel every day",
            "default_member_permissions": str(MANAGE_GUILD),
            "options": [
                {
                    "name": "channel",
                    "description": "Channel to post in",
                    "type": _CHANNEL,
                    "required": True,
                }
            ],
        },
        {
            "name": "schedule",
            "description": "Schedule prayers in a channel",
            "default_member_permissions": str(MANAGE_GUILD),
            "options": [
                {
                    "name": "add",
                    "description": "Add a schedule (cron or natural language)",
                    "type": _SUB_COMMAND,
                    "options": [
                        {
                            "name": "channel",
                            "description": "Channel to post in",
                            "type": _CHANNEL,
                            "required": True,
                        },
                        {
                            "name": "when",
                            "description": "Natural language, e.g. every day at 3pm and 6pm",
                            "type": _STRING,
                            "required": False,
                        },
                        {
                            "name": "cron",
                            "description": "A cron expression, e.g. 0 15 * * *",
                            "type": _STRING,
                            "required": False,
                        },
                        {
                            "name": "content",
                            "description": "What to post (default: random)",
                            "type": _STRING,
                            "required": False,
                            "choices": _CONTENT_CHOICES,
                        },
                        {
                            "name": "category",
                            "description": "Category when content is 'from a category'",
                            "type": _STRING,
                            "required": False,
                            "autocomplete": True,
                        },
                        {
                            "name": "timezone",
                            "description": "IANA timezone (default: Asia/Riyadh)",
                            "type": _STRING,
                            "required": False,
                        },
                    ],
                },
                {
                    "name": "list",
                    "description": "List this server's schedules",
                    "type": _SUB_COMMAND,
                },
                {
                    "name": "remove",
                    "description": "Remove a schedule by id",
                    "type": _SUB_COMMAND,
                    "options": [
                        {
                            "name": "id",
                            "description": "The schedule id (from /schedule list)",
                            "type": _STRING,
                            "required": True,
                        }
                    ],
                },
            ],
        },
    ]

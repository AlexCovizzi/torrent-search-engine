from torrentsearchengine.utils import JsonValidator

TORRENT_PROVIDER_SCHEMA = {
    "type": "object",
    "default": {},
    "patternProperties": {
        ".+": {
            "type": "object",
            "required": [
                "url",
                "search",
                "list"
            ],
            "properties": {
                "url": {
                    "type": "string"
                },
                "search": {
                    "type": "string"
                },
                "whitespace": {
                    "type": "string"
                },
                "headers": {
                    "type": "object",
                    "default": {},
                    "patternProperties": {
                        "[\\w\\-]+": {
                            "type": "string"
                        }
                    }
                },
                "list": {
                    "type": "object",
                    "required": [
                        "items",
                        "item"
                    ],
                    "properties": {
                        "items": {
                            "type": "string"
                        },
                        "item": {
                            "type": "object",
                            "required": ["title"],
                            "patternProperties": {
                                "[a-zA-Z]+": {
                                    "type": "string"
                                }
                            }
                        }
                    }
                },
                "item": {
                    "type": "object",
                    "patternProperties": {
                        "[a-zA-Z]+": {
                            "type": "string"
                        }
                    }
                }
            }
        }
    }
}

torrent_provider_validator = JsonValidator(TORRENT_PROVIDER_SCHEMA)
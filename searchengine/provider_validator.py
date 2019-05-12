from torrenttv.utils.jsonvalidator import JsonValidator

PROVIDER_SCHEMA = {
    "type": "object",
    "required": [
        "name",
        "url",
        "search"
        "list"
    ],
    "properties": {
        "name": {
            "type": "string"
        },
        "url": {
            "anyOf": [
                {
                    "type": "string"
                },
                {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            ]
        },
        "userAgent": {
            "type": "string",
            "default": ""
        },
        "search": {
            "type": "string"
        },
        "next": {
            "type": "string",
            "default": ""
        },
        "list": {
            "type": "object",
            "required": ["items", "item"],
            "properties": {
                "items": {
                    "type": "string"
                },
                "item": {
                    "type": "object",
                    "required": ["title"],
                    "properties": {
                        "[a-zA-Z]+": {
                            "type": "string"
                        }
                    }
                }
            }
        },
        "item": {
            "type": "object",
            "default": {},
            "patternProperties": {
                "[a-zA-Z]+": {
                    "type": "string"
                }
            }
        },
        "format": {
            "type": "object",
            "default": {},
            "patternProperties": {
                "[a-zA-Z]+": {
                    "type": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {
                        "type": "string"
                    }
                }
            }
        }
    }
}

provider_validator = JsonValidator(PROVIDER_SCHEMA)

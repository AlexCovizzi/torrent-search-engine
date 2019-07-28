from jsonschema import Draft4Validator, validators, ValidationError


TORRENT_PROVIDER_SCHEMA = {
    "type": "object",
    "default": {},
    "required": [
        "name",
        "url",
        "search",
        "list"
    ],
    "properties": {
        "name": {
            "type": "string"
        },
        "fullname": {
            "type": "string"
        },
        "url": {
            "type": "string",
            "pattern": "^https?://[\\w\\.]+\\w+/?$"
        },
        "search": {
            "anyOf": [
                {
                    "type": "string"
                },
                {
                    "type": "object",
                    "required": ["all"],
                    "properties": {
                        "all": {
                            "type": "string"
                        },
                        "movies": {
                            "type": "string"
                        },
                        "tv": {
                            "type": "string"
                        },
                        "music": {
                            "type": "string"
                        },
                        "games": {
                            "type": "string"
                        },
                        "apps": {
                            "type": "string"
                        }
                    }
                }
            ]
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
                    "required": ["name"],
                    "patternProperties": {
                        "[a-z_]+": {
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
                "[a-z_]+": {
                    "type": "string"
                }
            }
        }
    }
}


def extend_with_default(validator_class):
    validate_props = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for prop, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(prop, subschema["default"])

        for err in validate_props(validator, properties, instance, schema):
            yield err

    return validators.extend(
        validator_class, {"properties": set_defaults},
    )


JsonValidator = extend_with_default(Draft4Validator)

torrent_provider_validator = JsonValidator(TORRENT_PROVIDER_SCHEMA)

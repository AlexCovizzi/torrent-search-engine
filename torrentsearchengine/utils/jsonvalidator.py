from jsonschema import Draft7Validator, validators


def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for prop, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(prop, subschema["default"])

        for err in validate_properties(validator, properties, instance, schema):
            yield err

    return validators.extend(
        validator_class, {"properties": set_defaults},
    )


JsonValidator = extend_with_default(Draft7Validator)

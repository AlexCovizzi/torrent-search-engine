from jsonschema import Draft7Validator, validators


def extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for prop, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(prop, subschema["default"])

        for error in validate_properties(validator, properties, instance, schema,):
            yield error

    return validators.extend(
        validator_class, {"properties": set_defaults},
    )


JsonValidator = extend_with_default(Draft7Validator)


if __name__ == '__main__':
    obj = {}
    schema = {'properties': {'foo': {'default': 'bar'}}}
    # Note jsonschem.validate(obj, schema, cls=DefaultValidatingDraft7Validator)
    # will not work because the metaschema contains `default` directives.
    JsonValidator(schema).validate(obj)
    print(obj)

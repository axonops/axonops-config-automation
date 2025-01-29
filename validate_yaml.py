import os
import yamale


def find_yaml_files(base_dir):
    """
    Recursively find all YAML files in the base directory.
    """
    yaml_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                yaml_files.append(os.path.join(root, file))
    return yaml_files


def get_schema_file(yaml_file, schema_dir):
    """
    Given a YAML file path, find the corresponding schema file in the schemas directory.
    Example: 'config/bus1/file_a.yaml' → 'schemas/file_a_schema.yaml'
    """
    filename = None
    if yaml_file.endswith(".yaml"):
        filename = os.path.basename(yaml_file).replace('.yaml', '_schema.yaml')
    elif yaml_file.endswith(".yml"):
        filename = os.path.basename(yaml_file).replace('.yml', '_schema.yml')
    else:
        raise NotImplementedError("Only .yaml and .yml files supported")
    return os.path.join(schema_dir, filename)


def validate_yaml_files(base_dir, schema_dir):
    """
    Validate each YAML file against its corresponding schema in the schemas directory.
    """
    yaml_files = find_yaml_files(base_dir)

    if not yaml_files:
        print(f"No YAML files found in {base_dir}.")
        os.exit(1)
        return

    num_yaml_ok = 0
    num_yaml_error = 0
    num_yaml_missing = 0

    for yaml_file in yaml_files:
        schema_file = get_schema_file(yaml_file, schema_dir)

        print(f"Validating {yaml_file} against {schema_file}...")

        if not os.path.exists(schema_file):
            print(f"✖ Schema file not found: {schema_file}")
            num_yaml_missing += 1
            continue

        try:
            schema = yamale.make_schema(schema_file)

            data = yamale.make_data(yaml_file)

            yamale.validate(schema, data)
            print(f"✔ {yaml_file} is valid.")
            num_yaml_ok += 1
        except yamale.YamaleError as e:
            print(f"✖ {yaml_file} failed validation:\n{e}")
            num_yaml_error += 1
        except Exception as e:
            print(f"✖ Error validating {yaml_file}: {e}")
            num_yaml_error += 1

    print(f"OK: {num_yaml_ok}")
    print(f"ERRORS: {num_yaml_error}")
    print(f"MISSING: {num_yaml_missing}")


if __name__ == "__main__":
    config_dir = "config"
    schema_dir = "schemas"

    validate_yaml_files(config_dir, schema_dir)

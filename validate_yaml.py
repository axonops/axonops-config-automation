import os
import sys
import yamale
from collections import Counter


def find_yaml_files(base_dir: str) -> list[str]:
    """
    Recursively find all YAML files in the base directory.

    Args:
        base_dir(str): Path where to find the YAML files

    Returns:
        list[str]: list of YAML files
    """
    yaml_files = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(('.yaml', '.yml')):
                yaml_files.append(os.path.join(root, file))
    return yaml_files


def get_schema_file(yaml_file: str, schema_dir: str) -> str:
    """
    Given a YAML file path, find the corresponding schema file in the schemas directory.

    Example: 'config/demo/file_a.yaml' → 'schemas/file_a_schema.yml'

    Args:
        yaml_file (str): Path to the YAML file.
        schema_dir (str): Directory where schema files are stored.

    Returns:
        str: Corresponding schema file path.

    Raises:
        NotImplementedError: If the file extension is not .yaml or .yml.
    """
    base_name = os.path.basename(yaml_file)
    if base_name.endswith(("yaml", "yml")):
        name, _ = base_name.rsplit(".", 1)
        filename = name + "_schema.yml"
    else:
        raise NotImplementedError("Only .yaml and .yml files supported")
    return os.path.join(schema_dir, filename)


def validate_yaml_file(yaml_file: str, schema_file: str) -> str:
    """
    Validate a single YAML file against its schema.

    Args:
        yaml_file (str): Path to the YAML file.
        schema_file (str): Path to the corresponding schema file.

    Returns:
        str: "ok" if valid, "error" if validation fails, "missing" if schema is missing.
    """
    if not os.path.exists(schema_file):
        print(f"✖ Schema file not found: {schema_file}")
        return 'missing'

    print(f"Validating {yaml_file} against {schema_file}...")

    try:
        schema = yamale.make_schema(schema_file)

        data = yamale.make_data(yaml_file)

        yamale.validate(schema, data)
        print(f"✔ {yaml_file} is valid.")
        return 'ok'
    except yamale.YamaleError as e:
        print(f"✖ {yaml_file} failed validation:\n{e}")
        return 'error'
    except Exception as e:
        print(f"✖ Error validating {yaml_file}: {e}")
        return 'error'


def validate_yaml_files(base_dir: str, schema_dir: str) -> int:
    """
    Validate each YAML file against its corresponding schema in the schemas directory.
    Args:
        base_dir (str): Directory containing YAML files.
        schema_dir (str): Directory containing schema files.

    Returns:
        int: 0 if all files pass, 1 if there are errors or missing schemas.
    """
    yaml_files = find_yaml_files(base_dir)

    if not yaml_files:
        print(f"No YAML files found in {base_dir}.")
        return 1

    results = Counter()

    for yaml_file in yaml_files:
        schema_file = get_schema_file(yaml_file, schema_dir)

        result = validate_yaml_file(yaml_file, schema_file)
        results[result] += 1

    print(f"OK: {results['ok']}")
    print(f"ERRORS: {results['error']}")
    print(f"MISSING: {results['missing']}")

    return int(results['error'] or results['missing'])


if __name__ == "__main__":
    config_dir = "config"
    schema_dir = "schemas"

    exit_value = validate_yaml_files(config_dir, schema_dir)

    sys.exit(exit_value)

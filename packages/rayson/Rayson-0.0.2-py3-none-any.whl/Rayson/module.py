import json
import re

def keys_by_value(data, target_value):
    """
    Searches the JSON data for the given target value and returns a list of key names
    (as strings) that directly precede the target value in the JSON string.

    Note: This approach converts the JSON data to a string and uses regex for searching,
    which may lead to false matches if the target value occurs within other strings.

    :param data: A Python object (usually a dict or list) representing JSON data.
    :param target_value: The value to search for (as a string).
    :return: List of key names where the target value is found.
    """
    try:
        # Convert the data to a JSON string for regex manipulation
        data_str = json.dumps(data)
        tracker = []

        # Use re.escape to safely search for the target_value
        for match in re.finditer(re.escape(target_value), data_str):
            tracker.append((match.start(), match.end()))

        keys = []
        for start, _ in tracker:
            # Backtrack to find the key that precedes the target value
            i = start - 1
            temp = ""
            # Stop at characters that likely denote the beginning of a key
            while i >= 0 and data_str[i] not in [',', '{', '[']:
                temp = data_str[i] + temp
                i -= 1
            # If we find a colon, assume the substring before it is the key
            if ":" in temp:
                key_part = temp.split(":")[0].strip().strip('"')
                keys.append(key_part)
        return keys
    except Exception as e:
        print(f"Error in keys_by_value: {e}")
        return []

def generate_path(data,extracted_keys=None, payload_name="payload"):
    """
    Generates JSON paths for each key in the provided JSON data.
    The function returns a newline-separated string of key path assignments.

    For example, given:
        data = {"name": "Alice", "info": {"age": 30}}
    It may produce paths like:
        payload['name']= 'Alice'
        payload['info']['age']= 30

    :param data: Dictionary representing JSON data.
    :param payload_name: A base name for the JSON payload (default: "payload").
    :return: A string with one JSON path assignment per line.
    """
    try:
        result = []
        # Traverse the top-level keys
        for key, value in data.items():
            initial = f"{payload_name}['{key}']"
            result.append(initial)
            recursive_path_finder(initial, value, result)

        # Filter to paths that include an assignment (i.e. leaf values)
        output = [path for path in result if "=" in path]
        final_result = []
        # Optionally, filter further if needed (this block can be adjusted)
        for path in output:
            for key in data:
                if not extracted_keys:
                    if f"['{key}']" in path:
                        final_result.append(path)
                else:
                    for ekey in extracted_keys:
                         if f"['{ekey}']" in path:
                            final_result.append(path)

        return "\n".join(final_result)
    except Exception as e:
        print(f"Error in generate_path: {e}")
        return ""

def recursive_path_finder(current_path, value, result):
    """
    Recursively traverses the JSON data structure to build full key paths.

    If the value is a dict, it appends keys; if it's a list, it indexes the elements.
    Leaf values are recorded with an assignment (e.g., key= value).

    :param current_path: The JSON path built so far.
    :param value: The current value (could be dict, list, or a primitive).
    :param result: The list that accumulates paths.
    """
    try:
        if isinstance(value, dict):
            for k, v in value.items():
                new_path = f"{current_path}['{k}']"
                result.append(new_path)
                recursive_path_finder(new_path, v, result)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                new_path = f"{current_path}['{index}']"
                result.append(new_path)
                if isinstance(item, (dict, list)):
                    recursive_path_finder(new_path, item, result)
                else:
                    # Record the leaf value for simple list items
                    item_value = f"'{item}'" if isinstance(item, str) else str(item)
                    result.append(f"{new_path}={item_value}")
        else:
            # Record the leaf value for primitive types (str, int, etc.)
            value_str = f"'{value}'" if isinstance(value, str) else str(value)
            result.append(f"{current_path}={value_str}")
    except Exception as e:
        print(f"Error in recursive_path_finder: {e}")



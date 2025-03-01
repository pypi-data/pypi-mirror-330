import json
import re
from datetime import datetime,timedelta


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
        return "\n".join(set(final_result))
    except Exception as e:
        print(f"Error in generate_path: {e}")


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


def get_value_type(value):
    """Returns the JSON Schema type for a given Python value."""
    if isinstance(value, str):
        if value=="Y" or value=="N":
            return "flag"
        return "string"
    elif isinstance(value, int):
        return "integer"
    elif isinstance(value, float):
        return "number"
    elif isinstance(value, bool):
        return "boolean"
    elif value is None:
        return "null"
    else:
        return "string"  # Default fallback



def calculate_age(start_date: str=None, end_date: str = None,travel: int = None):
    '''calculates the age'''
    if not travel:
             # Parse the start date
        start_date = datetime.strptime(start_date, "%d-%m-%Y")

        # Use today's date if end_date is not provided
        if end_date:
            end_date = datetime.strptime(end_date, "%d-%m-%Y")
        else:
            end_date = datetime.today()

        # Get year, month, and day differences correctly
        years = end_date.year - start_date.year
        months = end_date.month - start_date.month
        days = end_date.day - start_date.day

        # Adjust for negative months/days
        if days < 0:
            months -= 1
            prev_month = (end_date.month - 1) or 12  # Handle January case
            prev_year = end_date.year if end_date.month > 1 else end_date.year - 1
            days += (datetime(prev_year, prev_month, 1) - datetime(prev_year, prev_month - 1 or 12, 1)).days

        if months < 0:
            years -= 1
            months += 12

        # Calculate total days difference correctly
        total_days = (end_date - start_date).days

        # Construct response
        result = {
            "years": years,
            "months": months,
            "days": days,
            "total_days": total_days
        }

        return json.dumps(result, indent=4)
    else:
        travel=-1*travel
        if end_date:
            offset = datetime.strptime(end_date, "%d-%m-%Y")-timedelta(travel)
            return offset.strftime("%d-%m-%Y")
        else:
            offset= datetime.today()-timedelta(travel)
            return offset.strftime("%d-%m-%Y")




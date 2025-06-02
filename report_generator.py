# report_generator.py

def _fetch_raw_data(source_id: str) -> list[dict]:
    """
    (Simulated) Fetches raw data based on a source ID.
    In a real app, this might talk to a database or read a complex file.
    """
    if source_id == "users":
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    elif source_id == "products":
        return [{"id": 101, "item": "Laptop"}, {"id": 102, "item": "Mouse"}]
    else:
        return [] # No data for unknown source_id
    
def _format_data_for_display(identification: str) -> str:
    """
    (Simulated) Formats a list of dictionaries into a display string.
    In a real app, this might involve complex string formatting or template rendering.
    """

    raw_data = _fetch_raw_data(identification)
    formatted_lines = []
    
    for item in raw_data:
        # Assuming items have 'id' and either 'name' or 'item'
        if 'name' in item:
            formatted_lines.append(f"User ID: {item['id']}, Name: {item['name']}")
        elif 'item' in item:
            formatted_lines.append(f"Product ID: {item['id']}, Item: {item['item']}")
        else:
            formatted_lines.append(f"Unknown item format: {item}")
    
    # print("Formatted_lines: ", formatted_lines)
    return "\n".join(formatted_lines)

if __name__ == "__main__":

    # Examples
    print(_format_data_for_display("users"))
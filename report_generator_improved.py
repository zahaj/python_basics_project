# report_generator.py

def _fetch_raw_data(source_id: str) -> list[dict]:
    """
    (Simulated) Fetches raw data based on a source ID.
    In a real app, this might talk to a database or read a complex file.
    """
    # print(f"DEBUG: REAL _fetch_raw_data called with {source_id}") # ADD THIS LINE

    if source_id == "users":
        return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    elif source_id == "products":
        return [{"id": 101, "item": "Laptop"}, {"id": 102, "item": "Mouse"}]
    else:
        return [] # No data for unknown source_id

def _format_data_for_display(raw_data: list[dict]) -> str:
    """
    (Simulated) Formats a list of dictionaries into a display string.
    In a real app, this might involve complex string formatting or template rendering.
    """
    if not raw_data:
        return "No items to display."
    
    formatted_lines = []
    for item in raw_data:
        # Assuming items have 'id' and either 'name' or 'item'
        if 'name' in item:
            formatted_lines.append(f"User ID: {item['id']}, Name: {item['name']}")
        elif 'item' in item:
            formatted_lines.append(f"Product ID: {item['id']}, Item: {item['item']}")
        else:
            formatted_lines.append(f"Unknown item format: {item}")
    
    return "\n".join(formatted_lines)

class ReportGenerator:
    def generate_report(self, source_id: str) -> str:
        """
        Generates a full report by fetching raw data and then formatting it.
        """
        print(f"Generating report for source: {source_id}")
        raw_data = _fetch_raw_data(source_id) # Dependency 1 (internal function)
        formatted_report = _format_data_for_display(raw_data) # Dependency 2 (internal function)
        return f"--- Report for {source_id} ---\n{formatted_report}\n--- End Report ---"
import json
from datetime import datetime, timedelta

# Function to process each object in the array
def process_json_object(obj, match_counts):
    customer_id = "CUST0023"
    source_id = "SRC00456"
    template_id = "45678901"
    response_created_date = datetime.strptime(obj["response_created"], "%Y-%m-%d %H:%M:%S")
    if (
        obj["customer_id"] == customer_id
    ):
        # Increment match count for this condition
        match_counts["condition_1"] += 1

        # Set "is_exception" to True for every second record that matches the condition
        if match_counts["condition_1"] % 6 == 0:
            obj["total_tokens"] = str(int(obj["total_tokens"]) + 183)
    
    if (
        obj["source_id"] == source_id
    ):
        # Increment match count for this condition
        match_counts["condition_2"] += 1

        # Set "is_exception" to True for every second record that matches the condition
        if match_counts["condition_2"] % 6 == 0:
            obj["latency"] = str(float(obj["latency"]) + 280)

# Read the JSON file
file_path = "outlier_avoidance.json"  # Replace this with the actual file path
with open(file_path, "r") as file:
    data = json.load(file)

# Initialize match counts for each condition
match_counts = {
    "condition_1": 0,
    "condition_2": 0
}

# Process each object in the JSON array
for item in data:
    process_json_object(item, match_counts)

# Save the modified JSON back to the file
with open(file_path, "w") as file:
    json.dump(data, file, indent=4)

print("JSON file has been updated successfully.")

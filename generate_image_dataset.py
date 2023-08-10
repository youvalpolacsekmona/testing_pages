import json
import random
from faker import Faker

fake = Faker()

# Specify the number of rows in the dataset
num_rows = 20000

# List of common cities and countries
common_cities = ["New York", "Los Angeles", "London", "Paris", "Tokyo", "Sydney"]
common_countries = ["United States", "United Kingdom", "France", "Australia", "Japan"]

# Scene description templates based on detected objects
scene_description_templates = {
    "cat": "A cat is sitting on {{a|an}} {{color}} {{object}} {{location}}.",
    "dog": "A dog is {{activity}} near {{a|an}} {{color}} {{object}} {{location}}.",
    "car": "{{a|an}} {{color}} car is parked on {{the}} {{location}}.",
    "tree": "{{a|an}} {{location}} tree stands tall in the background.",
    "building": "{{a|an}} {{color}} building dominates the scene.",
    "person": "A person is {{activity}} in {{the}} {{location}}.",
    "bird": "{{a|an}} {{color}} bird is perched on {{a|an}} {{location}}.",
    "bicycle": "{{a|an}} {{color}} bicycle leans against {{the}} {{location}}."
}

def generate_sentence(object_type, location, color=None):
    template = scene_description_templates.get(object_type, "Something is happening in {{the}} {{location}}.")
    if color is None:
        color = fake.safe_color_name()
    activity = fake.random_element(elements=("standing", "sitting", "running", "walking"))
    return template.replace("{{object}}", object_type).replace("{{location}}", location).replace("{{color}}", color).replace("{{activity}}", activity).replace("{{a|an}}", fake.random_element(elements=("a", "an"))).replace("{{the}}", fake.random_element(elements=("the", "a", "an")))

# Generate JSON data
data = []

for _ in range(num_rows):
    # Generate random labels for objects detected
    num_objects = random.randint(1, 5)
    objects_detected = fake.random_elements(
        elements=("cat", "dog", "car", "tree", "building", "person", "bird", "bicycle"),
        unique=True,
        length=num_objects
    )

    # Capitalize the first letter of objects for better sentence formation
    capitalized_objects = [obj.capitalize() for obj in objects_detected]

    # Randomly choose one or more of the detected objects as ground truth labels
    ground_truth_labels = fake.random_elements(
        elements=capitalized_objects,
        unique=False,
        length=random.randint(1, len(capitalized_objects))
    )

    # Generate random duration between 0.002 and 1.5 seconds
    duration = round(random.uniform(0.002, 1.5), 3)

    # Choose a common city and country
    location = fake.random_element(elements=common_cities)
    country = fake.random_element(elements=common_countries)

    # Simulate image properties
    image_width = fake.random_int(min=800, max=1920)
    image_height = int(image_width / 1.77)  # Aspect ratio of 16:9
    num_pixels = image_width * image_height

    # Generate a scene description based on detected objects
    scene_description = " ".join([
        generate_sentence(obj, location) for obj in objects_detected
    ])
    user_feedback_sentiment = fake.random_element(
        elements=("Positive", "Neutral", "Negative")
    )

    # Generate User_Feedback_Ratings based on User_Feedback_Sentiment
    if user_feedback_sentiment == "Positive":
        user_feedback_ratings = fake.random_element(elements=(4, 5))
    elif user_feedback_sentiment == "Neutral":
        user_feedback_ratings = 3
    elif user_feedback_sentiment == "Negative":
        user_feedback_ratings = fake.random_element(elements=(1, 2))

    # Simulate data quality issues
    data_quality_issues = fake.random_element(
        elements=("Blurry image", "Incorrect labels", "Low resolution", "Overexposed")
    )

    # Simulate prediction mistakes by randomly selecting predicted class
    predicted_class = fake.random_element(elements=capitalized_objects + ground_truth_labels)
    
    # Determine if Ground_Truth_Labels match the Top_Predicted_Class
    ground_truth_match = predicted_class in ground_truth_labels

    # Generate dynamic relation between Top_Predicted_Probability and Model_Confidence_Score
    base_probability = random.uniform(0.1, 0.9)
    model_confidence_variation = random.uniform(0.05, 0.15)

    if ground_truth_match:
        top_predicted_probability = min(0.989, base_probability + model_confidence_variation + 0.23)  # Increase by 0.1 when correct
        model_confidence_score = min(0.989, base_probability + model_confidence_variation * random.uniform(0.8, 1.2) + 0.11)  # Increase by 0.1 when correct
    else:
        top_predicted_probability = max(0.0, base_probability - model_confidence_variation + 0.11)
        model_confidence_score = max(0.0, base_probability - model_confidence_variation * random.uniform(0.8, 1.2))

    row = {
        "Image_Width": str(image_width),
        "Image_Height": str(image_height),
        "Num_Pixels": str(num_pixels),
        "Aspect_Ratio": "16:9",
        "Location_Captured": location,
        "Country_Captured": country,
        "Capture_Date": fake.date_this_year().strftime('%Y-%m-%d'),
        "Objects_Detected": capitalized_objects,
        "Object_Bounding_Boxes": [
            str(fake.random_int(0, image_width)),
            str(fake.random_int(0, image_height)),
            str(fake.random_int(0, image_width)),
            str(fake.random_int(0, image_height))
        ],
        "Scene_Description": scene_description,
        "Ground_Truth_Labels": ground_truth_labels,
        "Top_Predicted_Class": predicted_class,
        "Top_Predicted_Probability": str(round(top_predicted_probability, 3)),
        "Model_Confidence_Score": str(round(model_confidence_score, 3)),
        "User_Feedback_Ratings": str(user_feedback_ratings),
        "User_Feedback_Sentiment": user_feedback_sentiment,
        "Data_Split_Type": fake.random_element(
            elements=("Train", "Validation", "Test")
        ),
        "Data_Source_Type": fake.random_element(
            elements=("Web scraping", "User uploads", "Stock photos")
        ),
        "Annotation_Type": fake.random_element(
            elements=("Bounding Box", "Segmentation Mask")
        ),
        "Augmentation_Methods": fake.random_element(
            elements=("Rotation", "Flip", "Color Adjustment")
        ),
        "Duration": str(duration),
        "Data_Quality_Issues": data_quality_issues
    }

    data.append(row)

# Save JSON data to a file
with open("image_classification_dataset.json", "w") as jsonfile:
    json.dump(data, jsonfile, indent=4)

print(f"Generated {num_rows} rows of fake image classification data in JSON format.")

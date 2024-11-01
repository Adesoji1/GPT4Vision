import os
import requests
import csv
import base64
from PIL import Image
from io import BytesIO

import openai


# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] = 'sk---xxxxx'
openai.api_key = os.getenv("OPENAI_API_KEY")

def download_and_optimize_images(image_urls, output_folder='optimized_images'):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    saved_filenames = []

    for url in image_urls:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        
        # Resize the image to 512x512 pixels
        img.thumbnail((512, 512))
        
        # Save the optimized image
        filename = url.split('/')[-1]
        filepath = os.path.join(output_folder, filename)
        img.save(filepath)
        saved_filenames.append(filepath)

    return saved_filenames

# Example usage
image_urls = ['https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg']
saved_images = download_and_optimize_images(image_urls)

# client = OpenAI()

def process_image(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"The file {image_path} does not exist.")

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high"
                        }
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    
    return response.choices[0].message.content

# Process each saved image
for saved_image in saved_images:
    processed_data = process_image(saved_image)
    print(processed_data)

def save_to_csv(data, filename='output.csv'):
    # Check if the directory exists for the file, create if not
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Project ID', 'Style'])
        writer.writerow([data['project_id'], data['style']])

# Assuming 'processed_data' contains the result from the previous step
save_to_csv({'project_id': '12345', 'style': 'modern'})

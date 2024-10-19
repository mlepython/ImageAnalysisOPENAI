from openai import OpenAI
import base64
from pdf2image import convert_from_path
from pathlib import Path
from dotenv import load_dotenv
import os
import json

load_dotenv()

def save_to_json(data, filename='result.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def append_to_json_file(file_path, new_data):
    if isinstance(new_data, str):
        new_data = json.loads(new_data)
    # Read the existing data from the file
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # If the file does not exist, start with an empty list
        data = []

    # Append the new data to the existing data
    if isinstance(data, list):
        data.append(new_data)
    elif isinstance(data, dict):
        data.update(new_data)
    else:
        raise ValueError("Unsupported data format in JSON file")
    
    save_to_json(data, filename=file_path)

class OpenAI_Image_Data_Extraction(OpenAI):
    def __init__(self, model_name="gpt-4-vision-preview", max_tokens=2000):
        super().__init__()
        self.file_path = ""
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.first_page = None
        self.last_page = None
        self.system_prompt = ""
        self.user_prompt = ""

    def check_file_path(self):
        if len(self.file_path) != 0:
            self.file_path = Path(self.file_path)
        else:
            raise ValueError('You must provide a path to your image file or pdf')

    def convert_pdf_to_images(self, pdf_path, output_folder='temp_images'):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"Directory '{output_folder}' created.")
        else:
            print(f"Directory '{output_folder}' already exists.")

        if (self.first_page or self.last_page) is None:
            print("Converting all pages to images")
            images = convert_from_path(pdf_path)
        else:
            print(f"Converting pages {self.first_page} to {self.last_page} to images")
            images = convert_from_path(pdf_path, first_page=self.first_page, last_page=self.last_page)

        pdf_image_path = []
        for count, image in enumerate(images):  
            image_path = f"{output_folder}/page_{count + 1}.png"
            image.save(image_path, 'PNG')
            print(f"Page {count + 1} saved as {image_path}")
            pdf_image_path.append(image_path)
        return pdf_image_path

    def message_with_images(self, images: list):
        role = "user"
        content = []
        for i, image_path in enumerate(images):
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

                content.append({"type": "text", "text": self.user_prompt})
                content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})

        return {"role": role, "content": content}

    def system_message(self) -> list:
        if len(self.system_prompt) != 0:
            messages =  [{"role": "system", "content": [
                {"type": "text", "text": self.system_prompt}
                ]
                }
            ]
        else:
            raise ValueError("System Prompt cannot be empty.")
        return messages

    def run_openai(self, messages: list):
        response = self.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content

    def process_file(self):
        self.check_file_path()

        if self.file_path.suffix.lower() == '.pdf':
            image_paths = self.convert_pdf_to_images(self.file_path, output_folder='temp_images')
        else:
            if isinstance(self.file_path, list): image_paths = self.file_path
            else: image_paths=[self.file_path]

        messages = self.system_message()
        messages.append(self.message_with_images(images=image_paths))
        result = self.run_openai(messages=messages)
        return result
    
    def process_multiple_files(self, directory, json_filename):
        pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]
        print("PDF files in directory:")
        for file in pdf_files:
            print(file)
            self.file_path = directory + f'/{file}'
            result = self.process_file()
            data = result.split('``json')[-1].split("```")[0]
            append_to_json_file(file_path=json_filename, new_data=data)
    

    
if __name__ == "__main__":
    script = OpenAI_Image_Data_Extraction()
    directory = r"G:\My Drive\Royal Crown Mike\MHF4U\Unit 6 - Review-Combined-Function-ROC\Unit 5 - Combine Functions and Rates of Change\Lesson Plan\Lesson Plans - pdf"
    
    script.system_prompt = """Your task will be to extract lesson content from the provided images by the user.
                Extract the following content from the image as it appears in the table. Put result into a JSON array.
                course_code: <text>
                overall: <overall expectation list>
                specific: <specific expectation list>
                unit_name: <text>
                lesson_topic: <text>
                learning_goal: <text>
                success_criteria: <text>
                introduction: <text>
                development: <text>
                consolidation: <text>
                extension: <text>
                materials: <text>
                strategies/activities: <only highlighted text>
                IF the content cannot be extracted from image return an empty JSON array.
                """
    # script.process_file()
    script.process_multiple_files(directory, json_filename='mhf4u_unit_5_lesson_plan.json')
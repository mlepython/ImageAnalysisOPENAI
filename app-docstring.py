
from openai import OpenAI
import base64
from pdf2image import convert_from_path
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

class OpenAI_Image_Data_Extraction(OpenAI):
    '''
    A class to extract image data using OpenAI's GPT-4 Vision API.

    Parameters:
    - model_name (str): The name of the model to use. Default is 'gpt-4-vision-preview'.
    - max_tokens (int): The maximum number of tokens for the GPT-4 Vision API to use.
    '''

    def __init__(self, model_name="gpt-4-vision-preview", max_tokens=1000):
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
        '''
        Check if the file path provided is valid.

        Raises:
        - ValueError: If no file path was provided.
        '''
        if len(self.file_path) != 0:
            self.file_path = Path(self.file_path)
        else:
            raise ValueError('You must provide a path to your image file or pdf')

    def convert_pdf_to_images(self, pdf_path, output_folder='temp_images'):
        '''
        Converts a provided PDF into images.

        Parameters:
        - pdf_path (str): The path to the PDF file.
        - output_folder (str): The folder to save the converted images in.

        Returns:
        - pdf_image_path (list): A list of paths to the converted images.
        '''
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

        pdf_image_path = []  # Store paths of converted images
        for count, image in enumerate(images):  
            image_path = f"{output_folder}/page_{count + 1}.png"
            image.save(image_path, 'PNG')
            print(f"Page {count + 1} saved as {image_path}")
            pdf_image_path.append(image_path)
        return pdf_image_path

    def message_with_images(self, images: list):
        '''
        Prepares a message with images for the GPT-4 Vision API.

        Parameters:
        - images (list): A list of paths to the images to include in the message.

        Returns:
        - (dict): A dictionary containing the message with images.
        '''
        role = "user"
        content = []
        for i, image_path in enumerate(images):
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

                content.append({"type": "text", "text": self.user_prompt})  # Append any user text prompts to content
                content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})

        return {"role": role, "content": content}

    def system_message(self) -> list:
        '''
        Prepares a system message for the GPT-4 Vision API.

        Returns:
        - messages (list): A list containing the system message.

        Raises:
        - ValueError: If the system prompt is empty.
        '''
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
        '''
        Runs the GPT-4 Vision API.

        Parameters:
        - messages (list): The messages to send to the GPT-4 Vision API.

        Returns:
        - (dict): The response from the GPT-4 Vision API.
        '''
        response = self.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content

    def process_file(self):
        '''
        Processes the file, converts it to images, and runs the GPT-4 Vision API.

        Returns:
        - (dict): The result from the GPT-4 Vision API.
        '''
        self.check_file_path()

        if self.file_path.suffix.lower() == '.pdf':
            image_paths = self.convert_pdf_to_images(self.file_path, output_folder='temp_images')
        else:
            if isinstance(self.file_path, list): image_paths = self.file_path
            else: image_paths=[self.file_path]

        messages = self.system_message()
        messages.append(self.message_with_images(images=image_paths))
        result = self.run_openai(messages=messages)
        print(result)
        return result

if __name__ == "__main__":
    script = OpenAI_Image_Data_Extraction()
    script.file_path = r"OpenAI-Blog.pdf"
    script.system_prompt = """Summarize the content for a markdown document"""
    script.process_file()  # Run the process on the provided file

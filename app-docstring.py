
from openai import OpenAI
import base64
from pdf2image import convert_from_path
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

class OpenAI_Image_Data_Extraction(OpenAI):
    def __init__(self, model_name="gpt-4-vision-preview", max_tokens=1000):
        '''
        Initialize the OpenAI_Image_Data_Extraction class.

        Parameters:
        - model_name (str): The name of the OpenAI model to be used.
        - max_tokens (int): The maximum number of tokens for model completion.

        Returns:
        None
        '''
        super().__init__()
        self.file_path = ""
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.first_page = None
        self.last_page = None
        self.system_prompt = ""
        self.user_prompt = ""

    def check_file_path(self) -> None:
        '''
        Check if the file path is provided.

        Raises:
        ValueError: If the file path is empty.
        '''
        if len(self.file_path) != 0:
            self.file_path = Path(self.file_path)
        else:
            raise ValueError('You must provide a path to your image file or pdf')

    def convert_pdf_to_images(self, pdf_path:str, output_folder:str='temp_images') -> list:
        '''
        Convert a pdf to a list of images.

        Parameters:
        - pdf_path (str): The path to the pdf file.
        - output_folder (str): The output folder for the converted images.

        Returns:
        list: A list of paths to the converted images.
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

        pdf_image_path = []
        for count, image in enumerate(images):  
            image_path = f"{output_folder}/page_{count + 1}.png"
            image.save(image_path, 'PNG')
            print(f"Page {count + 1} saved as {image_path}")
            pdf_image_path.append(image_path)
        return pdf_image_path

    def message_with_images(self, images: list) -> dict:
        '''
        Generate a message containing images.

        Parameters:
        - images (list): A list of paths to the images.

        Returns:
        dict: A message containing the images.
        '''
        role = "user"
        content = []
        for i, image_path in enumerate(images):
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')

                content.append({"type": "text", "text": self.user_prompt})
                content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}})

        return {"role": role, "content": content}

    def system_message(self) -> list:
        '''
        Generate a system message.

        Returns:
        list: A system message list.
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

    def run_openai(self, messages: list) -> str:
        '''
        Run the OpenAI model.

        Parameters:
        - messages (list): A list of messages.

        Returns:
        str: The response from the model.
        '''
        response = self.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=self.max_tokens
        )
        return response.choices[0].message.content

    def process_file(self) -> str:
        '''
        Process the file and run the OpenAI model.

        Returns:
        str: The processed result from the OpenAI model.
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
    # script.first_page = 2
    # script.last_page = 4
    script.system_prompt = """Summarize the content for a markdown document
    """
    script.process_file()

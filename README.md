# OpenAI Image Data Extraction

The `OpenAI Image Data Extraction` class in this code allows you to process images and PDFs using OpenAI's GPT-4 vision model to extract information and generate a summary. It provides functions to convert a PDF to images, generate a message containing the images, create a system message, and run the OpenAI model with the provided messages.

## Prerequisites

Before using the code, ensure you have the following dependencies installed:
- `openai` library
- `pdf2image` library
- `pathlib` library
- `dotenv` library
- OpenAI API key stored in a `.env` file

## Usage

1. First, create a `.env` file in the same directory as the code and add your OpenAI API key in the following format:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

2. Initialize the `OpenAI_Image_Data_Extraction` class with optional parameters for model name and max tokens.

   ```python
   script = OpenAI_Image_Data_Extraction(model_name="gpt-4-vision-preview", max_tokens=1000)
   ```

3. Set the file path for the image or PDF to be processed.

   ```python
   script.file_path = "path_to_your_file.pdf"  # Replace with the actual file path
   ```

4. Optionally, specify the first and last page if processing a specific range of pages from a PDF.

   ```python
   script.first_page = 2
   script.last_page = 4
   ```

5. Set the system prompt for the OpenAI model.

   ```python
   script.system_prompt = "Summarize the content for a markdown document"
   ```

6. Run the processing and OpenAI model by calling the `process_file` method.

   ```python
   script.process_file()
   ```

## Example

Here's an example of using the `OpenAI_Image_Data_Extraction` class to process a PDF file and extract information:

```python
script = OpenAI_Image_Data_Extraction(model_name="gpt-4-vision-preview", max_tokens=1000)
script.file_path = "sample_document.pdf"
script.system_prompt = "Summarize the content for a markdown document"
script.process_file()
```

## Important Notes

- Ensure that you have the correct OpenAI API key set in the `.env` file.
- The code uses base64 encoding to include images in the messages sent to the OpenAI model.
- The `convert_pdf_to_images` function creates temporary image files when processing PDFs.
- The `run_openai` method interacts with the OpenAI GPT-4 vision model to generate the response.

## Future Improvements

- Error handling for different file formats and edge cases.
- Support for additional OpenAI models and parameters.
- Performance optimizations when handling large PDFs or images.

Feel free to customize the code and contribute to the class for further enhancements. If you encounter any issues, please consider opening an GitHub issue or pull request.
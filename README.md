# README for OpenAI_Image_Data_Extraction

This is a README file for the Python module `OpenAI_Image_Data_Extraction`. This module is used to extract data from images and PDFs using the *GPT-4 Vision* model of OpenAI. It converts PDFs to images, encodes them in base64, sends it to OpenAI for analysis and extracts the data.

## Setup and Installation

To use this module, make sure you have these dependencies installed:
* OpenAI `openai==0.6.13`
* pdf2image `pdf2image==1.16.0`
* dotenv `python-dotenv==0.19.1`

Install them using pip:
```bash
pip install openai==0.6.13 pdf2image==1.16.0 python-dotenv==0.19.1
```

## Functionality

The main functions of the `OpenAI_Image_Data_Extraction` class are:
- `check_file_path()`: Validates the file path of the image or PDF.
- `convert_pdf_to_images(pdf_path, output_folder='temp_images')`: Converts PDF to images and stores them in the specified output folder.
- `message_with_images(images: list)`: Prepares the message content with image data for the OpenAI API call.
- `system_message()`: Returns the system message used for the OpenAI API request.
- `run_openai(messages: list)`: Executes the OpenAI API call and returns the data extracted from the images.
- `process_file()`: Orchestrates the entire process of extracting data from files.

To use the module, create an instance of the class `OpenAI_Image_Data_Extraction`, specify the file path, and call the `process_file()` method:

```python
script = OpenAI_Image_Data_Extraction()
script.file_path = "path_to_your_file.pdf"
script.process_file()
```

You can also specify the range of pages you want to convert from the PDF:

```python
script = OpenAI_Image_Data_Extraction()
script.file_path = "path_to_your_file.pdf"
script.first_page = 2
script.last_page = 4
script.process_file()
```

## Contributing

For **suggestions**, **bug reports**, or **enhancements**, feel free to open an [issue](https://github.com/YourGitHub/OpenAI_Image_Data_Extraction/issues).

## License

This project is licensed under the terms of the MIT license. For more details, see the [LICENSE](https://github.com/YourGitHub/OpenAI_Image_Data_Extraction/blob/main/LICENSE) file.

![OpenAI logo](https://openai.com/static/images/openai/og-image.jpg)

---
*Made with* **Python** *and* **OpenAI**.
import pytesseract
from PIL import Image
from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class OCRInput(BaseModel):
    image_path: str = Field(..., description="Path to the image to be processed")

class OCRTool(BaseTool):
    """
    OCR Tool
    """
    name: str = "OCR Tool"
    args_schema: Type[BaseModel] = OCRInput
    description: str = "Performs OCR on an image"

    def _execute(self, image_path: str = None):
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
        return greetings_str

import pytesseract
from pyvirtualdisplay.smartdisplay import SmartDisplay  # Added import
import openai
from PIL import Image
from PIL import ImageGrab
from superagi.tools.base_tool import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import os
import time
import numpy as np
import cv2
from screeninfo import get_monitors

disp = SmartDisplay(visible=0, size=(800, 600))
disp.start()

import pyautogui  # Now you can import pyautogui

class OCRInput(BaseModel):
    image_path: str = Field(..., description="Path to the image to be processed")
    language: str = Field('eng', description="Language for OCR")      

class OcrTool(BaseTool):
    """
    OCR Tool
    """
    name: str = "OCR Tool"
    args_schema: Type[BaseModel] = OCRInput
    description: str = "Performs OCR on an image"
    
    def __init__(self):
        super().__init__()
    

    def _execute(self, image_path: str = None, language: str = 'eng'):
        # Check if the image file exists
        if not os.path.isfile(image_path):
            return "Error: File does not exist"

        try:
            # Open the image file
            image = Image.open(image_path)
        except Exception as e:
            return f"Error: Unable to open image file: {e}"

        # Perform OCR on the image
        try:
            text = pytesseract.image_to_string(image, lang=language)  
        except Exception as e:
            return f"Error: Unable to perform OCR: {e}"

        # Use GPT-3 to generate text
        openai.api_key = 'your-openai-api-key'
        response = openai.Completion.create(engine="text-davinci-003", prompt=text, max_tokens=100)

        # Simulate typing the generated text
        for char in response.choices[0].text.strip():
            pyautogui.typewrite(char)
            time.sleep(0.1)  # pause between each character

        return response.choices[0].text.strip()

    def move_mouse_and_click(self, x: int, y: int):
        try:
            pyautogui.moveTo(x, y)
            pyautogui.click()
        except Exception as e:
            return f"Error: Unable to move mouse and click: {e}"

    def perform_ocr(self):
        # Clear text box
        self.chatbox.delete('1.0', 'end')

        # Initialize best text and its length
        best_text = ""
        best_length = 0

        # Iterate over all screens
        for screen in get_monitors():
            try:
                # Grab the screen
                img = ImageGrab.grab()
                img_np = np.array(img)
                gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

                # Process the image
                if self.mode_var.get() == 'Threshold':
                    threshold = self.threshold_scale.get()
                    _, processed_img = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
                else:
                    processed_img = gray

                # Perform OCR
                text = pytesseract.image_to_string(processed_img)

                # If this text is better than the current best, update the best text
                if len(text) > best_length:
                    best_text = text
                    best_length = len(text)
            except Exception as e:
                self.chatbox.insert(1.0, f"Error: {str(e)}\n")

        # Display the best text
        self.text = best_text
        self.chatbox.insert(1.0, f"{best_text}\n")

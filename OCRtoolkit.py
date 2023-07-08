from abc import ABC
from superagi.tools.base_tool import BaseToolkit, BaseTool
from typing import Type, List
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from ocr_tool import OcrTool


class OCRToolkit(BaseToolkit, ABC):
    name: str = "OCR Toolkit"
    description: str = "OCR Tool kit contains all tools related to OCR with GPT-4"

    def get_tools(self) -> List[BaseTool]:
        return [OcrTool()]

    def get_env_keys(self) -> List[str]:
        return ["OPENAI_API_KEY"]
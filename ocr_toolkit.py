import logging
from abc import ABC
from superagi.tools.base_tool import BaseToolkit, BaseTool
from typing import Type, List
import sys
import os
sys.path.insert(0, '/app/superagi/tools/OCRProject')

from ocr_tool import OcrTool


class OCRToolkit(BaseToolkit, ABC):
    name: str = "OCR Toolkit"
    description: str = "OCR Tool kit contains all tools related to OCR with GPT-4"
    organisation_id: int
    id: int
    
    def __init__(self, organisation_id: int, id: int):
        self.organisation_id = organisation_id
        self.id = id
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def get_tools(self) -> List[BaseTool]:
        self.logger.debug('Getting tools')
        return [OcrTool()]

    def get_env_keys(self) -> List[str]:
        self.logger.debug('Getting environment keys')
        return ["OPENAI_API_KEY"]

import os
import re
from pathlib import Path
import google.generativeai as genai
import pyautogui, pygetwindow
from typing import Optional
from langchain.tools import tool

VISION_MODEL="gemini-2.0-flash-exp"
class Vision:
    """Vision is a tool that allows the agent to see the screen and answer questions about it.
    Currently supports only gemini models."""
    def __init__(self, model):
        self.image_directory = os.path.join(os.getcwd(),'MAS','Database','images', 'QnA_images')
        self.model=model

    def _input_image_setup(self,file_loc):
        if not (img := Path(file_loc)).exists():
            raise FileNotFoundError(f"Could not find image: {img}")
        image_parts = [
            {
                "mime_type": "image/png",
                "data": Path(file_loc).read_bytes()
                }
            ]
        return image_parts
    def _answer_image(self,context_or_sentence, image_content):
        input_prompt = """You are an multimodal ai agent as part of larger ai system. Your job is to help user or other ai agents with their image related query. Describe the image in detail as well as try to answer user query."""
        model = genai.GenerativeModel(model_name=self.model)
        prompt_parts = [input_prompt,image_content[0],context_or_sentence]
        response = model.generate_content(prompt_parts)
        response.resolve()
        return response.text
    
    def activate_window(self):
        x,y=pyautogui.position()
        window=pygetwindow.getWindowsAt(x=x,y=y)[0]
        window.activate()


    def vision_workfow(self, query: str) -> str:
        # Ensure the image directory exists
        os.makedirs(self.image_directory, exist_ok=True)

        # Define the full file path with a proper extension (e.g., .png)
        file_path = os.path.join(self.image_directory, "screenshot.png")

        # self.activate_window()
        pyautogui.screenshot(file_path)
        print('Screenshot saved to:', file_path)

        # Process the saved image
        image_content = self._input_image_setup(file_path)
        result = self._answer_image(query, image_content=image_content)

        # Clean up by removing the screenshot
        os.remove(file_path)

        return result


VISION_OBJ=Vision(model=VISION_MODEL)


@tool('Vision',return_direct=False)
def Vision_Model(query: Optional[str]):
    """{query : str}\n analyzes image based on query.This acts as your vision/eye which helps you see the screen. Ask relevant questions to this."""
    return VISION_OBJ.vision_workfow(query=query)

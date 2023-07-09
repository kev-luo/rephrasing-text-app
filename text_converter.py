from langchain import PromptTemplate
from langchain.llms import OpenAI

template = """
    Below is some text that may be poorly worded.
    Your goal is to:
    - Properly format the text
    - Convert the input text to a specified tone
    - Convert the input text to a specified dialect

    Here are some examples different Tones:
    - Formal: We went to Barcelona for the weekend. We have a lot of things to tell you.
    - Informal: Went to Barcelona for the weekend. Lots to tell you.  

    Here are some examples of words in different dialects:
    - American: French Fries, cotton candy, apartment, garbage, cookie, green thumb, parking lot, pants, windshield
    - British: chips, candyfloss, flag, rubbish, biscuit, green fingers, car park, trousers, windscreen

    Example Sentences from each dialect:
    - American: I headed straight for the produce section to grab some fresh vegetables, like bell peppers and zucchini. After that, I made my way to the meat department to pick up some chicken breasts.
    - British: Well, I popped down to the local shop just the other day to pick up a few bits and bobs. As I was perusing the aisles, I noticed that they were fresh out of biscuits, which was a bit of a disappointment, as I do love a good cuppa with a biscuit or two.
    
    Below is the text, tone, and dialect:
    TONE: {tone}
    DIALECT: {dialect}
    TEXT: {text}
    
    YOUR {dialect} RESPONSE:
"""

class TextConverter:
    def __init__(self, openai_api_key):
        self.prompt = PromptTemplate(
            input_variables=["tone", "dialect", "text"],
            template=template
        )
        self.llm = self.load_LLM(openai_api_key)

    def load_LLM(self, openai_api_key):
        llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
        return llm

    def convert_text(self, tone, dialect, text):
        prompt_with_text = self.prompt.format(tone=tone, dialect=dialect, text=text)
        converted_text = self.llm(prompt_with_text)
        return converted_text
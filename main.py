import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

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

prompt = PromptTemplate(input_variables=["tone", "dialect", "text"], template=template)


def load_LLM(openai_api_key):
    # logic for loading the chain i want to use
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    return llm


def get_openai_api_key():
    input_api_key = st.text_input(
        label="OpenAI API Key", placeholder="Ex: sk-3Pk92DIjoi...", key="openai_api_key_input"
    )
    return input_api_key


st.set_page_config(page_title="Rephrase Text", page_icon=":robot:")

st.markdown("# Rephrase This Please")
col1_header, col2_header = st.columns(2)
with col1_header:
    st.markdown(
        "Sometimes your grammar isn't the best or you want to convey a certain tone and don't know exactly how to do it. This app is designed to help with that by rephrasing things how you want. This is powered by [LangChain](https://docs.langchain.com/docs/) and [OpenAI](https://openai.com/). Thank you to Greg Kamradt's [youtube video](https://www.youtube.com/watch?v=U_eV8wfMkXU&list=PLqZXAkvF1bPNQER9mLmDbntNfSpzdDIU5&index=13&ab_channel=GregKamradt%28DataIndy%29) demonstrating how to create this."
    )
with col2_header:
    st.image(image="greg_kamradt_youtube_screenshot.png", width=500, caption="https://www.youtube.com/@DataIndependent")

st.markdown("### Enter your text to rephrase")
openai_api_key = get_openai_api_key()
col1_option, col2_option = st.columns(2)
with col1_option:
    option_tone = st.selectbox("Which tone would you like your text to have?", ("Formal", "Informal"))
with col2_option:
    option_dialect = st.selectbox("Which English Dialect would you like?", ("American English", "British English"))


def get_text():
    text_to_rephrase = st.text_area(label="Text to Rephrase", placeholder="Your text here...", key="rephrase_text")
    return text_to_rephrase


input_text = get_text()


def update_input_text_with_example():
    print("in updated")
    st.session_state.rephrase_text = "Hey I want eat veggies, and want you to come. What time to go?"


st.button(
    "*See An Example*",
    type="secondary",
    help="Click to see an example of some text to rephrase.",
    on_click=update_input_text_with_example,
)

st.markdown("### Your rephrased text:")
if input_text:
    if not openai_api_key:
        st.warning(
            "Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)",
            icon="⚠️",
        )
        st.stop()
    if len(input_text.split(" ")) > 700:
        st.write("Please enter a shorter text block. The maximum length is 700 words.")
        st.stop()
    llm = load_LLM(openai_api_key=openai_api_key)
    llm_prompt_with_text = prompt.format(tone=option_tone, dialect=option_dialect, text=input_text)
    rephrased_text = llm(llm_prompt_with_text)
    st.write(rephrased_text)

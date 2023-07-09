import streamlit as st
from text_converter import TextConverter


def get_openai_api_key():
    input_api_key = st.text_input(
        label="OpenAI API Key", placeholder="Ex: sk-3Pk92DIjoi...", key="openai_api_key_input"
    )
    return input_api_key


def get_text():
    text_to_rephrase = st.text_area(label="Text to Rephrase", placeholder="Your text here...", key="rephrase_text")
    return text_to_rephrase


def get_conversion_options():
    col1_option, col2_option = st.columns(2)
    with col1_option:
        option_tone = st.selectbox("Which tone would you like your text to have?", ("Formal", "Informal"))
    with col2_option:
        option_dialect = st.selectbox("Which English Dialect would you like?", ("American English", "British English"))
    return option_tone, option_dialect


def update_input_text_with_example():
    print("in updated")
    st.session_state.rephrase_text = "Hey I want eat veggies, and want you to come. What time to go?"


def main():
    st.set_page_config(page_title="Rephrase Text", page_icon=":robot:")
    st.markdown("# Rephrase This Please")
    col1_header, col2_header = st.columns(2)
    with col1_header:
        st.markdown(
            "Sometimes your grammar isn't the best or you want to convey a certain tone and don't know exactly how to do it. This app is designed to help with that by rephrasing things how you want. This is powered by [LangChain](https://docs.langchain.com/docs/) and [OpenAI](https://openai.com/). Thank you to Greg Kamradt's [youtube video](https://www.youtube.com/watch?v=U_eV8wfMkXU&list=PLqZXAkvF1bPNQER9mLmDbntNfSpzdDIU5&index=13&ab_channel=GregKamradt%28DataIndy%29) demonstrating how to create this."
        )
    with col2_header:
        st.image(
            image="greg_kamradt_youtube_screenshot.png", width=500, caption="https://www.youtube.com/@DataIndependent"
        )

    st.markdown("### Enter your text to rephrase")
    openai_api_key = get_openai_api_key()
    option_tone, option_dialect = get_conversion_options()
    input_text = get_text()

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
        converter = TextConverter(openai_api_key=openai_api_key)
        rephrased_text = converter.convert_text(tone=option_tone, dialect=option_dialect, text=input_text)
        st.write(rephrased_text)

if __name__ == "__main__":
    main()

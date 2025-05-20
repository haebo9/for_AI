# ... existing code ...
import streamlit as st
from model import convert_to_markdown

def main():
    # Set the page configuration for a better layout
    st.set_page_config(
        page_title="Text to Markdown Converter",
        layout="centered",  # Options: "centered", "wide"
        initial_sidebar_state="expanded",
    )

    st.title("Text to Markdown Converter")
    st.write("Convert your plain text into well-formatted Markdown suitable for GitHub README files.")

    # Increase the height of the text area
    user_input = st.text_area("Enter your text here:", height=300)

    if st.button("Convert to Markdown"):
        if user_input:
            # Display a spinner while the conversion is in progress
            with st.spinner('Converting to Markdown...'):
                markdown_text = convert_to_markdown(user_input)
            # Use st.code to display the output in a single block
            st.code(markdown_text, language='markdown')

        else:
            st.warning("Please enter some text to convert.")

    # Add a footer or additional information
    st.markdown("---")
    st.markdown("Developed by [haebo9 github](https://github.com/haebo9/for_AI)")

if __name__ == "__main__":
    main()
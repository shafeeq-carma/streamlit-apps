import streamlit as st
import base64
import requests
from anthropic import Anthropic


def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def analyze_image(image, prompt, api_key):
    encoded_image = encode_image(image)
    # Initialize Anthropic client
    anthropic = Anthropic(api_key=api_key)
    
    try:
        response = anthropic.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": f"image/{image.type.split('/')[-1]}",
                                "data": encoded_image,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ],
        )
        return response.content[0].text
    except Exception as e:
        return f"An error occurred: {str(e)}"

st.title("Claude Vision Image Analyzer")

api_key = st.text_input("Enter your Anthropic API key:", type="password")

if api_key:
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "gif", "webp"])
    prompt = st.text_input("Enter your prompt for Claude:", "Describe this image in detail.")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Analyze Image"):
            with st.spinner("Analyzing..."):
                result = analyze_image(uploaded_file, prompt, api_key)
            st.write("Claude's Analysis:")
            st.write(result)

st.sidebar.title("About")
st.sidebar.info(
    "This app uses Claude's vision capabilities to analyze images. "
    "Upload an image and enter a prompt to get Claude's analysis."
)

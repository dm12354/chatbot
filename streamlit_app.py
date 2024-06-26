import time
import os
import base64
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import torch
from PIL import Image
import whats_new
import terms_of_use
import privacy_policy
import blog_1
import about_us
import logging
import json

# Set page title and favicon
favicon_path = "./favicon.ico"
if os.path.exists(favicon_path):
    st.set_page_config(page_title="CHATBOT.ai", page_icon=favicon_path)

# Load custom CSS
def load_css(file_name):
    with open(file_name, 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css('styles.css')

# Load environment variables
load_dotenv()

# Configure the API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
# Initialize the chat model
chat = model.start_chat(history=[])
# File path for storing chat history
CHAT_HISTORY_FILE = 'chat_history.json'

# Load existing chat history from file
if os.path.exists(CHAT_HISTORY_FILE):
    with open(CHAT_HISTORY_FILE, 'r') as f:
        chat_history = json.load(f)
else:
    chat_history = []

def get_gemini_response(question, retries=2, delay=2):
    for attempt in range(retries):
        try:
            logging.debug(f"Attempt {attempt+1} to get response for question: {question}")
            response = chat.send_message(question, stream=False)  # Stream is set to False for a faster response
            logging.debug("Waiting for the response to resolve...")
            
            # Ensure the response is fully processed
            response.resolve()
            logging.debug(f"Response resolved: {response}")
            
            # Inspect the response object
            logging.debug(f"Response attributes: {dir(response)}")
            
            # Check for the candidates attribute
            if hasattr(response, 'candidates'):
                # Extract the text content correctly
                candidate = response.candidates[0]
                if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                    text_content = candidate.content.parts[0].text
                    logging.debug(f"Extracted text content: {text_content}")
                    
                    # Custom logic to respond with your name
                    if "who made you" in question.lower() or "who created you" in question.lower() or "who developed you" in question.lower() or "who created chatbot.ai" in question.lower() or "who is your creator" in question.lower():
                        return "I am created by Divyansh Mittal. He is a 13 year old boy who is the person behind my existence."
                    else:
                        return text_content
                else:
                    logging.error("Content parts not found in the response candidate.")
                    return "Sorry, I didn't get that. Can you please repeat?"
            else:
                logging.error("No candidates attribute found in the response.")
                return "Sorry, I didn't get that. Can you please repeat."
                
        except Exception as e:
            logging.error(f"Error getting response: {e}")
            if attempt < retries -1:
                time.sleep(delay)
            else:
                return f"An error occurred: {e}"

# Lazy loading for Stable Diffusion model
@st.cache_resource
def load_model():
    from diffusers import StableDiffusionPipeline
    try:
        model = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", low_cpu_mem_usage=True)
        if torch.cuda.is_available():
            model = model.to("cuda")
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Remove Streamlit menu etc. 
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;} 
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Add background image to sidebar
def sidebar_bg(bg_image):
    with open(bg_image, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
            [data-testid="stSidebar"] > div:first-child {{
                background: url(data:image/png;base64,{encoded_string});
                background-size: cover;
                background-position: center;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

sidebar_bg('bg.png')

# Sidebar navigation
st.sidebar.title("Welcome to Chatbot.ai")

def set_nav_item(nav_item):
    st.session_state.selected_nav_item = nav_item

if 'selected_nav_item' not in st.session_state:
    st.session_state.selected_nav_item = "Chatbot"

nav_items = {
    "Chatbot": "Chatbot",
    "What's New?": "What's New?",
    "Privacy Policy": "Privacy Policy",
    "Terms of Use": "Terms of Use",
    "Chat History": "Chat History",
    "Blog": "Blog",
    "Get in Touch": "Get in Touch",
    "About Us": "About Us"
}

icons = {
    "Chatbot": "💬",
    "What's New?": "📰",
    "Privacy Policy": "🛡️",
    "Terms of Use": "📄",
    "Chat History": "⏳",
    "Blog": "✍️",
    "Get in Touch": "☎️",
    "About Us": "👤"
}

for nav_item, display_name in nav_items.items():
    if st.sidebar.button(f"{icons[nav_item]} {display_name}", key=nav_item):
        set_nav_item(nav_item)
        st.rerun()
        st.sidebar.clear()

# Custom CSS for sidebar buttons


page = st.session_state.get('selected_nav_item', "Chatbot")

if page != "Blog":
    # Display the logo only if the current page is not "Blog"
    logo_path = "final logo.png"
    if os.path.exists(logo_path):
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center;">
                <img src="data:image/png;base64,{base64.b64encode(open(logo_path, "rb").read()).decode()}" style="width: 150px;">
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning(f"Logo not found at path: {logo_path}")

if page == "Chatbot":

    st.markdown("<h1 style='text-align: center;'>AI CHATBOT</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; font-size: 12px;'>v1.1.2</h3>", unsafe_allow_html=True)
    if 'toast_shown' not in st.session_state:
        st.toast("CHATBOT.ai just got updated !" , icon = '🗞️')
        st.session_state.toast_shown = True 
 
    st.markdown(
        """
        <style>
        .box {
            border: 1.8px solid grey;
            padding: 20px;
            border-radius: 15px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="box">🎓 How to study effeciently ?</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="box">📝 Brief Description of J.R.D Tata</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="box">🪖 Sacrifices of Indian Freedom Fighters</div>', unsafe_allow_html=True)
    
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        with st.container():
            alignment_class = 'user' if role == 'user' else 'assistant'
            st.markdown(
                f"""
                <div class="chat-message {alignment_class}">
                    <div class="chat-bubble {alignment_class}">
                        {content}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    prompt = st.chat_input("What is up?")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.container():
            st.markdown(
                f"""
                <div class="chat-message user">
                    <div class="chat-bubble user">
                        {prompt}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with st.container():
            try:
                response = get_gemini_response(prompt)
                # Display response letter by letter
                placeholder = st.empty()
                full_response = ""
                for letter in response:
                    full_response += letter
                    placeholder.markdown(
                        f"""
                        <div class="chat-message assistant">
                            <div class="chat-bubble assistant">
                                {full_response}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    time.sleep(0.01)  # Adjust the speed of typing simulation
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.chat_history.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error getting response: {e}")

elif page == "What's New?":
    whats_new.app()

elif page == "Privacy Policy":
    privacy_policy.app()

elif page == "Terms of Use":
    terms_of_use.app()

elif page == "Chat History":
    st.title("Chat History")
    if 'chat_history' in st.session_state:
        for message in st.session_state.chat_history:
            role = message["role"]
            content = message["content"]
            with st.container():
                alignment_class = 'user' if role == 'user' else 'assistant'
            st.markdown(
                f"""
                <div class="chat-message {alignment_class}">
                    <div class="chat-bubble {alignment_class}">
                        {content}
                    </div>
                </div>
                """,
                    unsafe_allow_html=True
                )
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.experimental_rerun()
    else:
        st.write("No Chat History Yet.😞")

elif page == "Blog":
    blog_1.app()

elif page == "About Us":
    about_us.app()

elif page == "Get in Touch":
    st.header("Get in touch with me ! 📫")
    contact_form = """
    <form action="https://formsubmit.co/chatbot.aidm@gmail.com" method="POST">
         <input type="hidden" name="_captcha" value="false">
         <input type="text" name="name" placeholder="Your Name" required>
         <input type="email" name="email" placeholder="Your email" required>
         <textarea name="message" placeholder="Your message" required></textarea>
         <button type="submit">Send</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)

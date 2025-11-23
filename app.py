"""
Multi-Modal Chatbot using Streamlit and Google Gemini API
Install dependencies: pip install streamlit google-generativeai pillow python-dotenv
Run: streamlit run app.py
"""

import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
from datetime import datetime
import io

# Page configuration
st.set_page_config(
    page_title="Multi-Modal AI Chatbot",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stApp {
        background: #000000;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
    }
    .assistant-message {
        background: #1a1a1a;
        color: #ffffff;
        margin-right: 20%;
        box-shadow: 0 2px 5px rgba(255,255,255,0.1);
        border: 1px solid #333;
    }
    .error-message {
        background: #fee;
        color: #c33;
        border: 1px solid #fcc;
        margin-right: 20%;
    }
    .timestamp {
        font-size: 0.75rem;
        opacity: 0.7;
        margin-top: 0.5rem;
    }
    div[data-testid="stButton"] button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    div[data-testid="stButton"] button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'api_key_configured' not in st.session_state:
    st.session_state.api_key_configured = False

if 'gemini_model' not in st.session_state:
    st.session_state.gemini_model = None

# Sidebar for API configuration
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    # API Key input
    api_key = st.text_input(
        "Enter Gemini API Key",
        type="password",
        help="Get your API key from https://makersuite.google.com/app/apikey",
        key="api_key_input"
    )
    
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.session_state.api_key_configured = True
            st.success("✅ API Key configured!")
        except Exception as e:
            st.error(f"❌ Invalid API Key")
            st.session_state.api_key_configured = False
    else:
        st.warning("⚠️ Please enter your Gemini API key")
        st.session_state.api_key_configured = False
    
    st.markdown("---")
    
    # Model selection
    model_option = st.selectbox(
        "Select Model",
        [
            "gemini-2.5-flash",
            "gemini-2.5-pro",
            "gemini-2.0-flash",
            "gemini-flash-latest",
            "gemini-pro-latest"
        ],
        help="Flash is faster, Pro is more powerful",
        index=0
    )
    
    st.markdown("---")
    
    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="Higher values make output more random"
    )
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    # Info section
    st.markdown("""
    ### 📝 Features
    - 💬 Text conversations
    - 🖼️ Image analysis
    - 🔄 Multi-modal input
    - 💾 Chat history
    
    ### 🎯 Tips
    - Upload images for analysis
    - Combine text with images
    - Use clear, specific prompts
    """)

# Main chat interface
st.title("✨ Multi-Modal AI Chatbot")
st.markdown("*Powered by Google Gemini*")

# Chat container
chat_container = st.container()

# Display welcome message if no messages
with chat_container:
    if len(st.session_state.messages) == 0:
        st.info("""
        👋 **Welcome to the Multi-Modal AI Chatbot!**
        
        You can:
        - 💬 Send text messages for conversations
        - 🖼️ Upload images for analysis
        - 🔄 Combine both for contextual understanding
        
        Get started by typing a message or uploading an image below!
        """)
    
    # Display chat messages
    for idx, message in enumerate(st.session_state.messages):
        role = message["role"]
        content = message.get("content", "")
        timestamp = message.get("timestamp", "")
        is_error = message.get("is_error", False)
        
        # Skip empty messages
        if not content and "image" not in message:
            continue
        
        if is_error:
            message_class = "error-message"
        elif role == "user":
            message_class = "user-message"
        else:
            message_class = "assistant-message"
        
        with st.container():
            st.markdown(f'<div class="chat-message {message_class}">', unsafe_allow_html=True)
            
            # Display image if present
            if "image" in message and message["image"] is not None:
                st.image(message["image"], width=300)
            
            # Display text content only if it exists
            if content:
                st.markdown(content)
            
            # Display timestamp
            st.markdown(f'<div class="timestamp">{timestamp}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# Input section at the bottom
st.markdown("---")

# Create columns for layout
col1, col2 = st.columns([1, 3])

with col1:
    uploaded_file = st.file_uploader(
        "📷 Upload Image",
        type=["png", "jpg", "jpeg", "webp"],
        help="Max size: 4MB"
    )
    
    if uploaded_file:
        st.image(uploaded_file, caption="Preview", use_column_width=True)

with col2:
    user_input = st.text_area(
        "💬 Your message",
        placeholder="Type a message or upload an image...",
        height=100,
        key="user_input"
    )
    
    send_button = st.button("🚀 Send Message", use_container_width=True)

# Process message when send button is clicked
if send_button:
    if not st.session_state.api_key_configured:
        st.error("❌ Please configure your Gemini API key in the sidebar!")
    elif not user_input and not uploaded_file:
        st.warning("⚠️ Please enter a message or upload an image!")
    else:
        # Prepare user message
        timestamp = datetime.now().strftime("%I:%M %p")
        user_message = {
            "role": "user",
            "content": user_input if user_input else "Please analyze this image.",
            "timestamp": timestamp
        }
        
        # Add image to user message if uploaded
        if uploaded_file:
            user_message["image"] = uploaded_file
        
        # Add user message to chat
        st.session_state.messages.append(user_message)
        
        # Generate AI response
        try:
            # Initialize the model with correct format - add "models/" prefix
            model_name = f"models/{model_option}" if not model_option.startswith("models/") else model_option
            
            generation_config = {
                "temperature": temperature,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
            }
            
            model = genai.GenerativeModel(
                model_name=model_option,  # Use without models/ prefix
                generation_config=generation_config
            )
            
            st.sidebar.info(f"Using model: {model_option}")
            
            # Prepare content for API
            content_parts = []
            
            if uploaded_file:
                # Process image
                image = Image.open(uploaded_file)
                
                # Check image size
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format=image.format if image.format else 'PNG')
                img_size = img_byte_arr.tell()
                
                if img_size > 4 * 1024 * 1024:  # 4MB limit
                    raise Exception("Image size exceeds 4MB limit")
                
                content_parts.append(image)
            
            # Add text prompt
            prompt = user_input if user_input else "Please analyze this image and describe what you see in detail."
            content_parts.append(prompt)
            
            # Generate response with spinner
            with st.spinner("🤔 Thinking..."):
                response = model.generate_content(content_parts)
                
                # Check if response has text
                if hasattr(response, 'text') and response.text:
                    assistant_response = response.text
                else:
                    # If no text, check candidates
                    if response.candidates:
                        assistant_response = "⚠️ Response was blocked or empty. Try rephrasing your prompt."
                    else:
                        assistant_response = "❌ No response generated. Please try again."
            
            # Add assistant message to chat
            assistant_message = {
                "role": "assistant",
                "content": assistant_response,
                "timestamp": datetime.now().strftime("%I:%M %p")
            }
            st.session_state.messages.append(assistant_message)
            
        except Exception as e:
            # Add error message to chat with more details
            error_details = str(e)
            error_message = {
                "role": "assistant",
                "content": f"❌ Error: {error_details}\n\nModel tried: {model_option}\n\nTry selecting a different model from the sidebar.",
                "timestamp": datetime.now().strftime("%I:%M %p"),
                "is_error": True
            }
            st.session_state.messages.append(error_message)
            st.error(f"Full error: {error_details}")
        
        # Rerun to update chat display
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Built with ❤️ using Streamlit and Google Gemini AI</p>
</div>
""", unsafe_allow_html=True)
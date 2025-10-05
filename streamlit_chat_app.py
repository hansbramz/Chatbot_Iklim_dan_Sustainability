import streamlit as st
import google.generativeai as genai

# --- 1. Page Configuration and Title ---
st.set_page_config(page_title="Climate Helper Chatbot", layout="centered")
st.title("🌱 Climate Helper Chatbot")
st.subheader("Your AI assistant for climate, solar, and sustainability questions via Gemini Flash model")
st.write("---")

# --- 2. Sidebar for Settings ---
with st.sidebar:
    google_api_key = st.text_input("Google AI API Key", key="google_api_key_input", type="password")
    st.markdown("Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)")
    reset_button = st.button("Reset Chat", type="primary")

# --- 3. API Key and Model Initialization ---
# Check if the user has provided an API key.
if not google_api_key:
    st.info("Please add your Google AI API key in the sidebar to start chatting.", icon="🗝️")
    st.stop()

# Configure the genai library with the API key.
try:
    genai.configure(api_key=google_api_key)
except Exception as e:
    st.error(f"Invalid API Key or configuration error: {e}")
    st.stop()
st.write("---")

# --- 4. Chat History Management ---
# Handle the reset button click
if reset_button:
    st.session_state.pop("messages", None)
    st.rerun()

# Initialize chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Halo! Aku asisten iklimmu. Tanyakan apa saja tentang energi surya, keberlanjutan, atau ilmu iklim. Mau dibantu apa hari ini?﻿"
        }
    ]

# --- 5. Display Past Messages ---
def display_messages():
    """Display all messages in the chat history"""
    for msg in st.session_state.messages:
        author = "user" if msg["role"] == "user" else "assistant"
        with st.chat_message(author):
            st.write(msg["content"])

def friendly_wrap(raw_text):
    """Add a friendly tone to AI responses"""
    return (
        "Pertanyaan bagus banget! 🌱\n\n"
        f"{raw_text.strip()}\n\n"
        "Apakah Anda ingin saya menjelaskan lebih lanjut tentang bagian ini, atau apakah Anda memiliki pertanyaan lain tentang iklim?﻿"
    )

display_messages()

# --- 6. Handle User Input and Generate Response ---
prompt = st.chat_input("Tanyakan saya tentang iklim, pemasangan solar panel, dan sustainability...")

if prompt:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Show user message
    with st.chat_message("user"):
        st.write(prompt)

    # Show thinking indicator while processing
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.write("🤔 Berpikir...")

        try:
            # Create the model instance after configuring the API key.
            # This is the correct way for modern library versions.
            model = genai.GenerativeModel('gemini-2.5-flash')

            response = model.generate_content(
                f"Anda adalah ahli iklim dan keberlanjutan yang sangat membantu. Tolong berikan informasi yang akurat dan membangkitkan semangat tentang:﻿ {prompt}"
            )

            # Extract response text
            answer = response.text
            friendly_answer = friendly_wrap(answer)

        except Exception as e:
            friendly_answer = f"Maafkan, Saya menemukan sebuah error: {e}. Tolong tanyakan pertanyaannya sekali lagi."

        # Replace thinking indicator with actual response
        placeholder.write(friendly_answer)

        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": friendly_answer})

    # Refresh the page to show the full chat history
    st.rerun()

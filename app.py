"""
app.py
"""
import streamlit as st
from openai import OpenAI

from utils import (
    append_to_sheet,
    moderation_check,
    text_to_speech,
    zero_shot_nsfw_classifier
)

DEFAULT_TEXT = """This document reflects the strategy we’ve refined over the past two years, 

including feedback from many people internal and external to OpenAI. The timeline to AGI remains uncertain, 

but our Charter will guide us in acting in the best interests of humanity throughout its development.

OpenAI’s mission is to ensure that artificial general intelligence (AGI)—by which we mean 

highly autonomous systems that outperform humans at most economically valuable work—benefits all of humanity.

We will attempt to directly build safe and beneficial AGI, but will also consider our mission fulfilled 

if our work aids others to achieve this outcome. To that end, we commit to the following principles:

Broadly distributed benefits

"""

st.set_page_config(page_title="AI Text-to-Speech",
                   page_icon="🎙")

st.title("Try OpenAI's Text-to-Speech 🎙")
with st.expander("About this app"):
    st.info("""
    This is a personal project, not affliated with OpenAI.
            
    **Contact:**  or [LinkedIn](https://www.linkedin.com/in/tundechrisbello/)
    """)
    
if "audio" not in st.session_state:
    st.session_state["audio"] = None

text = st.text_area("Your text", value = DEFAULT_TEXT, max_chars=4096, height=250)
voice = st.radio("Voice", ["alloy", "echo", "fable", "onyx", "nova", "shimmer"], horizontal = True, help="Previews can be found [here](https://platform.openai.com/docs/guides/text-to-speech/voice-options)")

if st.button("Generate Audio"):

    if len(text) == 0:
        st.warning("Please enter a text.", icon="🚫")

    if (moderation_check(text)) or (zero_shot_nsfw_classifier(text) == 1):
        st.warning("This text has been flagged as NSFW. Please revise it.", icon="🚫")
        append_to_sheet(text, voice, False)
        st.stop()
    
    with st.spinner("Generating your audio - this can take up to 30 seconds..."):
        st.session_state["audio"] = text_to_speech(text, voice)
        append_to_sheet(text, voice, True)

        audio_file = open("audio.mp3", 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mpeg')
        
        st.download_button(label="Download audio",
                             data=audio_bytes,
                             file_name="audio.mp3",
                             mime="audio/mp3")

import replicate
import streamlit as st
import requests
import io
import json
import os
from datetime import datetime
from PIL import Image
from streamlit_image_select import image_select 
import uuid

st.set_page_config(page_title="Icarus Image Generator", page_icon=":bow_and_arrow:", layout="wide")

st.image("gifs/pug_resized.gif")
st.markdown("# :orange[Icarus Text-to-Image Generator🔥]")

st.markdown(
    """
    <style>
    .orange-info {
        border-radius: 0.25rem;
        background-color: #D2B48C;
        padding: 1rem;
        color: white;
        font-size: 1rem;
    }
    .centered-image {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .centered-image img {
        width: 50%;
        max-width: 400px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


try:
    DEFAULT_REPLICATE_API_KEY = st.secrets["REPLICATE_API_TOKEN"]
    MODEL_ENDPOINT = st.secrets["REPLICATE_MODEL_ENDPOINT"]
except KeyError:
    st.error("API Key and Model Endpoint are not set. Please add them in the Streamlit Secrets.")
    st.stop()


if "user_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())


USER_LIMIT = 3
DAILY_LIMIT = 24
USER_COUNTER_FILE = "user_usage_counter.json"
GLOBAL_COUNTER_FILE = "global_usage_counter.json"


def init_global_counter():
    if os.path.exists(GLOBAL_COUNTER_FILE):
        with open(GLOBAL_COUNTER_FILE, "r") as file:
            data = json.load(file)
    else:
        data = {"date": str(datetime.now().date()), "count": 0}
    return data


def init_user_counter():
    if os.path.exists(USER_COUNTER_FILE):
        with open(USER_COUNTER_FILE, "r") as file:
            data = json.load(file)
    else:
        data = {}
    if st.session_state["user_id"] not in data:
        data[st.session_state["user_id"]] = {"date": str(datetime.now().date()), "count": 0}
    return data


def save_global_counter(data):
    with open(GLOBAL_COUNTER_FILE, "w") as file:
        json.dump(data, file)


def save_user_counter(data):
    with open(USER_COUNTER_FILE, "w") as file:
        json.dump(data, file)


global_counter = init_global_counter()
user_counter = init_user_counter()
today = str(datetime.now().date())

if global_counter["date"] != today:
    global_counter = {"date": today, "count": 0}
save_global_counter(global_counter)

if user_counter[st.session_state["user_id"]]["date"] != today:
    user_counter[st.session_state["user_id"]] = {"date": today, "count": 0}
save_user_counter(user_counter)


if "user_requests" not in st.session_state:
    st.session_state["user_requests"] = user_counter[st.session_state["user_id"]]["count"]
else:
    user_counter[st.session_state["user_id"]]["count"] = st.session_state["user_requests"]
    save_user_counter(user_counter)


def check_limits():
    if global_counter["count"] >= DAILY_LIMIT:
        st.warning("Daily limit for generated images reached. Please try again tomorrow.")
        st.stop()

    if st.session_state["user_requests"] >= USER_LIMIT:
        st.warning("You have reached the limit of generated images for this session.")
        st.stop()



def setup_sidebar():
    with st.sidebar:
        api_option = st.radio("Choose API Option", ["Use Free API Key (Capped)", "Use Your Own API Key"])
        if api_option == "Use Free API Key (Capped)":
            check_limits()
            api_key = DEFAULT_REPLICATE_API_KEY
        else:
            api_key = st.text_input("Enter your Replicate API Key", type="password")
            if not api_key:
                st.warning("Please enter your Replicate API Key.")
                st.stop()

        with st.form("input_form"):
            st.markdown('<div class="orange-info">Welcome to Icarus text-to-image generator! 😎</div>', unsafe_allow_html=True)
            style = st.selectbox(":orange[**Choose Art Style**]", ["Photography", "Anime", "Paint", "Pixel Art", "Comic Book", "Vintage"])
            img_width = st.number_input(":orange[**Width of output image**]", value=1024, help="Width must be divisible by 8. Examples: 1024, 1280, 1920")
            img_height = st.number_input(":orange[**Height of output image**]", value=1024, help="Height must be divisible by 8. Examples: 1024, 1280, 1920")
            prompt_text = st.text_area(":orange[**Prompt what you want ✒️**]")
            submit_button = st.form_submit_button("Submit", type="primary", use_container_width=True)

        st.divider()
        st.subheader("📖 Resources")
        st.markdown("""
                    - Model Used: [Stability AI SDXL](https://replicate.com/stability-ai/sdxl)
                    - API: [Replicate](https://replicate.com)
                    - Streamlit: [streamlit.io](https://streamlit.io)
                    - Gallery: [Gallery](https://streamlit.io/gallery)
        """)
        st.divider()
        st.subheader("👨‍💻 Contact")
        st.markdown("""
                    - Github → [Hugosh71](https://github.com/Hugosh71)
                    - LinkedIn → [Hugo Fanchini](https://www.linkedin.com/in/hugo-fanchini-386833252)
                    - Yahoo → [fanchinihugo@yahoo.fr](mailto:fanchinihugo@yahoo.fr)
                    - Portfolio → [Portfolio](https://hugo-fanchini.com/)
                    """)
    return submit_button, style, img_width, img_height, prompt_text, api_key, api_option


def generate_image(prompt, width, height, style, api_key):
    os.environ["REPLICATE_API_TOKEN"] = api_key
    full_prompt = f"{prompt}, {style} style"
    response = replicate.run(
        MODEL_ENDPOINT,
        input={
            "prompt": full_prompt,
            "negative_prompt": "A bad quality image with distorded features",
            "width": width,
            "height": height,
            "scheduler": "K_EULER_ANCESTRAL",
            "num_inference_steps": 50,
            "guidance_scale": 7.5,
            "prompt_strength": 0.8,
            "refine": "no_refiner",
            "high_noise_frac": 0.8
        }
    )
    return response


def main_content(user_request, style, width, height, prompt, api_key, api_option):
    if user_request:
        with st.spinner('Generating your image...☕'):
            try:
                images = generate_image(prompt, width, height, style, api_key)
                if images:
                    st.toast('Image generated!', icon='🤘')
                    st.session_state["generated_images"] = images
                    display_images(images, style)
                    if api_option == "Use Free API Key (Capped)":
                        st.session_state["user_requests"] += 1
                        global_counter["count"] += 1
                        user_counter[st.session_state["user_id"]]["count"] = st.session_state["user_requests"]
                        save_global_counter(global_counter)
                        save_user_counter(user_counter)
            except Exception as e:
                st.error(f'Error: {e}', icon="🚨")
    if not st.session_state.get("generated_images"):
        display_gallery()  


def display_images(images, style):
    for img_url in images:
        img_response = requests.get(img_url)
        if img_response.status_code == 200:
            img_data = img_response.content
            img = Image.open(io.BytesIO(img_data))
            st.image(img, caption=f"Generated Image ({style})", width=512)  
            st.download_button(
                label="Download Image",
                data=img_data,
                file_name=f"Icarus_image_{style}.png",
                mime="image/png",
                use_container_width=True
            )
        else:
            st.error(f"Failed to load image from {img_url}")


def display_gallery():
    st.markdown("# :rainbow[Image Gallery]")
    images = [
        ("images/Icarus_image_Photography.png", "A beautiful sunset over the ocean (Photography)"),
        ("images/Icarus_image_Anime.png", "A weary office worker slumped at their desk, surrounded by piles of paperwork. (Anime)"),
        ("images/Icarus_image_Paint.png", "A charming dog preparing a delicious meal for his friends. (Paint)"),
        ("images/Icarus_image_Pixel Art.png", "A fierce blond Viking warrior wielding a mighty axe, standing on a rugged landscape with a stormy sky. (Pixel Art)"),
        ("images/Icarus_image_Comic Book.png", "A superhero wearing a cape striking a powerful pose as he flies through a futuristic cityscape at night. (Comic Book)"),
        ("images/Icarus_image_Vintage.png", "A London gangster from the 1980s, casually posing in front of a classic car. (Vintage)"),
    ]
    selected_image = image_select(
        label="Select an image to view",
        images=[img[0] for img in images],
        captions=[img[1] for img in images],
        use_container_width=True
    )
    if selected_image:
        st.markdown('<div class="centered-image">', unsafe_allow_html=True)
        st.image(selected_image, use_column_width=False, width=400) 
        st.markdown('</div>', unsafe_allow_html=True)


def main():
    user_request, style, width, height, prompt, api_key, api_option = setup_sidebar()
    main_content(user_request, style, width, height, prompt, api_key, api_option)

if __name__ == "__main__":
    main()

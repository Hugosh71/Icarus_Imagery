#  Icarus Text-to-Image Generator 🎨

Welcome to the **Icarus Text-to-Image Generator**! This app utilizes Replicate's API to generate stunning images from text prompts.

Available here : [Icarus Imagery](https://icarusimagery.streamlit.app/)

![Vintage Gangster](./images/Icarus_image_Vintage.png)

## 🚀 Features

- **Multiple Art Styles**: Choose from Photography, Anime, Paint, Pixel Art, Comic Book, and Vintage.
- **Customizable Output**: Set your desired image width and height.
- **Download Options**: Easily download generated images.
- **API Key Options**: Use a free API key with usage limits or enter your own API key.

## 📖 Resources
- **Streamlit**: An open-source app framework in Python. It allows you to create beautiful, performant apps quickly.
- **Replicate**: An API that enables you to run machine learning models in the cloud.
- **Streamlit Image Select**: A custom Streamlit component that allows users to select images from a gallery. This is used in the image gallery section of the app to enhance user interaction.
- **Stability AI SDXL**: Stability AI's Stable Diffusion SDXL is a state-of-the-art text-to-image generation model. It excels in producing high-resolution, detailed images from textual descriptions, offering versatile art styles and fine-grained control over the output.


## How to use

1. Clone this repository:

   ```bash
   git clone https://github.com/Hugosh71/Icarus_Imagery.git
   ```

2. Navigate to the project directory:

   ```bash
   cd IcarusImagery
   ```

3. Install the dependencies:

   ```python
   pip install -r requirements.txt
   ```

4. Go to secrets.toml and paste your Replicate API token and your model endpoint:
   ```bash
   REPLICATE_API_TOKEN = "Your_API_Key_Here"
   REPLICATE_MODEL_ENDPOINT = "Your_Model_Endpoint_Here"
   ```
   
## How to run

1. Run the Streamlit app:

   ```python
   streamlit run app.py
   ```

2. You should on your terminal an url , Enjoy !

## Acknowledgment

- **Model**:[Stability AI sdxl](https://replicate.com/stability-ai/sdxl)
- **License**: [CreativeML Open RAIL++-M License](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/LICENSE.md)
- **Developed by**: [Stability AI](https://stability.ai/)
  

## 📜 License  

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Hugosh71/Icarus_Imagery/blob/main/LICENSE)

It is based on the original work by Tony Kipkemboi, the original project can be found [Here](https://github.com/tonykipkemboi/streamlit-replicate-img-app/tree/main)





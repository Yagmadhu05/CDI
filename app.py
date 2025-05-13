import cv2
import pandas as pd
import streamlit as st
import numpy as np
from PIL import Image

# Load CSV with color data
@st.cache_data
def load_colors():
    return pd.read_csv("colors.csv")

def get_closest_color(r, g, b, df):
    minimum = float('inf')
    cname = "Unknown"
    for i in range(len(df)):
        d = abs(r - df.loc[i, "R"]) + abs(g - df.loc[i, "G"]) + abs(b - df.loc[i, "B"])
        if d < minimum:
            minimum = d
            cname = df.loc[i, "color_name"]
    return cname

# Load image and convert
def process_image(uploaded_file):
    image = Image.open(uploaded_file)
    return np.array(image)

# Main app
def main():
    st.title("🎨 Color Detection from Images")
    df = load_colors()

    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image = process_image(uploaded_file)
        st.image(image, caption="Click to detect color", use_column_width=True)

        # Get click
        click = st.image(image, use_column_width=True)
        x = st.slider("X-coordinate", 0, image.shape[1] - 1)
        y = st.slider("Y-coordinate", 0, image.shape[0] - 1)

        r, g, b = image[y, x]
        color_name = get_closest_color(r, g, b, df)

        st.markdown(f"**Detected Color:** {color_name}")
        st.markdown(f"**RGB:** ({r}, {g}, {b})")
        st.markdown(
            f"<div style='width:100px;height:50px;background-color:rgb({r},{g},{b});'></div>",
            unsafe_allow_html=True,
        )

if __name__ == "__main__":
    main()

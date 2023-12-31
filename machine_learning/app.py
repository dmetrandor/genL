import streamlit as st
import numpy as np
import io
from PIL import Image
import style_look_description_generator as prompt_generator
import style_look_picture_generator as picture_generator
import imgru
import google_lenz_api
import re

def get_pil_image(file):
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    return file_bytes


# Title of the web app
st.title("GENL - Generate New Look")

# Input window for textual description of personality
personality_description = st.text_area("Enter Textual Description of Personality")

# Initialize a list to store information about each uploaded picture
uploaded_files_info = []

# Upload form for reference pictures (moodboard or clothes)
st.subheader("Upload Reference Pictures")
uploaded_files = st.file_uploader("Upload one or more reference pictures", accept_multiple_files=True)

# Create a list of options for picture type (moodboard or clothes)
picture_types = ["Moodboard", "Clothes"]

# Loop through uploaded pictures and create dropdowns for each
if uploaded_files:
    st.write("Specify the type for each uploaded picture:")
    for file in uploaded_files:
        # Display filename with larger font and highlighting
        pil_image = get_pil_image(file)
        st.markdown(f"**{file.name}**")
        picture_type = st.selectbox(f"Select type for {file.name}", picture_types)
        uploaded_files_info.append({"file": pil_image, "type": picture_type})

# Input form for style look goal
style_goal = st.text_area("Enter Style Look Goal")

# Process button to generate style look description and picture
if st.button("Generate"):
    st.spinner("Generating...")  # Display a spinner

    with st.spinner('Wait for it...'):
        # Generate style look description and picture
        style_look_description = prompt_generator.generate_style_look_description(personality_description, style_goal, uploaded_files_info)
        style_look_image = picture_generator.generate_style_look_picture(style_look_description)
    st.success('Generated!')

    # Display the generated picture
    st.write("Generated Style Look Picture:")
    st.image(style_look_image, use_column_width=True)

    url = imgru.create_url(style_look_image)
    shopping_df = google_lenz_api.query(url)
    shopping_df['price'] = shopping_df['price'].apply(lambda x: '$'+re.sub(r'[^0-9.]', '', x))
    shopping_df = shopping_df.sort_values(by='price')

    st.data_editor(
        shopping_df,
        column_config={
            "pic": st.column_config.ImageColumn(
                "Preview Image",
            ),
            "link": st.column_config.LinkColumn(
                "Shops",
            ),
            "price": st.column_config.NumberColumn(
                "Price (in USD)",
                help="The price of the product in USD",
                min_value=0,
                max_value=1000,
                step=1,
                format="$%d",
            ),
        },
        hide_index=True,
    )


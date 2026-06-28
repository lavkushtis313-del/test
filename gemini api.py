import streamlit as st
from PIL import Image
import google.generativeai as genai


# GEMINI API KEY
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]


genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


# STREAMLIT UI

st.set_page_config(
    page_title="AI Price Estimator",
    layout="centered"
)

st.title(" AI Item Price Estimator")

st.write(
    "Upload an image and provide a description. "
    "Gemini will analyze the item and estimate its market value."
)

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png", "webp"]
)

description = st.text_area(
    "Item Description",
    placeholder="Example: Used iPhone 14 Pro 256GB, excellent condition, purchased in 2023..."
)


# PRICE ESTIMATION

if st.button("Estimate Price"):

    if uploaded_file is None:
        st.warning("Please upload an image.")
        st.stop()

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Item",
        use_container_width=True
    )

    prompt = f"""
    You are an expert product valuation specialist.

    Analyze the uploaded image and the user's description.

    User Description:
    {description}

    Determine:

    1. What the item appears to be.
    2. Its likely condition.
    3. Estimated price range in USD.
    4. Estimated price range in INR.
    5. Confidence score (0-100%).
    6. Key factors affecting the valuation.
    7. A short summary.

    Return the answer in clean markdown format.
    """

    try:
        with st.spinner("Analyzing item and estimating value..."):

            response = model.generate_content(
                [prompt, image]
            )

        st.subheader(" Estimated Value")
        st.markdown(response.text)

    except Exception as e:
        st.error(f"Error: {e}")
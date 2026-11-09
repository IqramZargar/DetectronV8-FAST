from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st
from PIL import Image, UnidentifiedImageError

# Import the EXISTING detection function. The original YOLO implementation in
# utils.py remains the single source of truth and loads its model once per process.
from utils import run_detection


st.set_page_config(
    page_title="DetectronV8 | Object Detection",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
      html, body, [class*="css"] { font-family: Inter, sans-serif; }
      .stApp {
        background:
          radial-gradient(circle at 12% 8%, rgba(37,99,235,.16), transparent 32%),
          linear-gradient(135deg, #0b1020 0%, #0f0f0f 58%, #111827 100%);
        color: #f8fafc;
      }
      [data-testid="stHeader"] { background: rgba(15,15,15,.72); }
      .block-container { max-width: 1180px; padding-top: 2rem; }
      .hero {
        padding: 2rem 2.2rem; border-radius: 24px;
        border: 1px solid rgba(96,165,250,.28);
        background: linear-gradient(145deg, rgba(96,165,250,.12), rgba(37,99,235,.06)), #1a1a2e;
        box-shadow: 0 18px 44px rgba(0,0,0,.30); margin-bottom: 1.2rem;
      }
      .eyebrow { color: #93c5fd; font-size: .78rem; letter-spacing: .16em; font-weight: 800; text-transform: uppercase; }
      .hero h1 { font-family: 'Space Grotesk', sans-serif; font-size: clamp(2rem,5vw,3.3rem); margin: .35rem 0; color: #f8fafc; }
      .hero p { color: rgba(248,250,252,.76); font-size: 1rem; margin: 0; }
      .panel {
        background: linear-gradient(180deg, rgba(37,99,235,.08), transparent 35%), #171b2b;
        border: 1px solid rgba(96,165,250,.18); border-radius: 18px;
        padding: 1.1rem 1.2rem; margin-bottom: 1rem;
      }
      .small-muted { color: rgba(248,250,252,.65); font-size: .9rem; }
      div.stButton > button, div.stDownloadButton > button {
        border-radius: 10px; border: 1px solid #3b82f6;
        background: linear-gradient(90deg,#2563eb,#1d4ed8); color: white;
        font-weight: 700; min-height: 2.8rem;
      }
      div.stButton > button:hover, div.stDownloadButton > button:hover {
        border-color: #93c5fd; color: white; background: #1e40af;
      }
      [data-testid="stFileUploader"] {
        border: 1px dashed rgba(96,165,250,.5); border-radius: 14px;
        background: rgba(37,99,235,.05); padding: .5rem;
      }
      section[data-testid="stSidebar"] {
        background: #111827; border-right: 1px solid rgba(96,165,250,.18);
      }
      .metric-card {
        background: #1a1a2e; border: 1px solid rgba(96,165,250,.18);
        padding: 1rem; border-radius: 14px;
      }
      footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## 🎯 DetectronV8")
    page = st.radio("Navigation", ["Detect", "About"], label_visibility="collapsed")
    st.divider()
    st.caption("YOLOv8 Nano · Computer Vision")
    st.caption("CPU inference · Public demo")

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Computer Vision · YOLOv8</div>
      <h1>DetectronV8</h1>
      <p>Fast object detection. Upload an image, detect objects, and inspect the annotated result.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if page == "About":
    st.markdown("### About this project")
    st.markdown(
        """
        DetectronV8 is an image-based object detection application powered by
        **YOLOv8 Nano**, **OpenCV**, and the original Python detection pipeline.

        The app returns:
        - An image annotated with bounding boxes and class labels.
        - A list of detected objects and confidence scores.

        **Original project architecture**
        - FastAPI + Jinja2: retained in `main.py` and `templates/`.
        - Detection implementation: retained in `utils.py`.
        - Model weights: `yolov8n.pt`.
        - Streamlit: an additional public-hosting interface for Community Cloud.
        """
    )
    st.info("The original FastAPI website and HTML templates remain in this repository. This Streamlit page is an additional deployment entry point.")
else:
    st.markdown("### Start detection")
    st.markdown(
        '<p class="small-muted">Upload a JPG, JPEG, or PNG image. The existing '
        'YOLOv8 detection function will process it on CPU.</p>',
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        uploaded = st.file_uploader(
            "Choose an image",
            type=["jpg", "jpeg", "png"],
            help="Maximum upload size: 10 MB.",
        )
        detect_clicked = st.button("🔍 Detect Objects", type="primary", use_container_width=True)

    if detect_clicked:
        if uploaded is None:
            st.warning("Please upload an image first.")
        elif uploaded.size > 10 * 1024 * 1024:
            st.error("This image is larger than 10 MB. Please upload a smaller image.")
        else:
            try:
                image_bytes = uploaded.getvalue()
                with Image.open(__import__("io").BytesIO(image_bytes)) as check_image:
                    check_image.verify()
                with Image.open(__import__("io").BytesIO(image_bytes)) as check_image:
                    width, height = check_image.size
                    if width * height > 25_000_000:
                        raise ValueError("Image dimensions are too large (maximum 25 megapixels).")
                    image_format = (check_image.format or "").upper()
                    suffix = ".png" if image_format == "PNG" else ".jpg"

                with st.spinner("Loading YOLOv8 and detecting objects..."):
                    # Temporary input/output paths prevent uploaded files from
                    # accumulating on Streamlit Community Cloud's local disk.
                    with tempfile.TemporaryDirectory(prefix="detectronv8_") as temp_dir:
                        temp_path = Path(temp_dir)
                        input_path = temp_path / f"input{suffix}"
                        output_dir = temp_path / "processed"
                        input_path.write_bytes(image_bytes)

                        output_path, detections = run_detection(
                            str(input_path),
                            str(output_dir),
                        )
                        output_bytes = Path(output_path).read_bytes()

                st.session_state["detectron_result"] = {
                    "image": output_bytes,
                    "detections": detections or [],
                    "filename": uploaded.name,
                }
            except (UnidentifiedImageError, OSError):
                st.error("The uploaded file is not a valid supported image.")
            except ValueError as exc:
                st.error(str(exc))
            except Exception as exc:
                st.error("Detection failed. Please try another image. If this continues, check the app logs.")

    result = st.session_state.get("detectron_result")
    if result:
        st.markdown("### Detection results")
        left, right = st.columns([1.35, 1], gap="large")
        with left:
            st.image(result["image"], caption="YOLOv8 annotated image", use_container_width=True)
            st.download_button(
                "⬇️ Download annotated image",
                data=result["image"],
                file_name="detectronv8_result.jpg",
                mime="image/jpeg",
                use_container_width=True,
            )
        with right:
            detections = result["detections"]
            st.metric("Objects detected", len(detections))
            if detections:
                rows = [
                    {
                        "Object": item.get("label", "unknown"),
                        "Confidence": f'{float(item.get("confidence", 0)) * 100:.1f}%',
                    }
                    for item in detections
                ]
                st.dataframe(rows, hide_index=True, use_container_width=True)
            else:
                st.info("No objects were detected in this image.")

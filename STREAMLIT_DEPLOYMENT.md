# DetectronV8-FAST: Streamlit Community Cloud deployment

## What this deployment changes — and what it preserves

- `utils.py` is unchanged: Streamlit calls the original `run_detection()` function.
- `yolov8n.pt` is unchanged.
- `main.py`, `templates/`, and `static/` are retained unchanged. The original FastAPI/Jinja2 site remains in the repository.
- `streamlit_app.py` is an additional hosting entry point. It provides a Streamlit interface with the same upload → YOLO detection → annotated image + confidence results workflow.
- Important: Streamlit Community Cloud will display the Streamlit interface, not render the original FastAPI/Jinja2 templates. The exact original website appearance requires a host that supports running FastAPI (for example, a suitable container host).

## 1. Use your existing GitHub repository

Recommended: add these files to your existing `IqramZargar/DetectronV8-Fast` repository. Do not delete or replace the existing files.

Add:
- `streamlit_app.py`
- `.streamlit/config.toml`

Update:
- `requirements.txt` (Streamlit was added; original dependencies are retained)

All original files are included in this deployment package as well. Compare before overwriting if you have made newer edits on GitHub since downloading the original ZIP.

## 2. Push changes to GitHub

If you already cloned the repo:

```bash
git pull
```

Copy the new `streamlit_app.py` and `.streamlit/config.toml` into the repository and update `requirements.txt` from this package.

Then:

```bash
git add streamlit_app.py .streamlit/config.toml requirements.txt
git commit -m "Add Streamlit Community Cloud deployment"
git push origin main
```

If your default branch is `master`, replace `main` with `master`.

## 3. Deploy on Streamlit Community Cloud

1. Open https://share.streamlit.io/
2. Sign in with GitHub and authorize access to the public repository.
3. Click **Create app**.
4. Choose repository: `IqramZargar/DetectronV8-Fast`.
5. Choose branch: `main` (or your actual default branch).
6. Set **Main file path** to `streamlit_app.py`.
7. In Advanced settings, select Python 3.11 if offered.
8. Click **Deploy**.

Official deployment guide:
https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## 4. Test

When the app finishes building:
1. Open the assigned `*.streamlit.app` URL.
2. Upload a small JPG or PNG (start with a 1–2 MB image).
3. Click Detect Objects.
4. Confirm the annotated image and confidence table appear.
5. Test the download button.

If build or runtime fails, open **Manage app → Logs** and share the complete error text. Do not change PyTorch versions randomly before reviewing the actual error.

## Resource note

Community Cloud resource limits vary and can throttle or stop apps that exceed them. PyTorch + Ultralytics can be memory-heavy. This package uses CPU PyTorch and keeps the original YOLO model loaded once through the existing `utils.py` module. A successful deployment still needs a real inference test.

Official resource guidance:
https://docs.streamlit.io/deploy/streamlit-community-cloud/status

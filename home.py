import streamlit as st
import os
import uuid

st.set_page_config(page_title="Portfolio", layout="wide")


IMAGES_ROOT = "images"
ABOUT_DIR = os.path.join(IMAGES_ROOT, "about")
CERTS_DIR = os.path.join(IMAGES_ROOT, "certs")
PDFS_DIR = os.path.join(IMAGES_ROOT, "pdfs")
os.makedirs(ABOUT_DIR, exist_ok=True)
os.makedirs(CERTS_DIR, exist_ok=True)
os.makedirs(PDFS_DIR, exist_ok=True)
SCHOOL_DIR = os.path.join(IMAGES_ROOT, "school")
os.makedirs(SCHOOL_DIR, exist_ok=True)


def save_uploaded_file(uploaded_file, folder):
    ext = os.path.splitext(uploaded_file.name)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(folder, filename)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path


def list_saved_images(folder):
    files = []
    if os.path.exists(folder):
        for name in os.listdir(folder):
            lower = name.lower()
            if lower.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                files.append(os.path.join(folder, name))
    files.sort()
    return files


def list_saved_pdfs(folder):
    files = []
    if os.path.exists(folder):
        for name in os.listdir(folder):
            if name.lower().endswith('.pdf'):
                files.append(os.path.join(folder, name))
    files.sort()
    return files


def display_gallery(folder, title, cols=3, thumb_width=300, caption_prefix="Saved image"):
    saved = list_saved_images(folder)
    if saved:
        st.subheader(title)
        n = min(cols, len(saved))
        cols_elems = st.columns(n)
        for idx, path in enumerate(saved):
            cols_elems[idx % n].image(path, caption=f"{caption_prefix} {idx+1}", width=thumb_width)


def display_pdfs(folder, title):
    saved = list_saved_pdfs(folder)
    if saved:
        st.subheader(title)
        for path in saved:
            fname = os.path.basename(path)
            st.write(fname)
            with open(path, "rb") as f:
                data = f.read()
            st.download_button("Download PDF", data, file_name=fname, mime="application/pdf")
            # link to raw file in this repo (useful if the app is public and files are committed to the repo)
            raw_url = f"https://raw.githubusercontent.com/David-milltank/portfolio/main/{path}"
            st.markdown(f"[Open in new tab]({raw_url})")


# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "Home"

page = st.sidebar.selectbox(
    "Navigate",
    ["Home", "About Me", "Certifications", "School"],
    index=["Home", "About Me", "Certifications", "School"].index(st.session_state.page)
)
st.session_state.page = page

if page == "Home":
    st.title("Welcome to daves Portfolio (credits to Low Li Wen for helping me with the code)")
    
    st.write("---")
    st.subheader("Quick Navigation")
    col1, col2, col3 = st.columns(3)

    # Show saved PDFs (e.g. Letter of Recommendation, Resume)
    st.write("Letter of recommendation")
    # Public raw GitHub link for the LOR (so visitors on other machines can open it)
    LOR_RAW = "https://raw.githubusercontent.com/David-milltank/portfolio/main/LOR%202026%20Dave.pdf"
    st.write(LOR_RAW)
    st.write("Please click the link below to open the LOR in a new tab.")

    with col1:
        if st.button(" About Me", use_container_width=True):
            st.session_state.page = "About Me"
            st.rerun()
    
    with col2:
        if st.button(" Certs", use_container_width=True):
            st.session_state.page = "Certifications"
            st.rerun()
    
    with col3:
        if st.button(" School Experience", use_container_width=True):
            st.session_state.page = "School"
            st.rerun()

    # Public link to the Letter of Recommendation PDF hosted in the repo (or any public https URL).
    st.markdown(
        f'<a href="{LOR_RAW}" target="_blank" rel="noopener noreferrer">Open Letter of Recommendation (LOR 2026)</a>',
        unsafe_allow_html=True,
    )
    
    st.write("---")
    
   
elif page == "About Me":
    st.title("About Me")
    
    display_gallery(ABOUT_DIR, "Saved About / Profile Images", cols=3, thumb_width=200, caption_prefix="Saved image")
    st.write(" Hi,I'm dave.")
    st.write("I am the vice president of robotics in my school, and I have been programming for 2 years. I am decent in Python, and I was able to join many competitions. I enjoy playing sports in my f[...]")
    
    st.header("My Passion")
    st.write("My passion for coding started when my mother signed me up for a coding class when I was still a kid. It was a class for building LEGO robots and coding them to do different tasks. I got [...]
    

elif page == "Certifications":
    st.title("Certifications")
    st.write("Upload your certificate images here so visitors can see your achievements.")
    cert_images = st.file_uploader(
        "Upload certification images",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="cert_upload",
    )
    if st.button("Save Certification Images"):
        if cert_images:
            saved_paths = []
            for image in cert_images:
                saved_paths.append(save_uploaded_file(image, CERTS_DIR))
            st.success(f"Saved {len(saved_paths)} certificate image(s).")
            st.session_state.cert_upload = None
        else:
            st.warning("Please choose certificates to save first.")

    # PDFs uploader (resume, letters, etc.)
    st.write("Upload PDF certificates or documents (resume, LOR)")
    pdf_file = st.file_uploader(
        "Upload a PDF",
        type=["pdf"],
        accept_multiple_files=False,
        key="pdf_upload",
    )
    if st.button("Save PDF"):
        if pdf_file:
            saved_path = save_uploaded_file(pdf_file, PDFS_DIR)
            st.success("Saved PDF.")
            st.session_state.pdf_upload = None
        else:
            st.warning("Please choose a PDF to save first.")

    # Also show any saved certificates/images
    display_gallery(CERTS_DIR, "Saved Certificates", cols=4, thumb_width=200, caption_prefix="Saved certificate")
    display_pdfs(PDFS_DIR, "Saved Documents (PDFs)")
    st.write("If you prefer, add picture files in your repository and replace the uploader with `st.image('path/to/your-certificate.png')`.")

elif page == "School":
    st.title("School life")
    st.write("I Learnt alot in computing ,and the best part about it is going to competitions going to competitions allowed me to learn many new skills and meet alot of new people it boosted my compet[...]
    st.subheader("Cca")
    st.write("I have also learnt a lot from my robotics CCA and made a lot of friends and met a lot of different people in the competitions I have went for. I have went for at least two competitions f[...]
    st.subheader("Awards")
    st.write("i have also went for competitions to represent my school and placed for cross country.")

    display_gallery(SCHOOL_DIR, "Saved School Images", cols=3, thumb_width=200, caption_prefix="Saved school image")

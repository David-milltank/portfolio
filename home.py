import streamlit as st
import os
import uuid

st.set_page_config(page_title="Portfolio", layout="wide")


IMAGES_ROOT = "images"
ABOUT_DIR = os.path.join(IMAGES_ROOT, "about")
CERTS_DIR = os.path.join(IMAGES_ROOT, "certs")
PDFS_DIR = os.path.join(IMAGES_ROOT, "pdfs")
HOME_DIR = os.path.join(IMAGES_ROOT, "home")
os.makedirs(ABOUT_DIR, exist_ok=True)
os.makedirs(CERTS_DIR, exist_ok=True)
os.makedirs(PDFS_DIR, exist_ok=True)
os.makedirs(HOME_DIR, exist_ok=True)
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


def delete_files(paths):
    deleted = []
    for p in paths:
        try:
            if os.path.exists(p):
                os.remove(p)
                deleted.append(p)
        except Exception as e:
            st.error(f"Failed to delete {p}: {e}")
    return deleted


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

    # Home uploads
    st.subheader("Upload general image")
    uploaded_home_img = st.file_uploader("Choose an image to upload for Home", type=['png','jpg','jpeg','gif'], key='home_img_uploader')
    if uploaded_home_img is not None:
        saved_home = save_uploaded_file(uploaded_home_img, HOME_DIR)
        st.success(f"Saved home image to {saved_home}")
        st.image(saved_home, width=200)
        st.rerun()

    st.subheader("Upload general PDF")
    uploaded_home_pdf = st.file_uploader("Choose a PDF to upload for Home (resume/LOR)", type=['pdf'], key='home_pdf_uploader')
    if uploaded_home_pdf is not None:
        saved_home_pdf = save_uploaded_file(uploaded_home_pdf, PDFS_DIR)
        st.success(f"Saved PDF to {saved_home_pdf}")
        st.write("The PDF is available in the Saved Documents section.")
        st.rerun()

    # Manage/Delete Home images and show gallery
    st.subheader("Manage Home Images")
    home_files = list_saved_images(HOME_DIR)
    if home_files:
        to_delete_home = st.multiselect("Select home images to delete", options=home_files, format_func=lambda x: os.path.basename(x), key='home_del_select')
        if st.button("Delete selected home images", key='delete_home_btn'):
            deleted = delete_files(to_delete_home)
            if deleted:
                st.success(f"Deleted {len(deleted)} home image(s)")
                st.rerun()
            else:
                st.info("No home images were deleted.")
    else:
        st.write("No saved home images")

    display_gallery(HOME_DIR, "Saved Home Images", cols=3, thumb_width=200, caption_prefix="Home image")
   
elif page == "About Me":
    st.title("About Me")
    
    display_gallery(ABOUT_DIR, "Saved About / Profile Images", cols=3, thumb_width=200, caption_prefix="Saved image")

    # Image uploader for About/Profile
    st.subheader("Upload a profile/about image")
    uploaded_about = st.file_uploader("Choose an image to upload for About/Profile", type=['png','jpg','jpeg','gif'], key='about_uploader')
    if uploaded_about is not None:
        saved_path = save_uploaded_file(uploaded_about, ABOUT_DIR)
        st.success(f"Saved image to {saved_path}")
        st.image(saved_path, width=200)
        st.rerun()

    # Manage/Delete About images
    st.subheader("Manage About Images")
    about_files = list_saved_images(ABOUT_DIR)
    if about_files:
        to_delete = st.multiselect("Select About images to delete", options=about_files, format_func=lambda x: os.path.basename(x), key='about_del_select')
        if st.button("Delete selected About images", key='delete_about_btn'):
            deleted = delete_files(to_delete)
            if deleted:
                st.success(f"Deleted {len(deleted)} file(s)")
                st.rerun()
            else:
                st.info("No files were deleted.")
    else:
        st.write("No saved About images")

    st.write(" Hi,I'm dave.")
    st.write("I am the vice president of robotics in my school, and I have been programming for 2 years. I am decent in Python, and I was able to join many competitions. I enjoy playing sports in my free time.")
    
    st.header("My Passion")
    st.write("My passion for coding started when my mother signed me up for a coding class when I was still a kid. It was a class for building LEGO robots and coding them to do different tasks. I got interested and kept learning.")

elif page == "Certifications":
    st.title("Certifications")
   

    display_gallery(CERTS_DIR, "Saved Certificates", cols=4, thumb_width=200, caption_prefix="Saved certificate")
    display_pdfs(PDFS_DIR, "Saved Documents (PDFs)")
   
    # Certificate image uploader
    st.subheader("Upload a certificate (image)")
    uploaded_cert = st.file_uploader("Choose a certificate image to upload", type=['png','jpg','jpeg','gif'], key='cert_uploader')
    if uploaded_cert is not None:
        saved_cert = save_uploaded_file(uploaded_cert, CERTS_DIR)
        st.success(f"Saved certificate image to {saved_cert}")
        st.image(saved_cert, width=200)
        st.rerun()

    # PDF uploader (resume, letters, etc.)
    st.subheader("Upload a PDF document (resume, LOR, etc.)")
    uploaded_pdf = st.file_uploader("Choose a PDF to upload", type=['pdf'], key='pdf_uploader')
    if uploaded_pdf is not None:
        saved_pdf = save_uploaded_file(uploaded_pdf, PDFS_DIR)
        st.success(f"Saved PDF to {saved_pdf}")
        st.write("The PDF is available in the Saved Documents section.")
        st.rerun()
   
    # Manage/Delete certificate images and PDFs
    st.subheader("Manage Certificates & Documents")
    cert_files = list_saved_images(CERTS_DIR)
    pdf_files = list_saved_pdfs(PDFS_DIR)
    if cert_files:
        to_delete_certs = st.multiselect("Select certificate images to delete", options=cert_files, format_func=lambda x: os.path.basename(x), key='cert_del_select')
        if st.button("Delete selected certificate images", key='delete_cert_btn'):
            deleted = delete_files(to_delete_certs)
            if deleted:
                st.success(f"Deleted {len(deleted)} certificate image(s)")
                st.rerun()
            else:
                st.info("No certificate images were deleted.")
    else:
        st.write("No saved certificate images")

    if pdf_files:
        to_delete_pdfs = st.multiselect("Select PDFs to delete", options=pdf_files, format_func=lambda x: os.path.basename(x), key='pdf_del_select')
        if st.button("Delete selected PDFs", key='delete_pdf_btn'):
            deleted = delete_files(to_delete_pdfs)
            if deleted:
                st.success(f"Deleted {len(deleted)} PDF(s)")
                st.rerun()
            else:
                st.info("No PDFs were deleted.")
    else:
        st.write("No saved PDFs")
   
    # Also show any saved certificates/images    



elif page == "School":
    st.title("School life")
    st.write("I learnt a lot in Computing, and the best part about it is going to competitions. Going to competitions allowed me to learn many new skills and meet a lot of new people. It boosted my confidence.")
    st.subheader("Cca")
    st.write("I have also learnt a lot from my robotics CCA and made a lot of friends and met a lot of different people in the competitions I have went for. I have went for at least two competitions for my school.")
    st.subheader("Awards")
    st.write("i have also went for competitions to represent my school and placed for cross country.")

    # School images uploader
    st.subheader("Upload school images")
    uploaded_school = st.file_uploader("Choose a school image to upload", type=['png','jpg','jpeg','gif'], key='school_uploader')
    if uploaded_school is not None:
        saved_school = save_uploaded_file(uploaded_school, SCHOOL_DIR)
        st.success(f"Saved school image to {saved_school}")
        st.image(saved_school, width=200)
        st.rerun()

    # Manage/Delete school images
    st.subheader("Manage School Images")
    school_files = list_saved_images(SCHOOL_DIR)
    if school_files:
        to_delete_school = st.multiselect("Select school images to delete", options=school_files, format_func=lambda x: os.path.basename(x), key='school_del_select')
        if st.button("Delete selected school images", key='delete_school_btn'):
            deleted = delete_files(to_delete_school)
            if deleted:
                st.success(f"Deleted {len(deleted)} school image(s)")
                st.rerun()
            else:
                st.info("No school images were deleted.")
    else:
        st.write("No saved school images")

    display_gallery(SCHOOL_DIR, "Saved School Images", cols=3, thumb_width=200, caption_prefix="Saved school image")

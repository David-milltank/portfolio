import streamlit as st
import os
import uuid

st.set_page_config(page_title="Portfolio", layout="wide")


IMAGES_ROOT = "images"
ABOUT_DIR = os.path.join(IMAGES_ROOT, "about")
CERTS_DIR = os.path.join(IMAGES_ROOT, "certs")
os.makedirs(ABOUT_DIR, exist_ok=True)
os.makedirs(CERTS_DIR, exist_ok=True)
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


def display_gallery(folder, title, cols=3, thumb_width=300, caption_prefix="Saved image"):
    saved = list_saved_images(folder)
    if saved:
        st.subheader(title)
        n = min(cols, len(saved))
        cols_elems = st.columns(n)
        for idx, path in enumerate(saved):
            cols_elems[idx % n].image(path, caption=f"{caption_prefix} {idx+1}", width=thumb_width)


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
    st.write("Letter of recemandation")
    st.write(file:///C:/Users/davey/OneDrive/Desktop/balls/LOR%202026%20Dave.pdf)
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
    
    st.write("---")
    
   
elif page == "About Me":
    st.title("About Me")
    about_images = st.file_uploader(
        "Upload profile photos or About Me images",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="about_upload",
    )
    if st.button("Save About Images"):
        if about_images:
            saved_paths = []
            for image in about_images:
                saved_paths.append(save_uploaded_file(image, ABOUT_DIR))
            st.success(f"Saved {len(saved_paths)} image(s).")
            st.session_state.about_upload = None
        else:
            st.warning("Please choose images to save first.")
    
    display_gallery(ABOUT_DIR, "Saved About / Profile Images", cols=3, thumb_width=200, caption_prefix="Saved image")
    st.write(" Hi,I'm dave.")
    st.write(
        "I am the vice president of robotics in my school, and I have been programming for 2 years. I am decent in Python, i was able to join many competitions. I enjoy playing sports in my free time mainly basketball and bowling. I am passionate on imoroving my coding skills and intereting with others to create new things like robots or new code to help others."
    )
    
    st.header("My Passion")
    st.write(
        "My passion for coding started when my mother signed me up for a coding class when i was still a kid it was a class for building lego robots and coding them to do diffrent tasks i got hooked imeadiatly but was unable to continue since my family moved to  a new hosue and i was unable to attend it.When i joined serengoon garden secoundary school i was able to join the robotics club and i was able to continue my coding journey and i learnt so much from it i was able to join many competitions and though i didnt win them i gained valuable experiences and was able to get the role of roboticsvice president.When i heard that my school was offering o-levle computing i took it immeaditely though i was not good at it at first i was able to learn and with help from my teachers and friends i was able to grow even more."
    )
    

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
    # Also show any saved certificates/images
    display_gallery(CERTS_DIR, "Saved Certificates", cols=4, thumb_width=200, caption_prefix="Saved certificate")
    st.write("If you prefer, add picture files in your repository and replace the uploader with `st.image('path/to/your-certificate.png')`.")

elif page == "School":
    st.title("School life")
    st.write("I Learnt alot in computing python networking ect,but the best part is going to competitions i have went for three competitions for computing One was a hackaton for nanyang poly, there was one for TP and vjjv hackaton i went for both as well as ycep for nanyang poly i have gotten all the certs for all three of them they are incrediably fun since i laern new things and improve my coding skills.")
    st.subheader("Cca")
    st.write("I have also learnt alot from my robotics cca and made alot of friends and met alot of diffrent people in the competitions i have went for i have went for at least two comepetitions for robotics and i have learnt alot from it, i was also given a great opportunity to talk to DR janil he came to our school and i was able to represent my ccawith my friends and impressed him with our robot.")
    st.subheader("Awards")
    st.write("i have also went for competitions to represent my school and placed for cross country.")

    # School images uploader (separate folder from About and Certs)
    school_images = st.file_uploader(
        "Upload School images (events, projects, awards)",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="school_upload",
    )
    if st.button("Save School Images"):
        if school_images:
            saved_paths = []
            for image in school_images:
                saved_paths.append(save_uploaded_file(image, SCHOOL_DIR))
            st.success(f"Saved {len(saved_paths)} school image(s).")
            st.session_state.school_upload = None
        else:
            st.warning("Please choose images to save first.")

    display_gallery(SCHOOL_DIR, "Saved School Images", cols=3, thumb_width=200, caption_prefix="Saved school image")





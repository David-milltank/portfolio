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
    st.write("I am the vice president of robotics in my school, and I have been programming for 2 years. I am decent in Python, and I was able to join many competitions. I enjoy playing sports in my free time, mainly basketball and bowling. I am passionate about improving my coding skills and interacting with others to create new things like robots or new code to help others.")
    
    st.header("My Passion")
    st.write("My passion for coding started when my mother signed me up for a coding class when I was still a kid. It was a class for building LEGO robots and coding them to do different tasks. I got hooked immediately but was unable to continue since my family moved to a new house and I was unable to attend it. When I joined Serangoon Garden Secondary School, I was able to join the robotics club and I was able to continue my coding journey and I learnt so much from it. I was able to join many competitions and though I didn't win them, I gained valuable experiences and was able to get the role of robotics vice president. When I heard that my school was offering O-Level Computing, I took it immediately. Though I was not good at it at first, I was able to learn and with help from my teachers and friends I was able to grow even more.")
elif page == "Certifications":
    st.title("Certifications")
   

    # PDFs uploader (resume, letters, etc.)
   
    # Also show any saved certificates/images    


    display_gallery(CERTS_DIR, "Saved Certificates", cols=4, thumb_width=200, caption_prefix="Saved certificate")
    display_pdfs(PDFS_DIR, "Saved Documents (PDFs)")
    st.write("If you prefer, add picture files in your repository and replace the uploader with `st.image('path/to/your-certificate.png')`.")

elif page == "School":
    st.title("School life")
    st.write("I learnt a lot in Computing, and the best part about it is going to competitions. Going to competitions allowed me to learn many new skills and meet a lot of new people. It boosted my competitive spirit as well. I enjoyed my time in SGSS as I have made many friends and made countless memories from all the events that my school has held, like camp, workshops and inter-class games, which allowed me to build stronger bonds with my classmates.")
    st.subheader("Cca")
    st.write("I have also learnt a lot from my robotics CCA and made a lot of friends and met a lot of different people in the competitions I have went for. I have went for at least two competitions for robotics and I have learnt a lot from it. I was also given a great opportunity to talk to Dr. Janil. He came to our school and I was able to represent my CCA with my friends and impressed him with our robot.")
    st.subheader("Awards")
    st.write("i have also went for competitions to represent my school and placed for cross country.")

    display_gallery(SCHOOL_DIR, "Saved School Images", cols=3, thumb_width=200, caption_prefix="Saved school image")

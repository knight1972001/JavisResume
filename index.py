import time
import requests
import streamlit as st
from streamlit_lottie import st_lottie
from streamlit_extras.stateful_button import button
from streamlit_extras.customize_running import center_running
from streamlit_extras.streaming_write import write
import actionDB
import action

st.set_page_config(page_title= "Jarvis Job Advisor", layout="wide", menu_items={"About": "#contact"})
response = ""

def stateful_button(*args, key=None, **kwargs):
    if key is None:
        raise ValueError("Must pass key")

    if key not in st.session_state:
        st.session_state[key] = False

    if st.button(*args, **kwargs):
        st.session_state[key] = not st.session_state[key]

    return st.session_state[key]

def streaming_write(data):
        for word in data.split():
            yield word + " "
            time.sleep(0.1)
        

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Use local CSS
def local_css(filename):
    with open(filename) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def clear_response():
    global response
    response = "Waiting..."

local_css("style/style.css")

# load assets
lottie_coding = load_lottieurl("https://lottie.host/3f609a3d-1f8e-4119-abfe-1d55db24a1bf/lEuhW50jrQ.json")

# response = actionDB.get_resume_by_name("Long_TEST-13-12-2023-16-13-06")
# HTML OUTPUT

# Header
with st.container():
    # st.subheader("Hi, I'm Jarvis, your job coordinator <span class="wave">🖐")
    st.markdown("""
    ## Hi, I'm Jarvis, your job coordinator <span class="wave">🖐</span> 
""", unsafe_allow_html=True)
    st.title("Jarvis analyze")
    write("Struggling to stand out in the job market? Tired of sending out the same, generic resume and cover letter to countless employers? Say hello to Jarvis, your personal career assistant that crafts tailor-made resumes and cover letters, optimized for the job you're eyeing.")
    write("---")
    left_column, right_column = st.columns(2)
    
    with left_column:
        st.write(
        """
        ## ***🌟 Why Choose Jarvis? 🌟***
        
        1️⃣ **Personalized Content:** Input your job description and watch as our AI crafts a resume and cover letter that speaks directly to what employers are looking for.

        2️⃣ **Time-Saving:** Forget spending hours formatting and revising. Get a polished, professional package in minutes.

        3️⃣ **Keyword Optimization:** Our advanced algorithms scan job descriptions to include the right buzzwords and skills, increasing your chances of passing through Applicant Tracking Systems (ATS).

        4️⃣ **Industry-Specific Templates:** Whether you're in tech, healthcare, or the arts, we've got you covered with templates designed to highlight your skills in the best way possible.

        5️⃣ **Unlimited Revisions:** Not quite satisfied? Make unlimited edits until you're confident with your application.

        6️⃣ **Expert Advice:** Get tips and recommendations for improving your job search strategy, all built into the platform.
        """
    )
        
    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")
    
    st.write("---")
    
    # st.write("[Contact:](https://google.com/search)")
    
# # Initialize session state
# if 'show_form' not in st.session_state:
#     st.session_state.show_form = False

# with st.container():
#     button1 = st.button("Show Form 1")
    
#     if button1:
#         st.session_state.show_form = not st.session_state.show_form

#     if st.session_state.show_form:
#         with st.form(key='form9'):
#             st.write("***Add new resume***")
#             user_name = st.text_input("Your name: ")
#             user_input = st.text_area("Your resume: ", value="", height=600, max_chars=None)
#             submit_button = st.form_submit_button("Submit Resume")

#             if submit_button:
#                 st.write(f"Submitted Form 1 with {user_input} for user {user_name}")
#                 response = "This is the API response."
#                 st.session_state.show_form = False  # Reset the form visibility if needed
#             else:
#                 st.write(f"Not Submitted Form 1 with {user_input} for user {user_name}")


# Initialize session state
if 'show_form' not in st.session_state:
    st.session_state.show_form = None
    
if 'to_delete' not in st.session_state:
    st.session_state.to_delete = None
    
# Create a container for the buttons
with st.container():
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

    with col1:
        button1 = st.button("Add new profile resume")
    with col2:
        button2 = st.button("Write cover letter")
    with col3:
        button3 = st.button("Suggestion for editing resume")
    with col4:
        button4 = st.button("Answer question using profile resume")
    with col5: 
        button5 = st.button("Delete profile resume")

    if button1:
        st.session_state.show_form = 'form1'
    elif button2:
        st.session_state.show_form = 'form2'
    elif button3:
        st.session_state.show_form = 'form3'
    elif button4:
        st.session_state.show_form = 'form4'
    elif button5:
        st.session_state.show_form = 'form5'

# Create containers for each form
with st.container():
    if st.session_state.show_form == 'form1':
        clear_response()
        with st.form(key='form1'):
            st.write("***Add new resume***")
            user_name = st.text_input("Your name: ")
            user_resume = st.text_area("Your resume: ", value="", height=600, max_chars=None)
            submit_button = st.form_submit_button("Submit Resume")

            if submit_button:
                st.session_state.show_form = 'form1'  # Reset the form visibility if needed
                center_running()
                # action.create_profile(user_name, user_resume)
                if(actionDB.create_profile(user_name, user_resume)):
                    print("submited form 1")
                    response = f"Created profile for user {user_name} profile"
                else:
                    response = f"Fail to create {user_name} profile, Please wait a minute before trying again"

    elif st.session_state.show_form == 'form2':
        clear_response()
        with st.form(key='form2'):
            st.write("***Write cover letter***")
            
            # names = action.get_profiles_name()
            names = actionDB.get_profiles_name()
            
            name = st.selectbox("Select user resume: ", names)
            job_description = st.text_area("Job Description: ", value="", height=300, max_chars=None)
            addition_request = st.text_input("Addition request:")
            submit_button = st.form_submit_button("Submit Form 2")

            if submit_button:
                st.write(f"Submitted Job Description and Resume")
                center_running()
                response = action.write_cover_letter(name, job_description, addition_request)
                st.session_state.show_form = 'form2'  # Reset the form visibility if needed

    elif st.session_state.show_form == 'form3':
        clear_response()
        with st.form(key='form3'):
            st.write("***This is Form 3***")
            
            user_resume = st.text_area("Your resume: ", value="", height=600, max_chars=None)
            submit_button = st.form_submit_button("Submit Resume")

            if submit_button:
                st.write(f"Submitted Resume")
                center_running()
                response = action.suggest_resume(user_resume)
                st.session_state.show_form = 'form3'  # Reset the form visibility if needed
                    
    elif st.session_state.show_form == 'form4':
        clear_response()
        with st.form(key='form4'):
            st.write("Enter your question")
            
            names = actionDB.get_profiles_name()
            
            name = st.selectbox("Select user resume: ", names)
            job_description = st.text_area("Question: ", value="", height=300, max_chars=None)
            addition_request = st.text_input("Addition request:")
            submit_button = st.form_submit_button("Submit Form 4")

            if submit_button:
                st.write(f"Submitted Question and Resume")
                center_running()
                response = action.answer_question_base_on_resume(name, job_description, addition_request)
                st.session_state.show_form = 'form4'  # Reset the form visibility if needed
                
    elif st.session_state.show_form == 'form5':
        response = "Deleting process"
        profiles = actionDB.get_profiles_name()
        
        # Show list of profiles
        st.write("### List of Profiles")
        click = False
        # Initialize session state if not already done
        if 'to_delete' not in st.session_state:
            st.session_state.to_delete = None

        for i, name in enumerate(profiles):
            col1, col2 = st.columns([3, 1])  # Adjust the numbers for your specific layout needs

            with col1:
                st.write(f"{i+1}. {name}")

            with col2:
                if st.button("❌", key=f"Delete-{name}") :
                    st.session_state.to_delete = name
                    st.warning("You cannot recover this profile in the future")
                    if(actionDB.delete_profile_by_name(name)):
                        response = f'Deleted {name} profile'
                    else:
                        response = f'Failed when delete {name} profile'
                    center_running()
                    time.sleep(2)
                    st.experimental_rerun()
                    
with st.container():
    st.write("### Response:")
    st.code(f"{response}", language="json")
st.write("---")
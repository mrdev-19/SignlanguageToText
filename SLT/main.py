import streamlit as st
from streamlit_option_menu import option_menu
import database as db
import validations as val
import time
import send_mail as sm
import hasher as hs
import cv2
#---------------------------------------------------
# page config settings:

page_title="Sign Language"
page_icon=""
layout="centered"

st.set_page_config(page_title=page_title,page_icon=page_icon,layout=layout)
st.title(page_title+" "+page_icon)

#--------------------------------------------------
#hide the header and footer     

hide_ele="""
        <style>
        #Mainmenu {visibility:hidden;}
        footer {visibility:hidden;}
        header {visibility:hidden;}
        </style>
        """
st.markdown(hide_ele,unsafe_allow_html=True)
#---------------------------------------------------
curlogin=""
otp=""

def log_sign():
    selected=option_menu(
        menu_title=None,
        options=["Login","Signup","Admin"],
        icons=["bi bi-fingerprint","bi bi-pencil-square","bi bi-people"],
        orientation="horizontal"
    )
    global submit
    if(selected=="Login"):
        tab1,tab2=st.tabs(["Login","Forgot Password"])
        with tab1:
            with st.form("Login",clear_on_submit=True):
                st.header("Login")
                username=st.text_input("Email")
                password=st.text_input("Password",type="password")
                submit=st.form_submit_button()
                if(submit):
                    if(username=="" or password==""):
                        st.warning("Enter your login credentials")
                    else:
                        password=hs.hasher(password)
                        if(db.authenticate(username,password)):
                            st.session_state["curlogin"]=username
                            st.session_state["key"]="main"
                            st.experimental_rerun()
                        else:
                            st.error("Please check your username / password ")
        with tab2:
            with st.form("Forgot Password",clear_on_submit=True):
                st.header("Forgot Password")
                email=st.text_input("Email")
                submit=st.form_submit_button()
                if(submit):
                    if(email==""):
                        st.warning("Enter your email")
                    elif(not db.emailexists(email)):
                        st.warning("User with associated email is not found,kindly recheck the email!")
                    else:
                        otp=sm.forgot_password(email)
                        db.forgot_pass(email,otp)
                        st.success("Check your email for password reset instructions!.")
                
    elif(selected=="Signup"):
         with st.form("Sign Up",clear_on_submit=False):
            st.header("Sign Up")
            email=st.text_input("Enter your email")
            number=st.text_input("Enter your Mobile Number")
            password=st.text_input("Enter your password",type="password")
            submit=st.form_submit_button()
            if(submit):
                dev=db.fetch_all_users()
                emails=[]
                numbers=[]
                for user in dev:
                    emails.append(user["email"])
                    numbers.append(user["number"])
                var=True
                if(val.validate_email(email)==False):
                    st.error("Enter email in a valid format like 'yourname@srmap.edu.in'")
                elif(email in emails):
                    st.error("email already exists!\nTry with another email !")
                elif(val.validate_mobile(number)==False):
                    st.error("Please Check your mobile Number")
                elif(number in numbers):
                    st.error("Phone number already exists\nTry with another number")
                elif(val.validate_password(password)==False):
                    st.error("Password must be between 6-20 characters in length and must have at least one Uppercase Letter , Lowercase letter , numeric character and A Special Symbol(#,@,$,%,^,&,+,=)")
                elif(var):
                    password=hs.hasher(password)
                    db.insert_user(email,password,number)
                    st.success("Signed Up Successfully....Redirecting!!")
                    time.sleep(2)
                    st.session_state["curlogin"]=email
                    st.session_state["key"]="main"
                    st.experimental_rerun()
    
    elif selected=="Admin":
        with st.form("Admin Login",clear_on_submit=True):
            st.header("Admin Login")
            username=st.text_input("Username")
            password=st.text_input("Password",type="password")
            submit=st.form_submit_button()
            if(submit):
                if(username=="" or password==""):
                    st.warning("Enter your login credentials")
                else:
                    password=hs.hasher(password)
                    if(db.ad_authenticate(username,password)):
                        st.session_state["curlogin"]=username
                        st.session_state["key"]="adminmain"
                        st.experimental_rerun()
                    else:
                        st.error("Please check your username / password ")
def main():
    opt=option_menu(
        menu_title=None,
        options=["Live Video Input","File Upload"],
        # icons=["bi bi-fingerprint","bi bi-pencil-square","bi bi-people"],
        orientation="horizontal"
    )    
    if(opt=="Live Video Input"):
        run = st.checkbox('Run')
        FRAME_WINDOW = st.image([])
        camera = cv2.VideoCapture(0)

        while run:
            _, frame = camera.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(frame)
            
        else:
            st.write('Stopped')
    else:
        uploaded_file = st.file_uploader("Choose a file")   
        

def admin():
    print("Nth")

if "key" not in st.session_state:
    st.session_state["key"] = "log_sign"

if st.session_state["key"] == "log_sign":
    log_sign()

elif st.session_state["key"] == "adminmain":
    admin()

elif st.session_state["key"] == "main":
    main()

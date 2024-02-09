import pyrebase
from datetime import datetime
from click import style
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
import pickle
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris


# Configuration Key
#firebaseConfig = {
 #   'apiKey': " ",
  #  'authDomain': " ",
   # 'projectId': " ",
    #'databaseURL': " ",
    #'#storageBucket': " ",
    #'m#essagingSenderId': "",
    #'appId': " ",
    #'measurementId': " "
#}
st.set_page_config(page_title="Welcome To ChecknChatt-APP", page_icon=":tada:", layout='wide')

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def local_css(file_name):
    with open(file_name) as f:
      st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html= True)  
local_css("style.css")

html_temp = """
        <div style = "background-color:none;padding:5px;border-radius:30px;width :auto;">
        <h1 style = "color:white;text-align:center;font-size:20px;">检测并聊 </h1>
        </div>
        """
#royalblue
components.html(html_temp)

A,B = st.columns(2)
with A:
    st.write("Test your self and share your experience with others here!")
    st.success("Test yourself with ChecknChat🆗")
    st.warning("Test and Discover yourself with 检测并聊。🧑‍⚕")
     
    
    with B:
        lottie_coding = load_lottieurl("https://assets7.lottiefiles.com/private_files/lf30_6qyxpnwe.json")
        st_lottie(lottie_coding,height= 80,key = "care")


firebaseConfig = {
  'apiKey': "AIzaSyDL-z_llLXnvQcbLWwtJhsVuoyz-MB6uAg",
  'authDomain': "check-and-chat-app-937c8.firebaseapp.com",
  'projectId': "check-and-chat-app-937c8",
  'databaseURL':"https://check-and-chat-app-937c8-default-rtdb.asia-southeast1.firebasedatabase.app/",
  'storageBucket': "check-and-chat-app-937c8.appspot.com",
  'messagingSenderId': "1079184812710",
  'appId': "1:1079184812710:web:899c25dac937b11267e267",
  'measurementId': "G-KX3WJJLF79"
}

#firebaseConfig = {
 # 'apiKey': "AIzaSyD8HUrdIhoZoBuHjs36oQsqzexAb_N5jMs",
  #'authDomain': "all-in-one-detection-app.firebaseapp.com",
  #'projectId': "all-in-one-detection-app",
  #'databaseURL':"https://all-in-one-detection-app-default-rtdb.europe-west1.firebasedatabase.app/",
  #'storageBucket': "all-in-one-detection-app.appspot.com",
  #'messagingSenderId': "643426977084",
  #'appId': "1:643426977084:web:8349da1abceb4c837f8a39",
  #'measurementId': "G-VL0MLCR1YH"
#}

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Database
db = firebase.database()
storage = firebase.storage()
with st.sidebar:
 lottie_coding = load_lottieurl("https://assets7.lottiefiles.com/private_files/lf30_6qyxpnwe.json")
 st_lottie(lottie_coding,height= 80,key = "caring")


st.sidebar.title("检测并聊")
#ChecknChat-App
#st.title("多动能一体检测用程序/All In One  Detection App")
  
# Authentication
choice = st.sidebar.selectbox('登录:login|注册:Signup', ['Login', 'Sign up'])
#choice = st.selectbox('登录:login/注册:Signup', ['Login', 'Sign up'])

   
# Obtain User Input for email and password
email = st.sidebar.text_input('输入邮件📩')
password = st.sidebar.text_input('输入密码🔐', type='password')
#email = st.text_input('输入邮件/Please enter your email address')
#password = st.text_input('输入密码/Please enter your password', type='password')



# Sign up Block
if choice == 'Sign up':
    handle = st.sidebar.text_input(
    'Enter name', value='Default')
    submit = st.sidebar.button('注册🧾')
   # handle = st.text_input(
    #'Please input your app handle name', value='Default')
    #submit = st.button('注册/Create my account')


    if submit:
        user = auth.create_user_with_email_and_password(email, password)
        st.success('注册成功:Your account is created suceesfully!📩')
        st.balloons()
        # Sign in
        user = auth.sign_in_with_email_and_password(email, password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.title('Welcome' + handle)
        st.info('通过登录下拉列表和选择登录:Login via login drop down selection🔑')

# Login Block
if choice == 'Login':
  login = st.sidebar.checkbox('登录:Login')
    
    #login = st.checkbox('登录/Login')

  if login:
    user = auth.sign_in_with_email_and_password(email, password)
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    st.sidebar.success('您已成功登录，请关闭此侧栏。')



    st.write("---")
    bio = st.radio('Explore Now:', 
     ['主页🏛️',
     '用户配置文件图片👨',
     '找朋友👨🏿‍🤝‍👨🏾',
     '设置⚙️',
     '联系我们🤝','自检🩺'])
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    if bio=="主页🏛️":
      st.write("---")
      st.write("Example")
      st.write("Before jumping to self test page ,first you can study on how to do it using information given below:")
      st.write("在这里，它向个人展示了如何根据医生提供的关于心脏糖尿病、帕金森病和心脏病两个阶段的信息来测试自己的算法。")
      df = pd.DataFrame({'Pregnances': [5, 3, 10, 2,8],
                   'Glucose': [116, 78, 115, 197, 125],
                   'Skin Thickness': [0, 32, 0, 45, 0],
                   'Insulin': [0, 88, 0, 543, 0],
                   'DiabetesPedigree': [0.201, 0.248, 0.134, 0.158,0.232],
                   'BMI': [25.6, 31, 35.3, 30.5, 0],
                   'AGE': [30, 26, 29, 67, 50],
                   'Blood Pressure': [74, 50, 0, 70, 96]})
                   
      st.subheader('Diabetes:糖尿病')
      st.dataframe(df)

      df = pd.DataFrame({'Age': [54, 48, 49, 64,58],
                   'Sex': [1, 0, 1, 1, 0],
                   'CP': [0, 2, 1, 3, 3],
                   'trestbps': [140, 130, 130, 110, 150],
                   'chol': [239, 275, 266, 211,283],
                   'fbs': [0, 0, 0, 0, 1],
                   'exang': [0, 0, 0, 1, 0],
                   'oldpeak': [1.2, 0.2, 0.6, 1.8, 1],
                   'slope': [2, 2, 2, 1, 2],
                   'ca': [0, 0, 0,0, 0],
                   'thal': [2, 2, 2, 2, 2],
                   'targert': [1, 1, 1, 1, 1],
                   'thalach': [160, 139, 171, 144, 162]})
                   
      st.subheader('Heart:心脏病')
      st.dataframe(df)

      df = pd.DataFrame({'MDVP:Fo(Hz)': [88.333, 91.904, 136.926, 139.173,152.845],
                   'MDVP:Fhi(Hz)': [112.24, 115.871,159.866, 179.139, 163.305],
                   'MDVP:Flo(Hz)': [84.072, 86.292, 131.276, 76.556, 75.836],
                   'MDVP:Jitter(%)': [0.00505, 0.0054, 0.00293, 0.0039, 0.00294],
                   'MDVP:Jitter(Abs)': [0.00006, 0.00006, 0.00002, 0.00003,0.00002],
                   'MDVP:RAP': [0.00254, 0.00281, 0.00118,0.00165, 0.00121],
                   'MDVP:PPQ': [0.0033, 0.00336, 0.00153, 0.00208, 0.00149],
                   'Jitter:DDP': [0.00763, 0.00844, 0.00355, 0.00496, 0.00364],
                   'MDVP:Shimmer': [0.02143, 0.02752, 0.01259, 0.01642, 0.01828],
                   'MDVP:Shimmer(dB)': [0.197, 0.249, 0.112, 0.154, 0.158],
                   'Shimmer:APQ3': [0.01079, 0.01424, 0.00656, 0.00728, 0.01064],
                   'Shimmer:APQ5': [0.01342, 0.01641, 0.00717, 0.00932, 0.00972],
                   'Shimmer:DDA': [0.03237, 0.04272, 0.01968, 0.02184, 0.03191],
                   'NHR': [0.01166, 0.01141, 0.00581, 0.01041, 0.00609],
                   'NHR': [21.118, 21.414, 25.703, 24.889, 24.922],
                   'status': [1, 1, 1, 1, 1],
                   'RPDE': [0.611137, 0.58339, 0.4606, 0.430166, 0.474791],
                   'DFA': [0.776156, 0.79252, 0.646846, 0.665833, 0.654027],
                   'spread1': [-5.24977, -4.960234, -6.547148, -5.660217, -6.105098],
                   'spread2': [0.391002, 0.363566, 0.152813, 0.254989, 0.203653],
                   'D2': [2.407313, 2.642476,2.041277,2.519422, 2.125618],
                   'PPE': [0.24974, 0.275931, 0.138512, 0.199889, 0.1701],
                   'MDVP:APQ': [0.01892, 0.02214, 0.0114, 0.01797, 0.01246]})
                   
      st.subheader('Parkinsons:帕金森病')
      st.dataframe(df)
		
        # SETTINGS PAGE
    if bio == '设置⚙️':
            # CHECK FOR IMAGE
            nImage = db.child(user['localId']).child("Image").get().val()
            # IMAGE FOUND
            if nImage is not None:
                # We plan to store all our image under the child image
             Image = db.child(user['localId']).child("Image").get()
             for img in Image.each():
                img_choice = img.val()
                    # st.write(img_choice)
                st.image(img_choice)
                exp = st.beta_expander('改变图像:Change Bio and Image')
                # User plan to change profile picture
                with exp:
                      newImgPath = st.text_input('输入图像的完整路径:Enter full path of your profile image')
                      upload_new = st.button('上装:Upload')
                      if upload_new:
                        uid = user['localId']
                        fireb_upload = storage.child(uid).put(newImgPath, user['idToken'])
                        a_imgdata_url = storage.child(uid).get_url(fireb_upload['downloadTokens'])
                        db.child(user['localId']).child("Image").push(a_imgdata_url)
                        st.success('成功:Success!')
                        # IF THERE IS NO IMAGE
                        # 
            else:
                st.info("No profile picture yet")
                newImgPath = st.text_input('输入图像的完整路径:Enter full path of your profile image')
                upload_new = st.button('上装:Upload')
                if upload_new:
                 uid = user['localId']
                    # Stored Initated Bucket in Firebase
                 fireb_upload = storage.child(uid).put(newImgPath, user['idToken'])
                    # Get the url for easy access
                 a_imgdata_url = storage.child(uid).get_url(fireb_upload['downloadTokens'])
                    # Put it in our real time database
                 db.child(user['localId']).child("Image").push(a_imgdata_url)
        # HOME PAGE
    elif bio == '用户配置文件图片👨':
            st.write("---")
            col1, col2 = st.columns(2)

        # col for Profile picture
            with col1:
                nImage = db.child(user['localId']).child("Image").get().val()
                if nImage is not None:
                 val = db.child(user['localId']).child("Image").get()
                 for img in val.each():
                   img_choice = img.val()
                 st.image(img_choice, use_column_width=True)
                else:
                 st.info("还没有个人资料图片:No profile picture yet. Go to settings and upload!")

                post = st.text_input("分享或发布你当前的心情:Share and Post Your Current Mood!", max_chars=150)
                add_post = st.button('Share Posts')
            if add_post:
                      now = datetime.now()
                      dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                      post = {'Post:': post,
                      'Timestamp': dt_string}
                      results = db.child(user['localId']).child("Posts").push(post)
                      st.balloons()

        # This coloumn for the post Display

        ######
            with col2:
              all_posts = db.child(user['localId']).child("Posts").get()

              if all_posts.val() is not None:
               for Posts in reversed(all_posts.each()):
                st.write(Posts.key()) # Morty
                st.code(Posts.val(), language='')

        # WORKPLACE FEED PAGE
    else:

       if bio =="找朋友👨🏿‍🤝‍👨🏾":
                all_users = db.get()
                res = []
            # Store all the users handle name
                for users_handle in all_users.each():
                    k = users_handle.val()["Handle"]
                    res.append(k)
            # Total   users
                nl = len(res)
                st.write('Number Of Users In Use Of The App: ' + str(nl))

            # Allow the user to choose which other user he/she wants to see
                choice = st.selectbox('Friends In Circle', res)
                st.write('You selected out:', choice)
                push = st.button('Show Profile:显示配置文件')


            # Show the chosen Profile
                if push:
                     for users_handle in all_users.each():
                        k = users_handle.val()["Handle"]

                        if k == choice:
                         lid = users_handle.val()["ID"]

                         handlename = db.child(lid).child("Handle").get().val()

                         st.markdown(handlename, unsafe_allow_html=True)

                         nImage = db.child(lid).child("Image").get().val()
                         if nImage is not None:

                          val = db.child(lid).child("Image").get()
                          for img in val.each():
                             img_choice = img.val()
                             st.image(img_choice)
                         else:
                            st.info("还没有个人资料图片:No profile picture yet.Go to settings and upload!")

                        # All posts
                         all_posts = db.child(lid).child("Posts").get()
                         if all_posts.val() is not None:
                            for Posts in reversed(all_posts.each()):
                              st.code(Posts.val(), language='')

        ########
 
    if bio == "联系我们🤝":
        st.write("----")
        col1,col2 = st.columns(2)
            #st.title(f"you have selected{selected}")
        with col1:
            st.markdown(""" <style> .font {
                        font-size:35px ; font-family: 'Cooper Black'; color: blue;} 
                        </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">Get In Touch with 检测并聊 Team:</p>', unsafe_allow_html=True)
            contact_form = """
                     <input type = "hidden" name = " _capture" value = "false">
                     <form action="https://formsubmit.co/chototakudzwa8@gmail.com" method="POST">
                     <input type="text" name="name" placeholder = "Your name" required>
                     <input type="email" name="email" placeholder = "Your email" required>
                     <input type = "text" name = "company" placeholder = "Your company" required >
                     <textarea  name = "message" placeholder = "Enter message" required></textarea>
                     <button type="submit">Send</button>
                </form>

                     """
       
            st.markdown(contact_form, unsafe_allow_html=True)
        with col2:
            lottie_coding = load_lottieurl("https://assets1.lottiefiles.com/private_files/lf30_nsqfzxxx.json")
            st_lottie(lottie_coding,height=80,key = "message")

          
#-----------------------------------------------------------------------------------------------------
    if bio == '自检🩺':
        st.write("---")
    # loading the saved models
        diabetes_model = pickle.load(open(r'diabetes_model.sav','rb'))

        heart_disease_model = pickle.load(open(r'heart_disease_model.sav','rb'))

        parkinsons_model = pickle.load(open(r'parkinsons_model.sav','rb'))

        # sidebar for navigation

        bio = option_menu(menu_title="Self Test" ,options=
          ['Education|教育','Diabetes Prediction|糖尿病检测',
         'Heart Disease Prediction|心脏病检测',
         'Parkinsons Prediction|帕金森病检测'],
         icons=['book','activity', 'heart', 'person'],
         default_index=0,orientation="horizontal")

        styles={
           "container ": {"padding": "0!important", "background-color": "white"},
                           "icon": {"color": "blue", "font-size": "25px"},
                           "nav-link": {
                            "font-size": "25px",
                            "text-align": "left",
                            "margin": "0px",
                             "--hover-color": "blue",

                             },
                             "nav-link-selected": {"background-color": "blue"},
                               }
                            
    # loading the saved models
        diabetes_model = pickle.load(open(r'diabetes_model.sav','rb'))

        heart_disease_model = pickle.load(open(r'heart_disease_model.sav','rb'))

        parkinsons_model = pickle.load(open(r'parkinsons_model.sav','rb'))
                    
# Diabetes Prediction Page
        if (bio == 'Diabetes Prediction|糖尿病检测'):

    # page title
                              st.title('Diabetes Test')

    # getting the input data from the user
                              col1, col2, col3 = st.columns(3)

                              with col1:
                                  Pregnancies = st.text_input('Number of Pregnancies')

                              with col2:
                                  Glucose = st.text_input('Glucose Level')

                              with col3:
                                  BloodPressure = st.text_input('Blood Pressure value')

                              with col1:
                                 SkinThickness = st.text_input('Skin Thickness value')

                              with col2:
                                Insulin = st.text_input('Insulin Level')

                              with col3:
                                 BMI = st.text_input('BMI value')

                              with col1:
                                   DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

                              with col2:
                                    Age = st.text_input('Age of the Person')
    # code for Prediction
                                    diab_diagnosis = ''
    # creating a button for Prediction
                              if st.button('Diabetes Test Result:查结果'):
                                 diab_prediction = diabetes_model.predict(
                                 [[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])

                                 if (diab_prediction[0] == 1):
                                   diab_diagnosis = '这个人受到影响:The person is diabetic'
                                   st.warning(diab_diagnosis)
                                 else:
                                   diab_diagnosis = '这个人没受到影响:The person is not diabetic'
                                   st.success(diab_diagnosis)

# Heart Disease Prediction Page
        if (bio == 'Heart Disease Prediction|心脏病检测'):
    # page title
                                st.title('Heart Test')

                                col1, col2, col3 = st.columns(3)

                                with col1:
                                     age = st.text_input('Age')

                                with col2:
                                     sex = st.text_input('Sex')

                                with col3:
                                     cp = st.text_input('Chest Pain types')

                                with col1:
                                    trestbps = st.text_input('Resting Blood Pressure')

                                with col2:
                                    chol = st.text_input('Serum Cholestoral in mg/dl')

                                with col3:
                                    fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

                                with col1:
                                    restecg = st.text_input('Resting Electrocardiographic results')

                                with col2:
                                    thalach = st.text_input('Maximum Heart Rate achieved')

                                with col3:
                                    exang = st.text_input('Exercise Induced Angina')

                                with col1:
                                    oldpeak = st.text_input('ST depression induced by exercise')

                                with col2:
                                    slope = st.text_input('Slope of the peak exercise ST segment')

                                with col3:
                                    ca = st.text_input('Major vessels colored by flourosopy')

                                with col1:
                                    thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

    # code for Prediction
                                    heart_diagnosis = ''

    # creating a button for Prediction

                                if st.button('Heart Disease Test Result'):
                                    heart_prediction = heart_disease_model.predict(
                                    [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

                                    if (heart_prediction[0] == 1):
                                       heart_diagnosis = '这个人受到影响:The person is having a heart problem'
                                       st.warning(heart_diagnosis)
                                    else:
                                       heart_diagnosis = '这个人没受到影响:The person does not have any heart problem'
                                       st.success(heart_diagnosis)

# Parkinson's Prediction Page
        if (bio == "Parkinsons Prediction|帕金森病检测"):

    # page title
                                st.title("Parkinsons Test")

                                col1, col2, col3, col4, col5 = st.columns(5)

                                with col1:
                                      fo = st.text_input('MDVP:Fo(Hz)')

                                with col2:
                                    fhi = st.text_input('MDVP:Fhi(Hz)')

                                with col3:
                                        flo = st.text_input('MDVP:Flo(Hz)')

                                with col4:
                                   Jitter_percent = st.text_input('MDVP:Jitter(%)')

                                with col5:
                                           Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')

                                with col1:
                                   RAP = st.text_input('MDVP:RAP')

                                with col2:
                                    PPQ = st.text_input('MDVP:PPQ')

                                with col3:
                                   DDP = st.text_input('Jitter:DDP')

                                with col4:
                                    Shimmer = st.text_input('MDVP:Shimmer')

                                with col5:
                                           Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')

                                with col1:
                                         APQ3 = st.text_input('Shimmer:APQ3')

                                with col2:
                                       APQ5 = st.text_input('Shimmer:APQ5')

                                with col3:
                                       APQ = st.text_input('MDVP:APQ')

                                with col4:
                                             DDA = st.text_input('Shimmer:DDA')

                                with col5:
                                        NHR = st.text_input('NHR')

                                with col1:
                                   HNR = st.text_input('HNR')

                                with col2:
                                       RPDE = st.text_input('RPDE')

                                with col3:
                                           DFA = st.text_input('DFA')

                                with col4:
                                  spread1 = st.text_input('spread1')

                                with col5:
                                         spread2 = st.text_input('spread2')

                                with col1:
                                    D2 = st.text_input('D2')

                                with col2:
                                    PPE = st.text_input('PPE')

    # code for Prediction
                                    parkinsons_diagnosis = ''

    # creating a button for Prediction
                                if st.button("Parkinson's Test Result"):
                                     parkinsons_prediction = heart_disease_model.predict(
                                     [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

                                     if (parkinsons_prediction[0] == 1):
                                        heart_diagnosis = '这个人受到影响:The person is having a heart problem'
                                        st.warning(parkinsons_diagnosis)
                                     else:
                                        heart_diagnosis = '这个人没受到影响:The person does not have any heart problem'
                                        st.success(heart_diagnosis)


        if bio =="Education|教育":
            st.write("---")
            st.markdown('##')
            lottie_coding = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_tbjuenb2.json")
            st_lottie(lottie_coding,height= 200,key = "diabetes")
            st.write("""
           
           - KNOW MORE ABOUT DIABETES

           - Key facts
           The number of people with diabetes rose from 108 million in 1980 to 422 million in 2014. Prevalence has been rising more rapidly in low- and middle-income countries than in high-income countries.
           Diabetes is a major cause of blindness, kidney failure, heart attacks, stroke and lower limb amputation.
           Between 2000 and 2019, there was a 3% increase in diabetes mortality rates by age.
           In 2019, diabetes and kidney disease due to diabetes caused an estimated 2 million deaths.
           A healthy diet, regular physical activity, maintaining a normal body weight and avoiding tobacco use are ways to prevent or delay the onset of type 2 diabetes.
           Diabetes can be treated and its consequences avoided or delayed with diet, physical activity, medication and regular screening and treatment for complications.
          - Overview
            Diabetes is a chronic disease that occurs either when the pancreas does not produce enough insulin or when the body cannot effectively use the insulin it produces. Insulin is a hormone that regulates blood glucose. Hyperglycaemia, also called raised blood glucose or raised blood sugar, is a common effect of uncontrolled diabetes and over time leads to serious damage to many of the body's systems, especially the nerves and blood vessels.

            In 2014, 8.5% of adults aged 18 years and older had diabetes. In 2019, diabetes was the direct cause of 1.5 million deaths and 48% of all deaths due to diabetes occurred before the age of 70 years. Another 460 000 kidney disease deaths were caused by diabetes, and raised blood glucose causes around 20% of cardiovascular deaths (1).

            Between 2000 and 2019, there was a 3% increase in age-standardized mortality rates from diabetes. In lower-middle-income countries, the mortality rate due to diabetes increased 13%.

            By contrast, the probability of dying from any one of the four main noncommunicable diseases (cardiovascular diseases, cancer, chronic respiratory diseases or diabetes) between the ages of 30 and 70 decreased by 22% globally between 2000 and 2019. 

            - Type 2 diabetes
           Type 2 diabetes (formerly called non-insulin-dependent, or adult-onset) results from the body’s ineffective use of insulin. More than 95% of people with diabetes have type 2 diabetes. This type of diabetes is largely the result of excess body weight and physical inactivity.

           Symptoms may be similar to those of type 1 diabetes but are often less marked. As a result, the disease may be diagnosed several years after onset, after complications have already arisen.

           Until recently, this type of diabetes was seen only in adults but it is now also occurring increasingly frequently in children.

         - Type 1 diabetes
           Type 1 diabetes (previously known as insulin-dependent, juvenile or childhood-onset) is characterized by deficient insulin production and requires daily administration of insulin. In 2017 there were 9 million people with type 1 diabetes; the majority of them live in high-income countries. Neither its cause nor the means to prevent it are known.

          Symptoms include excessive excretion of urine (polyuria), thirst (polydipsia), constant hunger, weight loss, vision changes, and fatigue. These symptoms may occur suddenly.

          - Gestational diabetes
          Gestational diabetes is hyperglycaemia with blood glucose values above normal but below those diagnostic of diabetes. Gestational diabetes occurs during pregnancy

          Women with gestational diabetes are at an increased risk of complications during pregnancy and at delivery. These women and possibly their children are also at increased risk of type 2 diabetes in the future.

          Gestational diabetes is diagnosed through prenatal screening, rather than through reported symptoms.

          Impaired glucose tolerance and impaired fasting glycaemia
          Impaired glucose tolerance (IGT) and impaired fasting glycaemia (IFG) are intermediate conditions in the transition between normality and diabetes. People with IGT or IFG are at high risk of progressing to type 2 diabetes, although this is not inevitable.

          - Health impact
          Over time, diabetes can damage the heart, blood vessels, eyes, kidneys, and nerves.

          Adults with diabetes have a two- to three-fold increased risk of heart attacks and strokes (2).
          Combined with reduced blood flow, neuropathy (nerve damage) in the feet increases the chance of foot ulcers, infection and eventual need for limb amputation.
          Diabetic retinopathy is an important cause of blindness and occurs as a result of long-term accumulated damage to the small blood vessels in the retina. Close to 1 million people are blind due to diabetes (3).
          Diabetes is among the leading causes of kidney failure (4).
          People with diabetes are more likely to have poor outcomes for several infectious diseases, including COVID-19.

          - Prevention
          Lifestyle measures have been shown to be effective in preventing or delaying the onset of type 2 diabetes. To help prevent type 2 diabetes and its complications, people should:

          achieve and maintain a healthy body weight;
          be physically active – doing at least 30 minutes of regular, moderate-intensity activity on most days. More activity is required for weight control;
          eat a healthy diet, avoiding sugar and saturated fats; and
          avoid tobacco use – smoking increases the risk of diabetes and cardiovascular disease.

          - Diagnosis and treatment
           Early diagnosis can be accomplished through relatively inexpensive testing of blood glucose.

          Treatment of diabetes involves diet and physical activity along with lowering of blood glucose and the levels of other known risk factors that damage blood vessels. Tobacco use cessation is also important to avoid complications.

          Interventions that are both cost-saving and feasible in low- and middle-income countries include:

          blood glucose control, particularly in type 1 diabetes. People with type 1 diabetes require insulin, people with type 2 diabetes can be treated with oral medication, but may also require insulin;
          blood pressure control; and
          foot care (patient self-care by maintaining foot hygiene; wearing appropriate footwear; seeking professional care for ulcer management; and regular examination of feet by health professionals).
          Other cost saving interventions include:

          screening and treatment for retinopathy (which causes blindness);
          blood lipid control (to regulate cholesterol levels);
          screening for early signs of diabetes-related kidney disease and treatment.
          - WHO response
          WHO aims to stimulate and support the adoption of effective measures for the surveillance, prevention and control of diabetes and its complications, particularly in low- and middle-income countries. To this end, WHO:

          provides scientific guidelines for the prevention of major noncommunicable diseases including diabetes;
          develops norms and standards for diabetes diagnosis and care;
          builds awareness on the global epidemic of diabetes, marking World Diabetes Day (14 November); and
          conducts surveillance of diabetes and its risk factors.
          The WHO Global report on diabetes provides an overview of the diabetes burden, interventions available to prevent and manage diabetes, and recommendations for governments, individuals, the civil society and the private sector.

          The WHO module on diagnosis and management of type 2 diabetes brings together guidance on diagnosis, classification and management of type 2 diabetes in one document.

          In April 2021 WHO launched the Global Diabetes Compact, a global initiative aiming for sustained improvements in diabetes prevention and care, with a particular focus on supporting low- and middle-income countries. The Compact is bringing together all stakeholders to work on a shared vision of reducing the risk of diabetes and ensuring that all people who are diagnosed with diabetes have access to equitable, comprehensive, affordable and quality treatment and care.

          In May 2021, the World Health Assembly agreed a Resolution on strengthening prevention and control of diabetes. It recommends action in areas including increasing access to insulin; promoting convergence and harmonization of regulatory requirements for insulin and other medicines and health products for the treatment of diabetes. In May 2022 the World Health Assembly endorsed five global diabetes coverage and treatment targets to be achieved by 2030.

          - References

          1. Global Burden of Disease Collaborative Network. Global Burden of Disease Study 2019. Results. Institute for Health Metrics and Evaluation. 2020 (https://vizhub.healthdata.org/gbd-results/).

          2. Diabetes mellitus, fasting blood glucose concentration, and risk of vascular disease: a collaborative meta-analysis of 102 prospective studies. Emerging Risk Factors Collaboration. Sarwar N, Gao P, Seshasai SR, Gobin R, Kaptoge S, Di Angelantonio et al. Lancet. 2010; 26;375:2215-2222.

          3. Causes of blindness and vision impairment in 2020 and trends over 30 years, and prevalence of avoidable blindness in relation to VISION 2020: the Right to Sight: an analysis for the Global Burden of Disease Study GBD 2019 Blindness and Vision Impairment Collaborators* on behalf of the Vision Loss Expert Group of the Global Burden of Disease Study† Lancet Global Health 2021;9:e141-e160.

          4. 2014 USRDS annual data report: Epidemiology of kidney disease in the United States.
          United States Renal Data System. National Institutes of Health, National Institute of Diabetes and Digestive and Kidney Diseases, Bethesda, MD, 2014:188–210.

          - Related
          Health topic: Diabetes
          Global Diabetes Compact
          Fact sheets
          Healthy diet 29 April 2020
          Cardiovascular diseases (CVDs) 11 June 2021
          Regions
          Africa
          Americas
          Eastern Mediterranean
          Europe
          South-East Asia
          Western Pacific
          Policies
          Cyber security""")

            st.write("---")
            st.markdown("##")
            lottie_coding = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_33asonmr.json")
            st_lottie(lottie_coding,height= 200,key = "parkinson")   
            st.write("""
        
        - KNOW MORE ABOUT PARKINSON DISEASE

        - Parkinson’s Disease: Causes, Symptoms, and Treatments

        Parkinson’s disease is a brain disorder that causes unintended or uncontrollable movements, such as shaking, stiffness, and difficulty with balance and coordination.

        Symptoms usually begin gradually and worsen over time. As the disease progresses, people may have difficulty walking and talking. They may also have mental and behavioral changes, sleep problems, depression, memory difficulties, and fatigue.

        Older woman and her caregiverWhile virtually anyone could be at risk for developing Parkinson’s, some research studies suggest this disease affects more men than women. It’s unclear why, but studies are underway to understand factors that may increase a person’s risk. One clear risk is age: Although most people with Parkinson’s first develop the disease after age 60, about 5% to 10% experience onset before the age of 50. Early-onset forms of Parkinson’s are often, but not always, inherited, and some forms have been linked to specific gene mutations.

        - What causes Parkinson’s disease?
        The most prominent signs and symptoms of Parkinson’s disease occur when nerve cells in the basal ganglia, an area of the brain that controls movement, become impaired and/or die. Normally, these nerve cells, or neurons, produce an important brain chemical known as dopamine. When the neurons die or become impaired, they produce less dopamine, which causes the movement problems associated with the disease. Scientists still do not know what causes the neurons to die.

         a computer generated graphic of the brain with labels pointing to the basal ganglia.

         People with Parkinson’s disease also lose the nerve endings that produce norepinephrine, the main chemical messenger of the sympathetic nervous system, which controls many functions of the body, such as heart rate and blood pressure. The loss of norepinephrine might help explain some of the non-movement features of Parkinson’s, such as fatigue, irregular blood pressure, decreased movement of food through the digestive tract, and sudden drop in blood pressure when a person stands up from a sitting or lying position.

         Many brain cells of people with Parkinson’s disease contain Lewy bodies, unusual clumps of the protein alpha-synuclein. Scientists are trying to better understand the normal and abnormal functions of alpha-synuclein and its relationship to genetic mutations that impact Parkinson’s and Lewy body dementia.

         Some cases of Parkinson’s disease appear to be hereditary, and a few cases can be traced to specific genetic mutations. While genetics is thought to play a role in Parkinson’s, in most cases the disease does not seem to run in families. Many researchers now believe that Parkinson’s results from a combination of genetic and environmental factors, such as exposure to toxins.

         - Symptoms of Parkinson’s disease
         - Parkinson’s has four main symptoms:

         Tremor in hands, arms, legs, jaw, or head
         Muscle stiffness, where muscle remains contracted for a long time
         Slowness of movement
         Impaired balance and coordination, sometimes leading to falls
         Other symptoms may include:

         Depression and other emotional changes
         Difficulty swallowing, chewing, and speaking
         Urinary problems or constipation
         Skin problems
         The symptoms of Parkinson’s and the rate of progression differ among individuals. Early symptoms of this disease are subtle and occur gradually. For example, people may feel mild tremors or have difficulty getting out of a chair. They may notice that they speak too softly, or that their handwriting is slow and looks cramped or small. Friends or family members may be the first to notice changes in someone with early Parkinson’s. They may see that the person’s face lacks expression and animation, or that the person does not move an arm or leg normally.

         People with Parkinson's disease often develop a parkinsonian gait that includes a tendency to lean forward; take small, quick steps; and reduce swinging their arms. They also may have trouble initiating or continuing movement.

         Symptoms often begin on one side of the body or even in one limb on one side of the body. As the disease progresses, it eventually affects both sides. However, the symptoms may still be more severe on one side than on the other.

         Many people with Parkinson’s disease note that prior to experiencing stiffness and tremor, they had sleep problems, constipation, loss of smell, and restless legs. While some of these symptoms may also occur with normal aging, talk with your doctor if these symptoms worsen or begin to interfere with daily living.

         - Changes in cognition and Parkinson’s disease
          Some people with Parkinson’s may experience changes in their cognitive function, including problems with memory, attention, and the ability to plan and accomplish tasks. Stress, depression, and some medications may also contribute to these changes in cognition.

         Over time, as the disease progresses, some people may develop dementia and be diagnosed with Parkinson’s dementia, a type of Lewy body dementia. People with Parkinson’s dementia may have severe memory and thinking problems that affect daily living.

         Talk with your doctor if you or a loved one is diagnosed with Parkinson’s disease and is experiencing problems with thinking or memory.

         - Diagnosis of Parkinson’s disease
          There are currently no blood or laboratory tests to diagnose non-genetic cases of Parkinson’s. Doctors usually diagnose the disease by taking a person’s medical history and performing a neurological examination. If symptoms improve after starting to take medication, it’s another indicator that the person has Parkinson’s.

          A number of disorders can cause symptoms similar to those of Parkinson’s disease. People with Parkinson’s-like symptoms that result from other causes, such as multiple system atrophy and dementia with Lewy bodies, are sometimes said to have parkinsonism. While these disorders initially may be misdiagnosed as Parkinson’s, certain medical tests, as well as response to drug treatment, may help to better evaluate the cause. Many other diseases have similar features but require different treatments, so it is important to get an accurate diagnosis as soon as possible.

         - Treatments for Parkinson’s disease
          Although there is no cure for Parkinson’s disease, medicines, surgical treatment, and other therapies can often relieve some symptoms.

         - Medicines for Parkinson’s disease
          Medicines can help treat the symptoms of Parkinson’s by:

         - Increasing the level of dopamine in the brain
         Having an effect on other brain chemicals, such as neurotransmitters, which transfer information between brain cells
         Helping control non-movement symptoms
         The main therapy for Parkinson’s is levodopa. Nerve cells use levodopa to make dopamine to replenish the brain’s dwindling supply. Usually, people take levodopa along with another medication called carbidopa. Carbidopa prevents or reduces some of the side effects of levodopa therapy — such as nausea, vomiting, low blood pressure, and restlessness — and reduces the amount of levodopa needed to improve symptoms.

         People living with Parkinson’s disease should never stop taking levodopa without telling their doctor. Suddenly stopping the drug may have serious side effects, like being unable to move or having difficulty breathing.

         - The doctor may prescribe other medicines to treat Parkinson’s symptoms, including:

          Dopamine agonists to stimulate the production of dopamine in the brain
          Enzyme inhibitors (e.g., MAO-B inhibitors, COMT inhibitors) to increase the amount of dopamine by slowing down the enzymes that break down dopamine in the brain
          Amantadine to help reduce involuntary movements
          Anticholinergic drugs to reduce tremors and muscle rigidity
          Deep brain stimulation
          For people with Parkinson’s disease who do not respond well to medications, the doctor may recommend deep brain stimulation. During a surgical procedure, a doctor implants electrodes into part of the brain and connects them to a small electrical device implanted in the chest. The device and electrodes painlessly stimulate specific areas in the brain that control movement in a way that may help stop many of the movement-related symptoms of Parkinson’s, such as tremor, slowness of movement, and rigidity.

         - Other therapies
         Other therapies that may help manage Parkinson’s symptoms include:

         Physical, occupational, and speech therapies, which may help with gait and voice disorders, tremors and rigidity, and decline in mental functions
         A healthy diet to support overall wellness
         Exercises to strengthen muscles and improve balance, flexibility, and coordination
         Massage therapy to reduce tension
         Yoga and tai chi to increase stretching and flexibility
          Support for people living with Parkinson’s disease
          While the progression of Parkinson’s is usually slow, eventually a person’s daily routines may be affected. Activities such as working, taking care of a home, and participating in social activities with friends may become challenging. Experiencing these changes can be difficult, but support groups can help people cope. These groups can provide information, advice, and connections to resources for those living with Parkinson’s disease, their families, and caregivers. The organizations listed below can help people find local support groups and other resources in their communities.


           Content reviewed: April 14, 2022
         
         """)
            st.write("---")
            st.markdown("##")
            lottie_coding = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_kU5CYh.json")
            st_lottie(lottie_coding,height= 200,key = "heart")  
            st.write("""
            
            - KWOW MORE ABOUT HEART FAILURE

            - Why creating awareness about Heart Failure is so important
            Heart failure is a serious chronic condition where the heart cannot pump enough blood to support the needs of other organs in the body. The most common causes of heart failure include coronary heart disease, myocardial infarction (heart attack), congenital heart defects, or damaged heart valves. Symptoms include breathlessness, fatigue and swollen limbs. It is estimated that 1 in 5 people are at risk of heart failure and it is the most frequent cause of hospitalisation in people over the age of 65.

           - Read More
            Play Your Part and Protect Yourself and People Living with Heart Failure
            COVID-19 presents the world with an unprecedented public health challenge. Its rapid spread has caused significant alarm and disruption across the globe. Understandably, those living with heart failure are anxious and concerned. 

            Please play your part and follow the public health advice to reduce your chances of being infected or spreading COVID-19:

            Regularly and thoroughly clean your hands with an alcohol-based hand rub or wash them with soap and water. 
            Maintain at least 1 metre (3 feet) distance between yourself and others. 
            Avoid going to crowded places. 
            Wear a fabric face covering if there is widespread community transmission, and especially where physical distancing cannot be maintained. 
           Avoid touching eyes, nose and mouth. 
           Make sure you, and the people around you, follow good respiratory hygiene. 
           Stay home and self-isolate even with minor symptoms such as cough, headache, mild fever, until you recover. Avoiding contact with others will protect them from possible COVID-19 and other viruses.
           If you have a fever, cough and difficulty breathing, seek medical attention.
           Keep up to date on the latest information from trusted sources, such as WHO or your local and national health authorities. 
           - Know The Symptoms of Heart Failure
           Heart failure can affect different people in different ways. Symptoms can come on suddenly and be initially severe (acute heart failure) or they can appear over time and gradually get worse (chronic heart failure). If you have heart failure, you may have one, or a combination, of these symptoms. The more common symptoms of heart disease are:

           Coughing/wheezing
           Extreme tiredness or no energy
           Loss of appetite
           More frequent urination, especially at night
           Rapid heartbeat or palpitations
           Shortness of breath
           Shortness of breath, even when lying down
           Swelling in the ankles/feet/stomach
           Weight gain over a short period of time (>2kg over 2 days)
           By themselves, any one sign of heart failure may not be cause for alarm. But if you have one or more of these symptoms, even if you haven’t been diagnosed with any heart problems, you should visit your GP and ask the question “Could I have heart failure?”.
            
            """)
#-----------------------------------------------------------------------------------------------------------
lottie_coding = load_lottieurl("https://assets6.lottiefiles.com/packages/lf20_bsPjV4.json")
lottie_coding = load_lottieurl("https://assets6.lottiefiles.com/private_files/lf30_P2uXE5.json")

st.write("------")
footer="""<style>
a:link , a:visited{
color: white;
background-color: transparent;
text-decoration: none;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: none;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color:#5486ea ;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed and Built By 赵多多Takudzwa Gershom Choto <a style='display: block; text-align: center;'href="https://github.com/Gershom-Taku" target="_blank">人工智能创新实验@遵义师范学院(Zunyi Normal University)</a></p>
</div>

"""
st.markdown(footer,unsafe_allow_html=True)
''''
const admin = require('firebase-admin');
admin.initializeApp();

// ...

admin.appCheck().createToken(appId)
    .then(function (appCheckToken) {
      // Token expires in an hour.
      const expiresAt = Math.floor(Date.now() / 1000) + 60 * 60;

      // Return appCheckToken and expiresAt to the client.
    })
   .catch(function (err) {
     console.error('Unable to create App Check token.');
     console.error(err);
   });
   '''

                   
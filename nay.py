import  pandas as pd
from  PIL import  Image
import streamlit as st
import  os


@st.cache
def load_image(image_file):
    img = Image.open(image_file)
    return  img

def save_upload_file(uploadedfile):
    with open(os.path.join("",uploadedfile.name),"wb") as f:
        f.write(uploadedfile.getbuffer())
        return  st.success("".format(uploadedfile.name))

def main():
    st.title("File Uploads & Saved file to Directory App")
    menu = ["home","dataset","about"]
    choice = st.sidebar.selectbox("menu",menu)

    if choice == "home":
        st.subheader("upload images")
        image_file = st.file_uploader("upload image",type=['jpg','jpeg','jpg'])
        if image_file is not None:
            file_details = {"FileName":image_file.name,"FileType":image_file.type}
            st.write(file_details)
            st.write(type(image_file))
            img = load_image(image_file)
            st.image(img)

            with open(os.path.join("",image_file.name),"wb") as f:
                f.write(image_file.getbuffer())
                st.success("file saved")



        elif choice == "dataset":
            st.subheader("dataset")
            datafile = st.file_uploader("upload csv",type= ['csv'])
            if datafile is not None:
                file_details = {"FileName":datafile.name,"FileType":datafile.type}
                df = pd.read_csv(datafile)
                st.dataframe(df)


            else:
                st.subheader("about app")

if __name__ == '__main__':
    main()

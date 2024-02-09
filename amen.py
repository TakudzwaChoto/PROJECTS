import streamlit as st

val = st.sidebar.radio('Pick one!', ['A', 'B'])


def upload_video(key):
    st.write('key : ', key)
    if 'video_path' not in st.session_state:
        st.session_state['video_path'] = None
    # Let's user upload a file from their local computer

    uploaded_file = st.file_uploader(
        'Choose a file', key=key)
    if st.session_state['video_path'] != None:
        agree = st.checkbox(
            'Previous file found! Do you want to use previous video file?')
        if agree:
            vid = open(st.session_state['video_path'], 'rb')
            video_bytes = vid.read()
            st.video(video_bytes)
            return st.session_state['video_path']

    if uploaded_file is not None:
        # gets the uploaded video file in bytes
        bytes_data = uploaded_file.getvalue()
        file_details = {'Filename: ': uploaded_file.name,
                        'Filetype: ': uploaded_file.type,
                        'Filesize: ': uploaded_file.size}
        # st.write('FILE DETAILS: \n', file_details)
        st.session_state['video_path'] = uploaded_file.name
        st.write(st.session_state['video_path'])
        st.write('\n\nUploaded video file')
        # displays the video file
        st.video(uploaded_file)

        # saves the uploaded video file
        with open(uploaded_file.name, "wb") as vid:
            vid.write(bytes_data)
        return uploaded_file.name


# if the user presses "A" in the radio button
if val == "A":
    upload_video("A")

# if the user presses "B" in the radio button
if val == 'B':
    upload_video("B")





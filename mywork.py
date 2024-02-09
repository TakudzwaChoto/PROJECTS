import streamlit as st

st.markdown(" # `Markdown` ➡ to Streamlit App :balloon:")

import glob
import os

with open("README.md", 'r') as f:
    readme_line = f.readlines()
    readme_buffer = []
    resource_files = [os.path.basename(x) for x in glob.glob(f'Resources/*')]
    # resource_files
for line in readme_line:
    readme_buffer.append(line)
    for image in resource_files:
        if image in line:
            st.markdown(''.join(readme_buffer[:-1]))
            st.image(f'Resources/{image}')
            readme_buffer.clear()

st.markdown(''.join(readme_buffer))
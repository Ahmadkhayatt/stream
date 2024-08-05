import pandas as pd
import streamlit as st
import requests
st.write("hello")
@st.cache
def load_data(url):
    response = requests.get(url)
    df = pd.read_csv(pd.compat.StringIO(response.text))
    return df

url = 'https://raw.githubusercontent.com/Ahmadkhayatt/stream/main/News.csv'
df = load_data(url)
length = len(df)

# Streamlit App

window_texts = ["Read" for _ in range(length)]
Names = df['Article Name'].tolist()
page_contents = df['context'].tolist()
image_paths = df['image'].tolist()  # Convert to list to avoid any potential issues

# Initialize session state if not already done
if 'page' not in st.session_state:
    st.session_state.page = -1

# Function to create the main page with dynamic windows
def main_page(length):
    st.title("Main Page")
    num_cols = 3  # Number of columns per row
    cols = st.columns(num_cols)
    
    for i in range(length):
        col = cols[i % num_cols]
        
        with col:
            if i < len(image_paths):
                if pd.notna(image_paths[i]):
                    st.image(image_paths[i], use_column_width=True)
                else:
                    st.write(f"No image for index {i}")
            else:
                st.write(f"Index {i} is out of bounds for image_paths.")
            
            if i < len(Names):
                if pd.notna(Names[i]):
                    st.write(Names[i])
                else:
                    st.write(f"No name for index {i}")
            else:
                st.write(f"Index {i} is out of bounds for Names.")
            
            if st.button(window_texts[i], key=f"button_{i}"):
                st.session_state.page = i
                st.experimental_rerun()

# Function to create the content page for a specific window
def content_page(window_index):
    st.title(Names[window_index])
    
    if pd.notna(image_paths[window_index]):
        st.image(image_paths[window_index], use_column_width=True)
    else:
        st.write(f"No image for index {window_index}")

    st.write(page_contents[window_index])
    
    if st.button("Back to Main Page"):
        st.session_state.page = -1
        st.experimental_rerun()

# Display the appropriate page
if st.session_state.page == -1:
    main_page(length)
else:
    content_page(st.session_state.page)

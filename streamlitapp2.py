import pandas as pd
import streamlit as st
import requests
import io

st.write("hello")

@st.cache_data
def load_data(url):
    response = requests.get(url)
    df = pd.read_csv(io.StringIO(response.text))
    return df

url = 'https://raw.githubusercontent.com/Ahmadkhayatt/stream/main/News2.csv'
df = load_data(url)
length = len(df)

# Ensure the DataFrame has the expected columns
expected_columns = ['Article Name', 'context', 'image', 'page_url', 'translated_text']  # Include translated_text
for col in expected_columns:
    if col not in df.columns:
        st.error(f"Missing column in data: {col}")

window_texts = ["Read" for _ in range(length)]
Names = df['Article Name'].tolist()
page_contents = df['context'].tolist()
image_paths = df['image'].tolist()  # Convert to list to avoid any potential issues
page_url = df['page_url'].tolist()
translated_texts = df['translated_text'].tolist()  # Add this line to get the translated texts

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
            
            # Button to navigate to content page
            if st.button(window_texts[i], key=f"button_{i}"):
                st.session_state.page = i
                st.experimental_set_query_params(page=i)

# Function to create the content page for a specific window
def content_page(window_index):
    st.title(Names[window_index])
    
    if pd.notna(image_paths[window_index]):
        st.image(image_paths[window_index], use_column_width=True)
    else:
        st.write(f"No image for index {window_index}")

    st.write(page_contents[window_index])

    # Display the translated content with a header
    st.subheader("Translated Content")
    if pd.notna(translated_texts[window_index]):
        st.write(translated_texts[window_index])
    else:
        st.write(f"No translated content for index {window_index}")

    # Display the URL
    st.write("Read more at: ")
    st.markdown(f"[{page_url[window_index]}]({page_url[window_index]})")
    
    if st.button("Back to Main Page"):
        st.session_state.page = -1  # Reset to main page
        st.experimental_set_query_params(page=-1)

# Get the current page from query params
query_params = st.experimental_get_query_params()
page = int(query_params.get("page", [-1])[0])

# Update the session state based on the query params
st.session_state.page = page

# Display the appropriate page
if st.session_state.page == -1:
    main_page(length)
else:
    content_page(st.session_state.page)

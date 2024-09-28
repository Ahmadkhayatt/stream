import pandas as pd
import streamlit as st
import requests
import io



@st.cache_data
def load_data(url):
    response = requests.get(url)
    df = pd.read_csv(io.StringIO(response.text))
    return df

url = 'https://raw.githubusercontent.com/Ahmadkhayatt/stream/main/new_file_data2_newliy23.csv'
df = load_data(url)
length = len(df)

# Ensure the DataFrame has the expected columns
expected_columns = ['Article Name', 'context', 'page_url', 'output']  # Column names including 'output'
for col in expected_columns:
    if col not in df.columns:
        st.error(f"Missing column in data: {col}")

window_texts = ["Read" for _ in range(length)]
Names = df['Article Name'].tolist()
page_contents = df['context'].tolist()
page_url = df['page_url'].tolist()
output_texts = df['output'].tolist()  # Using 'output' as the column name

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
    
    # Display the context content
    st.subheader("Context")
    st.write(page_contents[window_index])

    # Display the output content with a clear description in red and bold
    st.markdown(
        "<h3 style='color: red; font-weight: bold;'>Summarized Output</h3>",
        unsafe_allow_html=True
    )  # Updated header to be clearer and styled
    if pd.notna(output_texts[window_index]):
        st.write(output_texts[window_index])  # Display the output text
    else:
        st.write(f"No summarized output for index {window_index}")

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

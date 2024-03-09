from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model=genai.GenerativeModel('gemini-pro-vision')
def get_gemini_response(input,image_data,user_prompt):
    response=model.generate_content([input,image_data[0],user_prompt])
    return response.text
def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        image_parts=[{
            'mime_type':uploaded_file.type,#represents the type eof the uploaded file
            'data':bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError('No file Uploaded')
with st.sidebar:
    st.write('This is a sidebar')


   
    
st.header('POEM GENERATOR')

input=st.text_input('Input prompt:',key='input')
uploaded_file=st.file_uploader('Image',type=['jpg','jpeg','png'])

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption='Uploaded File',use_column_width=True)

sub=st.button('GENERATE ME A POEM')

input_prompt="""You are an expert in understanding human faces and emotion.We will upload an image of a person and you will have to answer the qquestion or the euploaded image by generaating a 4 line poem for the person."""

if sub:
    with st.spinner('Wait'):
        image_data=input_image_details(uploaded_file)
        response=get_gemini_response(input_prompt,image_data,input)
        st.subheader('The response is')
        st.text_area(label="",value=response,height=500)

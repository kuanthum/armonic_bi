import streamlit as st
import json

import seaborn as sns
import matplotlib.pyplot as plt
from scrap import get_chords, get_youtube
from process import etl, chord_array, data
from acordes import get_key, detect_tone, get_linked, get_modals, modal_exchange



st.set_page_config(layout='wide')

st.markdown("<h1 style='text-align: center; color: white;'>Estructura armónica</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    band = st.text_input(label='Band:',value="",help="Type the band's name")

with col2:
    song = st.text_input(label="Song:",value="", help='Type the name of the song')
    
if band != "" and song != "":
    # Write link                             ---------------------------------------------
    link = get_youtube(band,song)
    st.write(f"[link]{link}")

    #Get json from chordify                  ---------------------------------------------
    tone, chords = get_chords(band,song) # From scrap
    clean_chords = etl(chords) # From procces ETL

    # Get Tone                               ---------------------------------------------
    acordes, grados = get_key(tone) 

    # Clean list of chords                   ---------------------------------------------
    arr = chord_array(clean_chords,grados,acordes)
    df = data(arr)

    # Detectar mayor o menor                 ---------------------------------------------
    mode = detect_tone(df)
    st.subheader(f"Tone: {tone} {mode}")
   
#Plots                                       ---------------------------------------------
    st.subheader("Estructura armónica")
    fig = sns.catplot(x="beat", y="chord", data=df, height=5, aspect=5, s=10, kind='strip', order=df['chord'].value_counts().index )
    st.pyplot(fig)

    st.subheader("Grados utilizados")
    fig2 = sns.catplot(x='chord', kind='count', data=df, height=3, aspect=3, order=df['chord'].value_counts().index)
    st.pyplot(fig2)

    enlaces_df = get_linked(arr)

    st.subheader("Enlaces utilizados")
    fig3 = sns.catplot(x='chord', kind='count', data=enlaces_df, height=10, aspect=2, order=enlaces_df['chord'].value_counts().index)
    plt.xticks(rotation = 45);

    st.pyplot(fig3)

    st.subheader("Recursos no convencionales")
    modals = get_modals(enlaces_df, mode)
    st.text(modals[0])

    st.subheader("Intercambios modales")
    exchange = modal_exchange(modals[1])
    pretty = json.dumps(exchange, indent=4)
    st.text(pretty)

####################################################################
### IMPORTS
####################################################################

from re import S
import streamlit as st
import numpy as np
import pandas as pd
import requests
from PIL import Image
from annotated_text import annotated_text
import streamlit.components.v1 as components

import os
import json
from os import listdir
from os.path import isfile, join

import spacy
from spacy_streamlit import visualize, visualize_ner, visualize_textcat, visualize_tokens, process_text

from spacy.vocab import Vocab
from spacy.tokens import Doc
import base64

####################################################################
### SIDEBAR & CONFIG
####################################################################

st.set_page_config(
            page_title="Projet Ephesus", # => Quick reference - Streamlit
            page_icon="",#on a choisi le logo standard mais on peut mettre au chose "🐍",
            layout="wide",
            initial_sidebar_state="auto") # collapsed


image = Image.open('images/wagon.png')
st.sidebar.image(image, caption='Le Wagon', use_column_width=False)
st.sidebar.markdown("")

direction = st.sidebar.radio('', ('Projet Ephesus', 'Démo', 'Run', 'Et pour finir'))

####################################################################
### PAGE 1 - Présentation du projet Ephesus
####################################################################

if direction == 'Projet Ephesus':


    html_code = '''
        <a target="_blank" href="https://geoffroygit.github.io/ephesus/notebooks/Ephesus.slides.html">
        <img src="https://raw.githubusercontent.com/JulianBreaud/ephesusWeb/master/images/fullscreen.png" /></a>
        <iframe width="100%" height="550" scrolling="yes" frameborder="no"
        allowfullscreen src="https://geoffroygit.github.io/ephesus/notebooks/Ephesus.slides.html"></iframe>
            '''
    components.html(html_code, height = 600)

####################################################################
### PAGE 2 - DEMO
####################################################################

elif direction == 'Démo':

    st.markdown("""
    # Démo

    """)

    # Son du Mémo
    st.markdown("""
        ### Réalisation d'un mémo vocal par une infirmière :
    """)
    st.write("")
    audio_file = open('audio/Prise_de_sang.m4a', 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format='audio/ogg')

    # Translation du mémo
    st.markdown("""
        ### Transcription du mémo :
    """)
    text = st.text_area("", "Prise de sang à domicile le samedi 26 février à 8h15 par amandine.")

    # identification des labels
    st.markdown("""
        ### Analyse :
    """)

    #----------------------------------------------------#
    #nlp = spacy.load("models/model_full/model-best")
    #doc = nlp(text)
    # replace the two lines of code above by an API call:
    predict_url = "https://ephesus-api-3d2vvkkptq-ew.a.run.app/predict"
    predict_params = {"sentence" : text}
    predict_response = requests.get(predict_url, params=predict_params)
    if predict_response.status_code == 200:
        predict_response = predict_response.json()
    else:
        predict_response = {} # (we need to better handle the errors)
    # create Doc() object from vocab bytes and doc bytes
    labels = predict_response["labels"]
    doc_bytes = base64.b64decode(predict_response["doc"])
    vocab_bytes = base64.b64decode(predict_response["vocab"])
    vocab = Vocab()
    vocab.from_bytes(vocab_bytes)
    doc = Doc(vocab).from_bytes(doc_bytes)
    #----------------------------------------------------#


    visualize_ner(doc, labels=labels,
    show_table = False,
    title = "",
    colors = {
        "Treatment" : "#99CCFF",
        "Cotation" : "#444444", #hors palette
        "Date" : "#B2E7E8",
        "Time" : "#8FB9AA",
        "Duration" : "#F2D096",
        "Frequency" : "#ED895",
        "Location" : "#FFCC99", #hors palette
        }
        )

    # Codage des labels
    st.markdown("""
        ### Traitement :
    """)

    liste = []
    for index, ent in enumerate(doc.ents):
        liste.append((str(doc.ents[index]), ent.label_))

    # url de l'api
    url = 'https://ephesus-api-3d2vvkkptq-ew.a.run.app/'

    endpoints = {
        "Treatment" : "treatment",
        "Date" : "date",
        "Time" : "time",
        "Location" : "location",
        }

    st.write("Nombre d'éléments détectés : " + str(len(liste)))

    for item in liste:
        if item[1] in endpoints:
            url_full = url + endpoints[item[1]]

        st.write(item[1] + " : " + item[0])

        params = {
            "sentence" : item[0]
            }

        # retrieve the response
        response = requests.get(
            url_full,
            params=params
        )



        if response.status_code == 200:
            response_api = response.json()

            df = pd.DataFrame(data = [response_api.values()],
                columns=response_api.keys()
                )

            # CSS to inject contained in a string
            hide_dataframe_row_index = """
                        <style>
                            .row_heading.level0 {display:none}
                            .blank {display:none}
                        </style>
                        """

            # Inject CSS with Markdown
            st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

            st.dataframe(df)
#


####################################################################
### PAGE 3 - RUN
### on importe l'ensemble des translations et on lance le modèle et on obtient un rapport d'éxécution
####################################################################

elif direction == 'Run':

    st.markdown("""
    # Récupération de plusieurs mémos

    """)

    st.markdown("""
        ### Partie 1 - Récupération des mémos retranscrits :
    """)

    rep = st.text_input('Les memos sont dans le repertoire :', "raw_data/input_json")

    LOCAL_PATH =str(rep)

    # récupération des noms des fichiers output translation des memos vocaux
    fichiers = [fichier for fichier in listdir(LOCAL_PATH) if isfile(join(LOCAL_PATH, fichier))]

    data = []
    for fichier in fichiers :
        lib_fichier = LOCAL_PATH + "/" + fichier
        with open(lib_fichier) as mon_fichier:
            data.append(json.load(mon_fichier))

    # récupération seulement de la phrase = sentence du mémo
    data = [data[i]["Translation"] for i in range(len(data))]

    # on écrit une ligne vide pour la présentation
    st.write("")

    if len(data) > 1 :
        st.write(f"{len(data)} translations trouvées : ")
    else :
        st.write(f"{len(data)} translation trouvée : ")

    for i in range(len(data)) :
        st.write(data[i])

    st.markdown("""
        ### Partie 2 - Lancement de l'analyse :
    """)
    if st.button("GO"):
            # print is visible in the server output, not in the page
            print('button clicked!')
            st.write('Analyse lancée 🎉')

            # url de l'api
            url = 'https://ephesus-api-3d2vvkkptq-ew.a.run.app/test'

            st.markdown("""
                            ### Partie 3 - Les résultats :
                            """)

            for i in range(len(data)) :

                params = {
                    "sentence" : data[i]
                    }

                # retrieve the response
                response = requests.get(
                    url,
                    params=params
                )

                st.write('Phrase ' + str(i) + " :")

                if response.status_code == 200:
                    response_api = response.json().get("entities", "not found")
                    response_api = tuple(tuple(i) if type(i)==type([]) else i for i in response_api)
                    annotated_text(*response_api)

                st.write("")

            st.markdown("""
                        ### Partie 4 - Le rapport d'exécution :
                        """)

            col1, col2 = st.columns(2)
            col1.metric("Nombre de documents lus", len(data), "")
            col2.metric("Taux de reconnaissances", "80%", "")

            # rapport d’exécution : le nombre de rejet, taux de détections, de reconnaissance

####################################################################
### PAGE 4 - FIN
####################################################################

else:
    '''
    # Merci pour votre écoute.
    # Avez-vous des questions ?
    '''

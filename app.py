
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

import ast
import zipfile
import time

####################################################################
### SIDEBAR & CONFIG
####################################################################

st.set_page_config(
            page_title="Projet Ephesus", # => Quick reference - Streamlit
            page_icon="",#on a choisi le logo standard mais on peut mettre au chose "🐍",
            layout="wide",
            initial_sidebar_state="auto") # collapsed


image = Image.open('images/medical.png')
st.sidebar.image(image, caption="", use_column_width=False)
st.sidebar.markdown("")

pages = ('Projet Ephesus', 'Démo', 'Run')#('Projet Ephesus', 'Démo', 'Run', 'Et pour finir')
direction = st.sidebar.radio('', pages)

####################################################################
### PAGE 1 - Présentation du projet Ephesus
####################################################################

if direction == pages[0]:
    presentation0 = Image.open('images/PresentationPage0.PNG')
    presentation1 = Image.open('images/PresentationPage1.PNG')
    presentation2 = Image.open('images/PresentationPage2.PNG')
    presentation3 = Image.open('images/PresentationPage3.PNG')

    if "persisted_variable" not in st.session_state:
        st.session_state.persisted_variable = 0

    columns_Page = st.columns(7)
    if columns_Page[6].button("▶️"):
        st.session_state.persisted_variable += 1

    if columns_Page[0].button("◀️"):
        st.session_state.persisted_variable -= 1

    # st.session_state.persisted_variable

    if st.session_state.persisted_variable == 0:
        st.image(presentation0, use_column_width=True)

    if st.session_state.persisted_variable == 1:
        st.image(presentation1, use_column_width=True)

    if st.session_state.persisted_variable == 2 :
        st.image(presentation2, use_column_width=True)

    if st.session_state.persisted_variable == 3 :
        st.image(presentation3, use_column_width=True)

    # Afficher une présentation html
    # html_code = '''
    #    <a target="_blank" href="https://geoffroygit.github.io/ephesus/notebooks/Ephesus.slides.html">
    #    <img src="https://raw.githubusercontent.com/JulianBreaud/ephesusWeb/master/images/fullscreen.png" /></a>
    #    <iframe width="100%" height="550" scrolling="yes" frameborder="no"
    #    allowfullscreen src="https://geoffroygit.github.io/ephesus/notebooks/Ephesus.slides.html"></iframe>
    #        '''
    # components.html(html_code, height = 600)

####################################################################
### PAGE 2 - DEMO
####################################################################

elif direction == pages[1]:

    # initialise session state
    if "button_audio2text_pressed" not in st.session_state:
        st.session_state.button_audio2text_pressed = False
    if "api_is_online" not in st.session_state:
        error_free = True # we assume the api is online
        st.session_state.api_is_online = error_free

    def run_models(text):
        '''
        return True is all is well
        return False if there's an error with api calls
        '''

        if not st.session_state.api_is_online:
            return False

        st.markdown("### Automatisation de l'analyse du texte")

        # api url
        api_base_url = "https://ephesus-api-3d2vvkkptq-ew.a.run.app/"

        colors = {
                "Treatment" : "#99CCFF",
                "Cotation" : "#444444", #hors palette
                "Date" : "#B2E7E8",
                "Time" : "#8FB9AA",
                "Duration" : "#F2D096",
                "Frequency" : "#ED895",
                "Location" : "#FFCC99", #hors palette
                }

        key_translation = {
            "NGAP" : "code facturation",
            "location" : "Lieu",
            "day" : "Jour",
            "month" : "Mois",
            "year" : "Année",
            "day_of_week" : "Jour de la semaine",
            "day_from_today" : "Jour relatif",
            "hour" : "Heure",
            "minute" : "Minutes"
        }

        # identify entities
        predict_url = api_base_url + "predict"
        predict_params = {"sentence" : text}
        predict_response = requests.get(predict_url, params=predict_params)
        if predict_response.status_code == 200:
            predict_response = predict_response.json()
        else:
            # error: most likely the api is offline
            st.session_state.api_is_online = False
            return False

        # create Doc() object from vocab bytes and doc bytes
        labels = predict_response["labels"]
        doc_bytes = base64.b64decode(predict_response["doc"])
        vocab_bytes = base64.b64decode(predict_response["vocab"])
        vocab = Vocab()
        vocab.from_bytes(vocab_bytes)
        doc = Doc(vocab).from_bytes(doc_bytes)

        # show entities on screen
        visualize_ner(doc, labels=labels,
                    show_table = False,
                    title = "",
                    colors = colors)

        # feed entities to the models for treatment, date, time, location
        # list entities
        entities = [(str(ent), ent.label_) for ent in doc.ents]

        endpoints = {
            "Treatment" : "treatment",
            "Date" : "date",
            "Time" : "time",
            "Location" : "location",
            }

        columns_models = st.columns(len(entities))

        for i, item in enumerate(entities):
            if item[1] not in endpoints:
                continue
            url_full = api_base_url + endpoints[item[1]]
            params = {"sentence" : item[0]}
            # api call
            response = requests.get(url_full, params=params)
            if response.status_code == 200:
                response_api = response.json()

                # show api response on screen
                #columns_models[i].markdown(f"#### {item[1]}")
                #columns_models[i].markdown(f"##### {item[0]}")
                color = colors[item[1]]
                for key, val in response_api.items():

                    # special treatment for missing values, day of week
                    # and softmax and sigmoid
                    # to improve readability
                    if str(val) == "99":
                        val = "absent"
                    elif key == "day_of_week":
                        val += 1
                    if key == "sigmoid":
                        if val < 0.5:
                            val = 1 - val
                    if key == "sigmoid" or key == "softmax":
                        val = f"{int(val * 100)}%"
                        key = "Confiance"
                    if key in key_translation:
                        key = key_translation[key]

                    columns_models[i].markdown(
                        f'<p style="background-color: {color}">{key} : {val}</p>',
                        unsafe_allow_html=True)
            else:
                st.session_state.api_is_online = False
                return False
        return True

    def run_transcription():
        # Text of the memo (can be changed by the user)
        text = st.text_area("", memo)
        # run the models
        return run_models(text)

    # Son du Mémo
    st.markdown("""
        ### Réalisation d'un mémo vocal par le personnel soignant
    """)
    # create columns to put the audio and the button side by side
    columns = st.columns(2)
    # load audio file
    audio_file = open('audio/Prise_de_sang.m4a', 'rb')
    audio_bytes = audio_file.read()
    columns[0].audio(audio_bytes, format='audio/ogg')
    # text transcript
    memo = "Prise de sang à domicile le samedi 26 février à 8h15 par Amandine."

    if not st.session_state.button_audio2text_pressed:
        # show button transcription
        if columns[1].button("Transcription du mémo"):
            st.session_state.button_audio2text_pressed = True
            error_free = run_transcription()
    else:
        error_free = run_transcription()

    if not error_free:
        st.error("Oups, quelque chose s'est mal passé. L'API est probablement hors ligne.")


# ####################################################################
# ### PAGE 3 - RUN
# ### on importe l'ensemble des translations et on lance le modèle et on obtient un rapport d'éxécution
# ####################################################################

elif direction == pages[2]:

    st.markdown("""
    # Sélectionner un ou plusieurs fichier(s) JSON
    """)

    uploaded_files = st.file_uploader(label="Uniquement des fichiers Translation", accept_multiple_files=True)

    st.markdown("""
                ### Rapport d'exécution :
                """)

    st.write("Nombre de fichiers téléchargés : " + str(len(uploaded_files)))

    if len(uploaded_files) > 0 :

        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            fichier = uploaded_file.name
            cle_fichier = fichier.replace("_translation.json","")
            cle_fichier
            text_1 = ast.literal_eval(bytes_data.decode("utf-8"))
            translation = text_1['Translation']
            translation

            dict_response_api = {
                "cle_fichier" : cle_fichier,
                "translation" : translation
            }

            fichier_output = "output/" + cle_fichier + "_translation.json"

            jsonString = json.dumps(dict_response_api)
            jsonFile = open(fichier_output, "w")
            jsonFile.write(jsonString)
            jsonFile.close()


        list_fichiers = os.listdir('output')
        list_fichiers_json = [fichier for fichier in list_fichiers if "json" in fichier ]

        list_fichiers_json

        with zipfile.ZipFile("output/json_output.zip", mode="w") as archive:
                for fichier in list_fichiers_json:
                    archive.write("output/" + fichier)

        with open('output/json_output.zip', 'rb') as f:
            st.download_button('Download Zip', f)


    # # url de l'api
    # url = 'https://ephesus-api-3d2vvkkptq-ew.a.run.app/test'

    # st.markdown("""
    #                 ### Partie 3 - Les résultats :
    #                 """)

    # for i in range(len(data)) :

    #     params = {
    #         "sentence" : data[i]
    #         }

    #     # retrieve the response
    #     response = requests.get(
    #         url,
    #         params=params
    #     )

    #     st.write('Phrase ' + str(i) + " :")

    #     if response.status_code == 200:
    #         response_api = response.json()



#             # rapport d’exécution : le nombre de rejet, taux de détections, de reconnaissance

# ####################################################################
# ### PAGE 4 - FIN
# ####################################################################

# else:
#     '''
#     # Merci pour votre écoute.
#     # Avez-vous des questions ?
#     '''

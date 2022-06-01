import streamlit as st
import datetime
import requests
from PIL import Image
from annotated_text import annotated_text

st.set_page_config(
            page_title="Projet Ephesus", # => Quick reference - Streamlit
            page_icon="🐍",
            layout="centered", # wide
            initial_sidebar_state="auto") # collapsed

# SIDEBAR

image = Image.open('images/wagon.png')
st.sidebar.image(image, caption='Le Wagon', use_column_width=False)
st.sidebar.markdown(f"""
    # Navigation
    """)

direction = st.sidebar.radio('Aller à', ('Présentation du projet Ephesus', 'Démo', 'Page3', 'Et pour finir'))

# PAGE 1 - Présentation du projet Ephesus
if direction == 'Présentation du projet Ephesus':
    st.markdown("""
    # Projet EPHESUS

    ## Interpréter les données textuelles générées par des mémos vocaux.

    Les infirmières lors de visite d’un patient, prennent une photo de la prescription médicale et
    réalisent un mémo vocal décrivant les tâches à effectuer. Ces informations sont ensuite
    saisies par des facturières qui réalisent toute la gestion du cabinet (télétransmission,
    compta). L’objectif est de préremplir les données d’une prescription afin que les facturières
    augmentent en productivité et puissent se concentrent sur la partie à forte valeur ajoutée et
    plus complexe.

    """)

# PAGE 2 - Présentation du projet Ephesus
elif direction == 'Démo':
    st.markdown("""
    # Démo

    """)

    # la partie - Son du Mémo
    st.markdown("""
        ### Merci d'enregistrer un mémo :
    """)

    # la partie - Translation du mémo
    st.markdown("""
        ### La translation du mémo :
    """)
    translation = st.text_area('',
        '''
        Un grand pansement à domicile à partir du 3 juin, tournée 2 , tous les deux
        jours pendant 3 semaines, 10 Km aller/retour IK montagne , en ald.
        ''')

    st.write('Longueur du mémo :', len(translation))

    columns = st.columns(2)
    if columns[0].button("Lancer l'analyse"):
        # print is visible in the server output, not in the page
        print('button clicked!')
        columns[1].write('Analyse lancée 🎉')

        # url de l'api
        url = 'https://ephesus-api-3d2vvkkptq-ew.a.run.app/test'

        params = {
            "sentence" : translation
            }

        # retrieve the response
        response = requests.get(
            url,
            params=params
        )

        st.markdown("""
                    ### Le résultat :
                    """)

        if response.status_code == 200:
            response_api=response.json().get("entities", "not found")
            response_api = tuple(tuple(i) if type(i)==type([]) else i for i in response_api)
            annotated_text(*response_api)

        else:
            st.error('Sorry ...')

    else:
        columns[1].write('Analyse non lancée 😞')


    # la partie - Resultats






# PAGE 3 -
elif direction == 'Page3':
    st.write('Page3')

# PAGE 4 - FIN
else:
    '''
    # Merci pour votre écoute.
    # Avez-vous des questions ?
    '''

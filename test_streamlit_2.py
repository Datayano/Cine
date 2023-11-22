import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO
import time
from streamlit_card import card


#Je charge mes différentes tables
df_film = pd.read_csv('table_film_finale.csv')
df_intervenants = pd.read_csv('table_intervenants_finale.csv')
df_liaison = pd.read_csv('table_de_liaison.csv')
df_recommandation_basic = pd.read_csv('df_recommandation_basic.csv')

#Création d'une bare laterale (st.sidebar()) contenant un menu déroulant (st.selectbox()) de 3 pages : "Acceuil", "Système de recommandation", "Test")
with st.sidebar.title("Navigation") :
        selection = st.sidebar.selectbox("Sélectionnez une page", ["Acceuil", "Système de recommandation", "Test"])

#Page "Acceuil" :
if selection == "Acceuil" :

        #Titre de la page d'acceuil : st.title()
        st.title("Bienvenue sur  d'accueil")

        #Auteur : st.subheader()
        st.subheader("Auteur : Bamba SYLLA, FROQUET Yann, DOIZON Sevan")

        #Description de l'application : st.write()
        st.write("**Bienvenue à toi ! Tu as apprécié nos diffusions ? Prolonge ton bonheur avec nos recommandations que tu apprécieras à coup sûr !**")
        st.write("*Texte de fonctionnement du site*")

#Page "Système de recommandation"
elif selection == "Système de recommandation" :

        titre = st.selectbox(
                        label = "choisir un film", #menu déroulant de label (=titre) "choisir un film"
                        options = df_film['title'] #menu déroulant qui itère les films de df_film 
                        )

        condition_film = df_film['title'] == titre #je filtre mon df_film sur le film selectionné 
        title_id = df_film[condition_film].loc[:,'titleId'].values[0] #je récupère l'id du film

        condition_liaison = df_liaison['titleId'] == title_id #je filtre mon df_liaison sur l'id selectionné 
        liste_intervenants = df_liaison.loc[condition_liaison, 'nconst'].values #je recupère la liste des intervenants du film


        #Je divise la page en 2 colonnes
        col_film_image, col_film_infos = st.columns(2)

        #Contenu de la première colonne : Poster du film
        with col_film_image :

                url = df_film[condition_film].loc[:,'Poster'].values[0]
                st.image(url)

        #Contenu de la deuxième colonne : Informations sur le film
        with col_film_infos :

                        df_info = df_film[condition_film]
                        liste_colonne = list(df_info.columns)

                        for indice, colonne in enumerate(liste_colonne) :
                                if indice in [3, 4, 6, 7, 8, 11, 16, 17] :
                                        info = df_info[colonne].values[0]
                                        st.markdown(f"🎥 {colonne} : {info}")

        #Je crée un bouton déroulant contenant les informations sur les 3 principaux intervenants
        with st.expander("Informations casting"):

                        condition_intervenants = df_intervenants['IMdb'].isin(liste_intervenants)
                        df_intervenants_film = df_intervenants[condition_intervenants].reset_index().sort_values(by=['Popularité'], ascending=False)
                        
                        col_intervenant_1, col_intervenant_2, col_intervenant_3 = st.columns(3)

                        with col_intervenant_1 :

                                st.image(df_intervenants_film.loc[0, 'Image'])
                                st.write(df_intervenants_film.loc[0, 'Biographie'])

                        with col_intervenant_2 :

                                st.image(df_intervenants_film.loc[1, 'Image'])
                                st.write(df_intervenants_film.loc[1, 'Biographie'])

                        with col_intervenant_3 :

                                st.image(df_intervenants_film.loc[2, 'Image'])
                                st.write(df_intervenants_film.loc[2, 'Biographie'])


        recommandation_basic, recommandation_keywords = st.columns(2)

        #Colonne du système de recommandation basique :
        with recommandation_basic :
                bouton_reco_basic = st.button(label = "Système de recommandation basique : ")

        #Colonne du système de recommandation keywords :
        with recommandation_keywords :
                bouton_reco_keywords = st.button(label = "Système de recommandation keywords : ")

        #Si l'utilisateur clique sur recommandation basique
        if bouton_reco_basic :

                        condition_reco_basic = df_recommandation_basic['Film'] == titre
                        df_recommandation_basic_film = df_recommandation_basic[condition_reco_basic].reset_index()

                        reco_basic_1, reco_basic_2, reco_basic_3 = st.columns(3)

                        with reco_basic_1 :

                                title_reco_basic_1 = df_recommandation_basic_film.iloc[0, 2]
                                bouton_reco_basic_1 = st.button(label = title_reco_basic_1)

                                #""" def on_image_click(image_reco_basic_1):
                                #        return "Test" """

                                condition_reco_basic_image_1 = df_film['title'] == title_reco_basic_1
                                st.image(df_film[condition_reco_basic_image_1].iloc[0,14])
                                #image = 
                                #image_reco_basic_1 = st.image(df_film[condition_image_reco_basic_1].iloc[0,14], use_column_width=True)
                                #image_reco_basic_1.alt = df_film[condition_image_reco_basic_1].iloc[0,14]

                                #if image_reco_basic_1.button_clicked :
                                #        selection = on_image_click(df_film[condition_image_reco_basic_1].iloc[0,14])
                                        
                                        #break


                        with reco_basic_2 :

                                title_reco_basic_2 = df_recommandation_basic_film.iloc[0, 3]
                                bouton_reco_basic_2 = st.button(label = title_reco_basic_2)

                                condition_reco_basic_image_2 = df_film['title'] == title_reco_basic_2
                                st.image(df_film[condition_reco_basic_image_2].iloc[0,14])

                        with reco_basic_3 :

                                title_reco_basic_3 = df_recommandation_basic_film.iloc[0, 4]
                                bouton_reco_basic_3 = st.button(label = title_reco_basic_3)

                                condition_reco_basic_image_3 = df_film['title'] == title_reco_basic_3
                                st.image(df_film[condition_reco_basic_image_3].iloc[0,14])

                        if bouton_reco_basic_1 :
                                st.write('Test 1')

                        elif bouton_reco_basic_2 :
                                st.write('Test 2')

                        elif bouton_reco_basic_3 :
                                st.write('Test 3')

elif selection == "Test" :

        st.write('Test')
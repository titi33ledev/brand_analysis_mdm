#%%
import streamlit as st
from streamlit_plotly_events import plotly_events
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid
from scrap_mdm import brand_worldcloud,compute_stats, scrap_products_url, get_image_count, process, scrap_first_page

st.title('Analyse des fiches produits sur Maison du Monde')
st.markdown('Vous allez découvrir les informations pertinentes sur la marque que vous recherchez sur Maison du Monde.')
st.markdown('Pensez bien à mettre le nom de la marque comme elle est indiqué sur la marketplace.')
st.markdown("Nous vous conseillons de faire le test en amont en recherchant sur Maison du Monde le nom de la marque et par la suite de l'ajouter dans la barre de recherche")


mot_cles = st.text_input('Écris ce que tu veux rechercher', '...')
if mot_cles != '...':
    st.write('La marque choisi est : ', mot_cles)
    soup = scrap_first_page(mot_cles)
    df = process(soup)
    moyenne_images = scrap_products_url(df)
    
if 'df' in locals():
    moyenne_caracteres_titres, moyenne_prix, mediane_prix = compute_stats(df)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Moy. longueurs titres",f"{moyenne_caracteres_titres:.2f}")
    col2.metric("Moyenne des prix", f"{moyenne_prix:.2f} €")
    col3.metric("Médiane des prix", f"{mediane_prix:.2f} €")
    col4.metric("Nombre d'images moy.",f"{moyenne_images:.2f}")

    st.subheader("Partie 2 : Analyse des caractères produits :abc:")
    
    image_wordcloud = brand_worldcloud(df)
    st.image(image_wordcloud)

    fig =  px.box(df, y="prix", title="Analyse des prix")
    st.plotly_chart(fig)
# %%

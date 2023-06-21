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

    #Afficher nuages de mots les plus fréquents
    
    image_wordcloud = brand_worldcloud(df)
    st.image(image_wordcloud)

    #Afficher quartiles des prix
    fig =  px.box(df, y="prix", title="Analyse des prix")
    st.plotly_chart(fig.show())


#         # Afficher le boxplot des prix
#         fig_quartiles = quartiles_prix_boxplot(df)
#         st.plotly_chart(fig_quartiles)

#         st.markdown("La boîte à moustaches (quartiles_prix_boxplot) est un outil mathématique et graphique qui permet d'analyser la répartition des prix dans un ensemble de données. Elle fournit des informations sur les quartiles, la médiane, les valeurs aberrantes et l'étendue des prix. Ces mesures statistiques permettent d'évaluer la dispersion et la distribution des prix, ce qui est utile pour la comparaison des données, la détection des valeurs aberrantes et la prise de décision éclairée.")
        

#         st.subheader("Partie 2 : Analyse des caractères produits :abc:")
        
#         #Afficher nuages de mots les plus fréquents
#         image_wordcloud, titles_filtre = title_to_worldcloud(df)
#         st.image(image_wordcloud)
        
#         st.markdown("Le WordCloud est une représentation graphique des mots les plus fréquents dans les titres des produits. Il permet une visualisation rapide des mots clés pertinents et des tendances. Les mots sont affichés en fonction de leur fréquence, avec une taille plus grande pour les mots les plus fréquents.")

#         # Afficher le classement des caractères les plus donnés
#         fig_classement_caracteres = n_gram(titles_filtre)
#         st.plotly_chart(fig_classement_caracteres)
# %%

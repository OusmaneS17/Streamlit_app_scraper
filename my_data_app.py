import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
import time
from PIL import Image

# Configuration générale de la page
st.set_page_config(
    page_title="Web Scraper App 🚀",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Chargement des images
scraping_img = "https://images.unsplash.com/photo-1600703508486-75e63378fc8a"
dashboard_img = "data/barometer-6550830_1280.jpg"
evaluation_img = "https://cdn.pixabay.com/photo/2022/03/01/11/09/check-7044608_1280.jpg"

st.markdown("""
    <style>
        /* Personnalisation du menu latéral (sidebar) */
        .css-1d391kg {
            background-color: #4C6B89; /* Couleur de fond */
            border-radius: 10px;
            padding: 10px;
            font-family: 'Arial', sans-serif;
        }
        
        /* Personnalisation du texte du menu */
        .css-1d391kg label {
            font-size: 1.2rem;
            color: white;
            font-weight: bold;
        }

        /* Personnalisation des éléments du menu */
        .css-1d391kg .st-radio input {
            accent-color: #FFC107; /* Couleur du bouton sélectionné */
        }

        .css-1d391kg .st-radio label {
            font-size: 1.1rem;
            color: #D6E4F0;
        }

        /* Effet hover sur les éléments du menu */
        .css-1d391kg .st-radio label:hover {
            color: #FFC107;
            cursor: pointer;
        }

        /* Personnalisation de l'élément actif */
        .css-1d391kg .st-radio label[aria-checked="true"] {
            color: white;
            font-weight: bold;
        }
            
        .metric-box {
            background-color: #f0f0f5;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .metric-box h3 {
            font-size: 1.5rem;
            font-weight: bold;
        }
        .metric-box p {
            font-size: 2rem;
            color: #333;
        }
        .stMetrics {
            display: flex;
            justify-content: space-between;
        }
    </style>
""", unsafe_allow_html=True)

# Barre latérale avec images et liens
st.sidebar.image(scraping_img, caption="🚀 Bienvenue dans l'app !")
st.sidebar.title("📊 Web Scraper Dashboard")
st.sidebar.markdown("Naviguez entre les sections 👇")

# Menu de navigation
menu = st.sidebar.radio("Choisissez une section :", ["🏠 Accueil", "🕵️‍♂️ Scraping", "📊 Dashboard", "📝 Évaluation", "📥 Charger des Données Scrapées"])

# --- Page d'accueil ---
if menu == "🏠 Accueil":
    st.title("Bienvenue dans l'application Web Scraper 🎉")
    st.image(scraping_img, use_column_width=True)
    st.markdown("""
    Cette application vous permet de :
    - **🔍 Scraper des données**
    - **📊 Visualiser et analyser ces données**
    - **💾 Télécharger les résultats**
    - **📝 Évaluer l'application avec un formulaire convivial**
    """)

    # Animation de chargement
    with st.spinner("Chargement des sections interactives..."):
        time.sleep(2)
    st.success("Les fonctionnalités sont prêtes ! 🚀")

# --- Scraping ---
# Configuration du menu
if menu == "🕵️‍♂️ Scraping":
    st.header("Scraping de Données 🕵️")
    st.image(scraping_img, caption="Extraction intelligente de données", use_column_width=True)

    # URL et nombre de pages à scraper pour Expat Dakar
    base_url = "https://www.expat-dakar.com/refrigerateurs-congelateurs?page="
    start_page = st.number_input("Numéro de page de départ :", min_value=1, value=2)
    end_page = st.number_input("Numéro de la dernière page :", min_value=start_page, value=6)

    # Fonction de scraping Expat Dakar
    def scrape_data_expat_dakar(start_page, end_page):
        data_all_url1 = []
        for page_num in range(start_page, end_page + 1):
            url1 = base_url + str(page_num)
            try:
                response = requests.get(url1)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "lxml")
                    data_table = soup.find('div', class_="listings-cards__list")

                    if data_table:
                        body_data_table = data_table.find_all('div', class_="listings-cards__list-item")

                        for listing_item in body_data_table:
                            # Extraction des détails
                            titre_element = listing_item.find('div', class_='listing-card__header__title')
                            titre = titre_element.text.strip() if titre_element else "N/A"

                            etat_frigo_element = listing_item.find('div', class_='listing-card__header__tags')
                            etat_frigo = etat_frigo_element.text.strip() if etat_frigo_element else "N/A"

                            zone_element = listing_item.find('div', class_='listing-card__header__location')
                            zone = zone_element.text.strip() if zone_element else "N/A"

                            date_element = listing_item.find('div', class_='listing-card__header__date')
                            date = date_element.text.strip() if date_element else "N/A"

                            prix_element = listing_item.find('span', class_='listing-card__price__value')
                            prix = prix_element.text.strip() if prix_element else "N/A"

                            # Construction des données
                            row_data = {
                                "Titre": titre,
                                "Etat": etat_frigo,
                                "Adresse": zone,
                                "Prix": prix,
                                "Date Publication": date,
                                "URL Page": url1
                            }
                            data_all_url1.append(row_data)
                    else:
                        st.warning(f"⚠️ Aucune donnée trouvée pour la page {page_num}.")
                else:
                    st.error(f"Erreur pour la page {page_num}. Code : {response.status_code}")
            except Exception as e:
                st.error(f"Erreur lors du scraping de la page {page_num} : {e}")
        return pd.DataFrame(data_all_url1)

    # Bouton pour lancer le scraping
    if st.button("🚀 Lancer le scraping"):
        with st.spinner("Scraping en cours..."):
            scraped_data = scrape_data_expat_dakar(start_page, end_page)
            if not scraped_data.empty:
                st.success(f"✅ {len(scraped_data)} annonces récupérées.")
                st.dataframe(scraped_data)

                # Téléchargement des données en CSV
                csv = scraped_data.to_csv(index=False)
                st.download_button(
                    label="📥 Télécharger les données en CSV",
                    data=csv,
                    file_name="scraped_data.csv",
                    mime="text/csv"
                )
            else:
                st.warning("⚠️ Aucune donnée récupérée.")

# --- Dashboard ---

# Charger les données
data = pd.read_excel("data/Cleaned/Climatisation_cleaned.xlsx")

if menu == "📊 Dashboard":
    st.header("Dashboard des Données des climatiseurs📊")
    st.image(dashboard_img, caption="Analyse dynamique des données", use_column_width=True)

    if not data.empty:

        # 📊 Boîtes pour afficher les KPIs
        col1, col2 = st.columns(2)

        # Prix moyen
        prix_moyen = data["Prix"].mean() if "Prix" in data.columns else 0
        with col1:
            st.markdown(f'<div class="metric-box"><h3>Prix Moyen (FCFA)</h3><p>{prix_moyen:,.0f}</p></div>', unsafe_allow_html=True)

        # Nombre d'annonces
        nombre_annonces = data.shape[0]
        with col2:
            st.markdown(f'<div class="metric-box"><h3>Nombre d\'Annonces</h3><p>{nombre_annonces:,}</p></div>', unsafe_allow_html=True)


        # 🌟 Graphique 1 : Distribution des prix
        if "Prix" in data.columns:
            data["Prix"] = pd.to_numeric(data["Prix"], errors="coerce").fillna(0).astype(int)
            fig1 = px.histogram(data, x="Prix", title="Distribution des Prix des Climatiseurs", nbins=20)
            st.plotly_chart(fig1, use_container_width=True)

        # 🌟 Graphique 2 : Nombre d'annonces par zone géographique
        if "Adresse" in data.columns:
            zone_counts = data["Adresse"].value_counts().reset_index()
            zone_counts.columns = ["Zone", "Nombre d'Annonces"]
            fig2 = px.bar(zone_counts, x="Zone", y="Nombre d'Annonces", title="Nombre d'Annonces par Zone")
            st.plotly_chart(fig2, use_container_width=True)

            prix_moyen_par_zone = data.groupby("Adresse")["Prix"].mean().reset_index()
            prix_moyen_par_zone.columns = ["Zone", "Prix Moyen"]

            # Graphique des prix moyens par zone
            fig_prix_moyen = px.bar(prix_moyen_par_zone, 
                                     x="Zone", y="Prix Moyen", 
                                     title="Distribution du Prix Moyen par Zone", 
                                     labels={"Zone": "Zones", "Prix Moyen": "Prix Moyen (FCFA)"})
            st.plotly_chart(fig_prix_moyen, use_container_width=True)

        # 🌟 Graphique 3 : Répartition des états des climatiseurs
        if "Etat_Clim" in data.columns:
            fig3 = px.pie(data, names="Etat_Clim", title="Répartition des États des Climatiseurs")
            st.plotly_chart(fig3, use_container_width=True)

        # 💾 Téléchargement des données
        csv_data = data.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Télécharger les données en CSV", csv_data, "data_dashboard.csv", "text/csv")
    else:
        st.info("📉 Aucune donnée disponible pour la visualisation.")

# --- Évaluation ---
if menu == "📝 Évaluation":
    st.header("Formulaire d'Évaluation 📝")
    st.image(evaluation_img, caption="Donnez-nous votre avis !", use_column_width=True)

    note = st.slider("Quelle note donnez-vous à l'application ?", min_value=1, max_value=5, value=3)
    commentaire = st.text_area("Commentaires supplémentaires")

    if st.button("✅ Soumettre l'évaluation"):
        with st.spinner("Enregistrement de votre évaluation..."):
            time.sleep(2)
        st.success("Merci pour votre évaluation ! 🎉")
        st.write(f"Note attribuée : {note} ⭐")
        st.write(f"Commentaire : {commentaire}")

# Charger des Données Scrapées
elif menu == "📥 Charger des Données Scrapées":
    st.header("📥 Charger des Données Scrapées")

    uploaded_file = st.file_uploader("Téléchargez votre fichier CSV :", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("✅ Fichier chargé avec succès !")
        st.write("Aperçu des données :")
        st.dataframe(df)
        
        # Option d'analyse rapide
        if st.checkbox("Afficher une analyse rapide"):
            st.write(df.describe())

        # Graphiques optionnels
        if st.checkbox("Afficher un graphique de distribution des prix"):
            fig = px.histogram(df, x="Prix", title="Distribution des Prix")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📂 Veuillez charger un fichier CSV.")





st.markdown(
    """
    <div style='text-align: center; margin-top: 100px; font-size: 14px; color: gray;'>
        @ Développé par <strong>Ousmane SOW</strong> - 2025
    </div>
    """,
    unsafe_allow_html=True,
)
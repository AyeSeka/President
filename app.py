import streamlit as st
import pickle
import numpy as np

# Charger le pipeline complet
with open('model/model2.pkl', 'rb') as file:
    pipeline = pickle.load(file)

# Injecter du CSS personnalisé pour styliser l'interface
st.markdown("""
    <style>
        @font-face {
            font-family: 'AptosDisplay';
            src: url('fonts/AptosDisplay-Regular.ttf') format('truetype');
        }
        html, body, .main {
            font-family: 'AptosDisplay', sans-serif;
            background-color: #f5f5f5;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #1f77b4;
            font-family: 'AptosDisplay', sans-serif;
        }
        p, div, span, input, textarea, select, button {
            color: #333333;
            font-family: 'AptosDisplay', sans-serif;
            font-size: 18px;
            line-height: 1.6;
        }
        .stButton>button {
            color: white;
            background-color: #1f77b4;
            border-radius: 8px;
            padding: 15px 30px;
            font-family: 'AptosDisplay', sans-serif;
            font-size: 20px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #125688;
        }
        .stSidebar .markdown {
            color: #FFFFFF !important;
        }

        /* CSS spécifique pour l'effet de curseur hésitant */
        .decision-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: relative;
            width: 440px;
            margin: 0 auto;
            margin-bottom: 40px;
        }
        .decision-container img {
            width: 200px;
            height: 200px;
            object-fit: cover;
            border-radius: 10px;
            transition: transform 0.2s ease-in-out;
        }
        .cursor {
            width: 40px;
            height: 40px;
            background-color: red;
            border-radius: 50%;
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            animation: move 2s infinite;
        }
        @keyframes move {
            0% { left: 0; }
            50% { left: calc(100% - 40px); }
            100% { left: 0; }
        }
    </style>
    """, unsafe_allow_html=True)


# Insérer l'image et le titre dans la sidebar
with st.sidebar:
    st.image("télécharger.jpeg", use_column_width=True)
    st.title('Prédiction de l\'Élection Présidentielle aux USA')
    st.markdown("""
    ### Description
    Ce tableau de bord vous permet de prédire les résultats des élections présidentielles aux États-Unis en fonction de divers paramètres locaux. 
    Les prédictions sont basées sur des données historiques et sont calculées à l'échelle locale avant d'être agrégées pour une vue globale.
    """)

# Ajouter la question avec les images
st.markdown("## Qui de Donald Trump représentant des Républicains ou de Hillary Clinton représentante des Démocrates va gagner?")

# Conteneur pour les images et le curseur
st.markdown("""
<div class="decision-container">
    <img src="https://th.bing.com/th/id/OIP.X3eKtUPMP4ttfLrZAmlSOgHaE-?w=269&h=180&c=7&r=0&o=5&dpr=1.5&pid=1.7" alt="Donald Trump">
    <img src="https://th.bing.com/th/id/OIP.9666zveJhCn7no9CcRp0cAHaK5?w=115&h=180&c=7&r=0&o=5&dpr=1.5&pid=1.7" alt="Hillary Clinton">
    <div class="cursor"></div>
</div>
""", unsafe_allow_html=True)

# Champs d'input dans la partie principale
st.header("Paramètres d'Entrée")

col1, col2 = st.columns(2)

with col1:
    Civilian_labor_force_2017 = st.number_input('Population active civile 2017', min_value=0.0, step=1.0)
    Unemployment_rate_2014 = st.number_input('Taux de chômage 2014', min_value=0.0, step=0.1)
    Percent_high_school_diploma_1970 = st.number_input('Pourcentage d\'adultes ayant seulement un diplôme d\'études secondaires, 1970', min_value=0.0, step=0.1)
    Percent_high_school_diploma_1990 = st.number_input('Pourcentage d\'adultes ayant seulement un diplôme d\'études secondaires, 1990', min_value=0.0, step=0.1)
    R_DOMESTIC_MIG_2013 = st.number_input('Migration intérieure 2013', min_value=0.0, step=1.0)
    R_DOMESTIC_MIG_2011 = st.number_input('Migration intérieure 2011', min_value=0.0, step=1.0)

with col2:
    Urban_Influence_Code_2013 = st.number_input('Code de l\'influence urbaine 2013', min_value=0.0, step=1.0)
    Percent_college_associate_degree_2000 = st.number_input('Pourcentage d\'adultes ayant obtenu un diplôme d\'études collégiales ou d\'études supérieures, 2000', min_value=0.0, step=0.1)
    Percent_college_1_3_years_1970 = st.slider('Pourcentage d\'adultes ayant terminé leurs études collégiales (1 à 3 ans), 1970', 0.0, 100.0, step=0.1)
    R_NET_MIG_2016 = st.number_input('Migration nette 2016', min_value=0.0, step=1.0)
    R_NET_MIG_2014 = st.number_input('Migration nette 2014', min_value=0.0, step=1.0)
    R_NET_MIG_2015 = st.number_input('Migration nette 2015', min_value=0.0, step=1.0)

# Centrer le bouton de prédiction
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Bouton de prédiction
    if st.button('🔮 Prédire'):
        # Vérifier si toutes les valeurs sont remplies
        if any(val is None or val == 0 for val in [
            Civilian_labor_force_2017,
            Unemployment_rate_2014,
            Percent_high_school_diploma_1970,
            Urban_Influence_Code_2013,
            Percent_college_associate_degree_2000,
            Percent_college_1_3_years_1970,
            Percent_high_school_diploma_1990,
            R_DOMESTIC_MIG_2013,
            R_DOMESTIC_MIG_2011,
            R_NET_MIG_2016,
            R_NET_MIG_2014,
            R_NET_MIG_2015
        ]):
            st.error("Veuillez remplir toutes les valeurs avant de prédire.")
        else:
            # Créer un numpy array avec les valeurs d'entrée
            input_data = np.array([
                Civilian_labor_force_2017,
                Unemployment_rate_2014,
                Percent_high_school_diploma_1970,
                Urban_Influence_Code_2013,
                Percent_college_associate_degree_2000,
                Percent_college_1_3_years_1970,
                Percent_high_school_diploma_1990,
                R_DOMESTIC_MIG_2013,
                R_DOMESTIC_MIG_2011,
                R_NET_MIG_2016,
                R_NET_MIG_2014,
                R_NET_MIG_2015
            ]).reshape(1, -1)

            # Faire la prédiction des probabilités
            proba = pipeline.predict_proba(input_data)[0]

            # Déterminer le parti avec la probabilité la plus élevée
            if proba[1] > proba[0]:
                result_text = f"Les Républicains vont gagner avec une prédiction de {proba[1]*100:.2f}%"
                image_path = "trump.jpeg"  # Remplacez par le chemin ou l'URL de l'image de Trump
            else:
                result_text = f"Les Démocrates vont gagner avec une prédiction de {proba[0]*100:.2f}%"
                image_path = "hillary.jpeg"  # Remplacez par le chemin ou l'URL de l'image de Hillary

            # Afficher le résultat dans le contenu principal
            st.header("Votre Résultat de Prédiction")
            st.success(result_text)
            st.image(image_path, use_column_width=True)

# Pour exécuter l'application Streamlit
# Utilisez la commande suivante dans le terminal:
# streamlit run app.py

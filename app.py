import streamlit as st
import pandas as pd
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Dashboard", layout="wide")

df_users = pd.read_csv("users.csv")

credentials = {
    "usernames": {
        row["name"]: {
            "name": row["name"],
            "password": row["password"],
            "email": row["email"],
            "failed_login_attempts": row["failed_login_attempts"],
            "logged_in": row["logged_in"],
            "role": row["role"]
        }
        for _, row in df_users.iterrows()
    }
}


authenticator = Authenticate(
    credentials,
    "cookie_name",
    "cookie_key",
    30
)

authenticator.login()

name = st.session_state.get("name")
authentication_status = st.session_state.get("authentication_status")
username = st.session_state.get("username")


if authentication_status:

    with st.sidebar:
        st.success(f"Bienvenue {name} 👋")

        selected = option_menu(
            menu_title=None,
            options=["Accueil", "Photos de mon chien"],
            icons=["house", "image"],
            default_index=0
        )

        authenticator.logout("Déconnexion", "sidebar")

    if selected == "Accueil":
        st.title("Bienvenue sur ma page !")
        st.image(
            "IMG_6762.jpeg",
            use_container_width=True
        )

    elif selected == "Photos de mon chien":
        st.title("Album photo du plus beau du monde : Aiko")

        images = [
            "IMG_6788.JPG",
            "IMG_6996.jpeg",
            "IMG_7031.JPG"
        ]

        cols = st.columns(3)
        for col, img in zip(cols, images):
            col.image(img, use_container_width=True)

elif authentication_status is False:
    st.error("Nom d'utilisateur ou mot de passe incorrect")

elif authentication_status is None:
    st.warning("Veuillez entrer vos identifiants, id : root, mdp : rootMDP")

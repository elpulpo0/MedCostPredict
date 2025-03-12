import streamlit as st
from utils import authenticate_user, create_user


def login_page():
    """Affiche la page de connexion et d'inscription."""
    st.title("Bienvenue sur MedCostPredict")

    tab1, tab2 = st.tabs(["Connexion", "Créer un compte"])

    # 🔹 Connexion
    with tab1:
        st.subheader("Connexion")
        email = st.text_input("Email", key="login_email")
        password = st.text_input(
            "Mot de passe", type="password", key="login_password"
        )
        login_btn = st.button("Se connecter")

        if login_btn:
            user = authenticate_user(email, password)
            if user:
                st.session_state["authenticated"] = True
                st.session_state["role"] = user["role"]
                st.session_state["token"] = user["token"]
                st.rerun()
            else:
                st.error("Identifiants incorrects")

    # 🔹 Inscription
    with tab2:
        st.subheader("Créer un compte")

        full_name = st.text_input("Nom complet", key="signup_name")
        signup_email = st.text_input("Email", key="signup_email")

        # 🔹 Ajout du champ de confirmation du mot de passe
        signup_password = st.text_input(
            "Mot de passe", type="password", key="signup_password"
        )
        confirm_password = st.text_input(
            "Confirmer le mot de passe", type="password", key="confirm_password"
        )

        signup_btn = st.button("S'inscrire")

        if signup_btn:
            # ✅ Vérification que les deux mots de passe correspondent
            if signup_password != confirm_password:
                st.error("❌ Les mots de passe ne correspondent pas.")
            else:
                success, message = create_user(
                    full_name, signup_email, signup_password
                )
                if success:
                    st.success(
                        "✅ Compte créé avec succès ! Vous pouvez maintenant vous connecter."
                    )
                else:
                    st.error(f"❌ Erreur : {message}")

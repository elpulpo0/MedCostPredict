import streamlit as st


def home_page():
    """Affiche la page principale après connexion."""
    st.title("🏠 Bienvenue sur MedCostPredict")
    st.write(
        "🔹 Sélectionnez une section dans la barre latérale pour commencer."
    )

    # 🔹 Affichage de la page sélectionnée
    if st.session_state["role"] == "admin":
        st.write("✅ Vous avez un accès administrateur.")

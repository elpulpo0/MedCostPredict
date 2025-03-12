import streamlit as st
from utils import get_patients


def patients_page():
    """Affiche la liste des patients."""
    st.title("Données des patients")

    patients = get_patients(st.session_state["token"])

    if not patients:
        st.warning("Aucune donnée de patient disponible.")
        return

    for patient in patients:
        st.write("**Nom** : Non disponible (anonymisé)")
        st.write("**Âge** : ", patient["age"])
        
        # 🔹 Sexe du patient
        sexe = "Femme" if patient["sex"] == 1 else "Homme"
        st.write(f"**Sexe** : {sexe}")

        # 🔹 IMC (Indice de Masse Corporelle)
        st.write(f"**Indice de Masse Corporelle (IMC)** : {patient['bmi']}")

        # 🔹 Nombre d'enfants
        enfants = "Oui" if patient["children"] > 0 else "Non"
        st.write(f"**Le patient a-t-il des enfants ?** : {enfants} ({patient['children']} enfant(s))")

        # 🔹 Fumeur ou non
        fumeur = "Oui" if patient["smoker"] == 1 else "Non"
        st.write(f"**Fumeur** : {fumeur}")

        # 🔹 Région
        st.write(f"**Région** : {patient['region']}")

        # 🔹 Charges médicales
        st.write(f"**Coût des soins médicaux** : {patient['charges']} €")

        st.write("---")

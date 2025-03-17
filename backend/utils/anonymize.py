import pandas as pd
import hashlib
from loguru import logger
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from dotenv import load_dotenv
import os
import base64


# Charger la clé secrète depuis le fichier .env
load_dotenv()
SECRET_KEY = bytes(
    os.getenv("SECRET_KEY", "").encode("utf-8")
)  # Assurez-vous d'avoir une clé secrète de 32 octets


# Fonction pour anonymiser un nom ou un prénom via hachage SHA256
def anonymize(name: str) -> str:
    """Hache un nom ou un prénom avec SHA256 pour anonymiser l'information."""
    return hashlib.sha256(name.encode("utf-8")).hexdigest()


# Fonction pour chiffrer un mot de passe
def encrypt_word(word: str) -> str:
    """Chiffre un mot de passe avec AES."""
    # Crée un padding pour que la taille soit multiple de 16 octets
    padder = padding.PKCS7(128).padder()
    padded_word = padder.update(word.encode()) + padder.finalize()

    # Génère un vecteur d'initialisation (IV) aléatoire
    iv = os.urandom(16)

    # Crée un cipher AES avec la clé et l'IV
    cipher = Cipher(
        algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend()
    )
    encryptor = cipher.encryptor()

    # Chiffre le mot de passe
    encrypted_word = (
        encryptor.update(padded_word) + encryptor.finalize()
    )

    # Retourner le mot de passe chiffré encodé en base64 pour faciliter l'enregistrement
    return base64.b64encode(iv + encrypted_word).decode("utf-8")


# Fonction pour déchiffrer un mot de passe
def decrypt_word(encrypted_word: str) -> str:
    """Déchiffre un mot de passe avec AES."""
    # Décode le mot de passe chiffré depuis base64
    encrypted_word_bytes = base64.b64decode(encrypted_word)

    # Extraire l'IV et le mot de passe chiffré
    iv = encrypted_word_bytes[:16]
    encrypted_word = encrypted_word_bytes[16:]

    # Crée un cipher AES avec la clé et l'IV
    cipher = Cipher(
        algorithms.AES(SECRET_KEY), modes.CBC(iv), backend=default_backend()
    )
    decryptor = cipher.decryptor()

    # Déchiffrer le mot de passe
    padded_word = (
        decryptor.update(encrypted_word) + decryptor.finalize()
    )

    # Enlever le padding
    unpadder = padding.PKCS7(128).unpadder()
    word = unpadder.update(padded_word) + unpadder.finalize()

    return word.decode("utf-8")


def anonymize_names(input_csv, output_csv):
    """Ajoute les colonnes name et surname à un fichier CSV."""
    try:
        df = pd.read_csv(input_csv)

        # Appliquer l'anonymisation aux colonnes 'name' et 'surname'
        df["name"] = df["name"].apply(anonymize)
        df["surname"] = df["surname"].apply(anonymize)

        df.to_csv(output_csv, index=False)

        logger.info(
            f"✅ Fichier anonymisé et mots de passe chiffrés enregistré à : {output_csv}"
        )

    except Exception as e:
        logger.error(f"❌ Erreur lors de l'ajout des colonnes : {e}")
        raise

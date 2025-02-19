import hashlib

# Fonction pour anonymiser un nom ou un prénom via hachage SHA256
def anonymize_name(name: str) -> str:
    """Hache un nom ou un prénom avec SHA256 pour anonymiser l'information."""
    return hashlib.sha256(name.encode("utf-8")).hexdigest()

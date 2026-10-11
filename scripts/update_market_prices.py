"""
Script d'actualisation des cotes de marché PopDex.
Exécuté de manière autonome chaque semaine via GitHub Actions.
"""
import json
import os
import sys
from datetime import datetime, timezone

PRICES_FILE = os.path.join(os.path.dirname(__file__), "..", "prices.json")

def main():
    if not os.path.exists(PRICES_FILE):
        print(f"Error: {PRICES_FILE} not found", file=sys.stderr)
        sys.exit(1)

    print("Chargement des cotes actuelles...")
    with open(PRICES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Vérification d'intégrité de la structure
    if "hardware" not in data or "games" not in data:
        print("Error: Invalid schema", file=sys.stderr)
        sys.exit(1)

    consoles_count = len(data["hardware"])
    games_count = len(data["games"])
    print(f"Structure valide: {consoles_count} consoles, {games_count} jeux référencés.")

    # Mise à jour de l'horodatage
    now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    data["updated_at"] = now_iso
    data["version"] = data.get("version", 1) + 1

    # Écriture du fichier rafraîchi
    with open(PRICES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(',', ':'))

    print(f"Actualisation réussie avec succès (version {data['version']}, timestamp {now_iso}).")

if __name__ == "__main__":
    main()

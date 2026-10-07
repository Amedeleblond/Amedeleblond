import os
import json
import requests
from bs4 import BeautifulSoup

# Remplacez par votre nom d'utilisateur si nécessaire, mais ici c'est déjà configuré
USERNAME = "Amedeleblond"
URL = f"https://github.com/users/{USERNAME}/contributions"

def fetch_data():
    print(f"Récupération des données pour {USERNAME}...")
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # GitHub utilise des balises <td> avec la classe 'ContributionCalendar-day'
    days = soup.find_all('td', class_='ContributionCalendar-day')
    
    data = []
    for day in days:
        date = day.get('data-date')
        level = day.get('data-level')
        if date and level is not None:
            data.append({"date": date, "level": int(level)})
    
    # Créer le dossier data s'il n'existe pas
    os.makedirs('data', exist_ok=True)
    
    # Sauvegarder en JSON
    with open('data/contributions.json', 'w') as f:
        json.dump(data, f)
        
    print(f"Succès : {len(data)} jours de contributions sauvegardés dans data/contributions.json")

if __name__ == "__main__":
    fetch_data()

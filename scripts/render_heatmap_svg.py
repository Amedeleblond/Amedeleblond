import json
import math

# Couleurs du thème GitHub (du plus sombre au plus clair/vert)
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_svg():
    try:
        with open('data/contributions.json', 'r') as f:
            days = json.load(f)
    except FileNotFoundError:
        print("Erreur : data/contributions.json introuvable.")
        return

    box_size = 10
    gap = 3
    cols = math.ceil(len(days) / 7)
    
    # Calculer la taille totale de l'image
    svg_w = cols * (box_size + gap) + 40
    svg_h = 7 * (box_size + gap) + 40
    
    svg_content = [
        f'<svg width="{svg_w}" height="{svg_h}" xmlns="http://www.w3.org/2000/svg">',
        '  <style>',
        '    @keyframes slideDown {',
        '      0% { opacity: 0; transform: translateY(-10px); }',
        '      100% { opacity: 1; transform: translateY(0); }',
        '    }',
        '  </style>',
        '  <rect width="100%" height="100%" fill="#0d1117" rx="8" />',
        '  <g transform="translate(20, 20)">'
    ]
    
    for i, day in enumerate(days):
        col = i // 7
        row = i % 7
        x = col * (box_size + gap)
        y = row * (box_size + gap)
        
        # Sécurité pour ne pas dépasser la taille de la palette
        level = min(day['level'], len(PALETTE) - 1)
        color = PALETTE[level]
        
        # L'animation se déclenche en diagonale (décalage basé sur la colonne et la ligne)
        delay = (col * 0.04) + (row * 0.04)
        
        rect = f'    <rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2" fill="{color}" style="opacity:0; animation: slideDown 0.5s ease-out {delay}s forwards;" />'
        svg_content.append(rect)
        
    svg_content.append('  </g>')
    svg_content.append('</svg>')
    
    with open('contrib-heatmap.svg', 'w') as f:
        f.write("\n".join(svg_content))
        
    print("Graphique généré : contrib-heatmap.svg")

if __name__ == "__main__":
    render_svg()

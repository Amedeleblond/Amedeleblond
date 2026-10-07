import os

def generate_info_card():
    static_mode = os.environ.get("STATIC", "0") == "1"
    
    # Vos informations
    title = "amedeleblond@github ~ $ neofetch"
    rows = [
        ("Role",  "Software Engineering student @ Atlas Univ"),
        ("Focus", "ASP.NET Core, Entity Framework & Cyber Security"),
        ("Stack", "C#, Python, Java, React, Node.js, Docker"),
        ("Quirk", "I burst out laughing when faced with difficulties")
    ]
    
    svg_content = [
        '<svg width="490" height="220" xmlns="http://www.w3.org/2000/svg">',
        '  <style>',
        '    .text { font-family: "Courier New", monospace; font-size: 14px; fill: #c9d1d9; }',
        '    .key { fill: #e36209; font-weight: bold; }',
        '    .title { fill: #e36209; font-weight: bold; }',
        '    @keyframes print {',
        '      0% { opacity: 0; transform: translateX(-10px); }',
        '      100% { opacity: 1; transform: translateX(0); }',
        '    }',
        '  </style>',
        '  <rect width="100%" height="100%" fill="#0d1117" rx="8" />',
        f'  <text x="20" y="40" class="text title">{title}</text>',
        '  <line x1="20" y1="50" x2="470" y2="50" stroke="#30363d" stroke-width="1" />'
    ]

    y_offset = 80
    delay = 0.3

    for key, value in rows:
        anim_style = "" if static_mode else f'style="opacity: 0; animation: print 0.4s ease-out {delay}s forwards;"'
        
        line = f"""
        <g {anim_style}>
            <text x="20" y="{y_offset}" class="text key">{key}</text>
            <text x="90" y="{y_offset}" class="text"> {value}</text>
        </g>
        """
        svg_content.append(line)
        y_offset += 30
        delay += 0.2

    svg_content.append('</svg>')

    with open("info-card.svg", "w") as f:
        f.write("\n".join(svg_content))

if __name__ == "__main__":
    generate_info_card()

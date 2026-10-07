import os
from PIL import Image

# Échelle de densité : du plus clair (espace) au plus sombre (@)
RAMP = " .`:-=+*cs#%@" 

def make_ascii_svg(input_path="source-prepped.png", output_path="avi-ascii.svg"):
    try:
        img = Image.open(input_path).convert('L')
    except FileNotFoundError:
        return

    target_w, target_h = 100, 53 
    img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
    pixels = img.load()

    lines = []
    for y in range(target_h):
        line_chars = []
        for x in range(target_w):
            brightness = pixels[x, y]
            ramp_index = int((255 - brightness) / 255 * (len(RAMP) - 1))
            char = RAMP[ramp_index]
            
            # Échapper les caractères XML
            if char == '<': char = '&lt;'
            elif char == '>': char = '&gt;'
            elif char == '&': char = '&amp;'
            
            line_chars.append(char)
        lines.append("".join(line_chars))

    svg_w, svg_h = 370, 220
    font_size = 4
    char_height = 4.15
    
    svg_content = [
        f'<svg width="{svg_w}" height="{svg_h}" xmlns="http://www.w3.org/2000/svg">',
        '  <style>',
        '    .ascii { font-family: "Courier New", monospace; font-size: ' + str(font_size) + 'px; fill: #8b949e; white-space: pre; }',
        '  </style>',
        '  <rect width="100%" height="100%" fill="#0d1117" />',
        '  <g class="ascii">'
    ]

    delay_step = 0.03
    for i, text_line in enumerate(lines):
        y_pos = (i + 1) * char_height
        start_time = i * delay_step
        
        # Animation ligne par ligne
        clip_path = f"""
        <clipPath id="clip{i}">
            <rect x="0" y="{y_pos - char_height}" width="0" height="{char_height + 2}">
                <animate attributeName="width" from="0" to="{svg_w}" begin="{start_time}s" dur="0.5s" fill="freeze" />
            </rect>
        </clipPath>
        """
        
        svg_content.append(clip_path)
        svg_content.append(f'    <text x="5" y="{y_pos}" clip-path="url(#clip{i})">{text_line}</text>')

    svg_content.append('  </g>')
    svg_content.append('</svg>')

    with open(output_path, "w") as f:
        f.write("\n".join(svg_content))

if __name__ == "__main__":
    make_ascii_svg()

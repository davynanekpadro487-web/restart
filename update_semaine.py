import re

with open('templates/core/defi.html', 'r', encoding='utf-8') as f:
    defi = f.read()

domain_styles = """
  <style>
  .domains-grid{
    display:grid; grid-template-columns:repeat(3,1fr); gap:20px; margin-bottom:40px; scroll-margin-top: 100px;
  }
  .domain-card{
    background:var(--white); border-radius:14px;
    padding:22px; box-shadow:0 4px 18px rgba(13,27,76,0.08);
    display:flex; flex-direction:column; gap:14px;
    transition:transform .2s ease, box-shadow .2s ease;
    text-decoration:none;
  }
  .domain-card:hover{ transform:translateY(-3px); box-shadow:0 10px 24px rgba(13,27,76,0.12); }
  .domain-card.optional{ grid-column:1 / 2; }
  .domain-top{ display:flex; align-items:flex-start; gap:14px; }
  .domain-icon{
    width:46px; height:46px; border-radius:50%;
    display:flex; align-items:center; justify-content:center; flex-shrink:0;
  }
  .domain-icon svg{ width:22px; height:22px; }
  .domain-info h4{ font-family:'Poppins',sans-serif; font-weight:700; font-size:15.5px; margin-bottom:4px; color:var(--bleu-nuit);}
  .domain-info p{ font-size:12.5px; color:var(--gris-texte); line-height:1.5; margin:0;}
  .optional-badge{
    display:inline-block; font-family:'Poppins',sans-serif; font-size:10px; font-weight:700;
    letter-spacing:.04em; text-transform:uppercase; color:var(--bleu-profond);
    background:#eaf2ff; padding:4px 10px; border-radius:999px; margin-bottom:6px;
  }

  .domain-status-row{ display:flex; align-items:center; justify-content:space-between; margin-top:auto;}
  .status-done-tag{ display:flex; align-items:center; gap:6px; font-size:13px; font-weight:600; color:#1f9d55; }
  .status-todo-tag{ display:flex; align-items:center; gap:6px; font-size:13px; font-weight:600; color:var(--gris-texte); }
  @media (max-width:960px){
    .domains-grid{ grid-template-columns:1fr; }
    .domain-card.optional{ grid-column:auto; }
  }
  </style>
"""

grid_match = re.search(r'<div class="domains-grid" id="domains-grid">.*?</div>\s*</div> <!-- End of tab-cette-semaine -->', defi, re.DOTALL)
grid_html = grid_match.group(0).replace('</div> <!-- End of tab-cette-semaine -->', '') if grid_match else ''

with open('templates/core/semaine_complete.html', 'r', encoding='utf-8') as f:
    sc = f.read()

sc = re.sub(r'<!-- Domaines Terminés -->.*?<!-- Invitation Journal Bilan -->', 
            f'<!-- Domaines Terminés -->\\n{domain_styles}\\n<div class="max-w-4xl mx-auto mb-16 text-left">\\n<h3 class="text-2xl font-bold text-gray-900 mb-6 px-2">Tes réalisations</h3>\\n{grid_html}\\n</div>\\n<!-- Invitation Journal Bilan -->', 
            sc, flags=re.DOTALL)

with open('templates/core/semaine_complete.html', 'w', encoding='utf-8') as f:
    f.write(sc)
print("Updated")

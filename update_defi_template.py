import re

html_content = """{% extends 'base.html' %}
{% load static %}

{% block content %}
<style>
  .img-placeholder{
    width:100%; height:100%; min-height:100px;
    background:
      repeating-linear-gradient(45deg,
        rgba(13,27,76,0.05), rgba(13,27,76,0.05) 10px,
        rgba(13,27,76,0.09) 10px, rgba(13,27,76,0.09) 20px);
    border:1.5px dashed rgba(13,27,76,0.25);
    border-radius:inherit;
    display:flex; align-items:center; justify-content:center;
    text-align:center; padding:10px;
    font-family:'Inter',sans-serif; font-size:11px; font-weight:600;
    letter-spacing:.03em; text-transform:uppercase;
    color:rgba(13,27,76,0.55);
  }

  main.page-defis-main { max-width:1240px; margin:0 auto; padding:40px 48px 80px; }

  .page-head h1{ font-family:'Poppins',sans-serif; font-weight:800; font-size:34px; margin-bottom:6px; color:var(--bleu-nuit); }
  .page-head p{ color:var(--gris-texte); font-size:15px; margin-bottom:24px; }

  .tabs{ display:flex; gap:12px; margin-bottom:28px; }
  .tab{ font-family:'Poppins',sans-serif; font-weight:600; font-size:14px; padding:11px 22px; border-radius:999px; border:1.5px solid rgba(26,79,180,0.18); background:var(--white); color:var(--bleu-nuit); cursor:pointer; }
  .tab.active{ background:var(--bleu-profond); color:var(--white); border-color:var(--bleu-profond); }

  /* HERO STATUS BANNER */
  .status-banner{
    border-radius:20px;
    padding:36px 40px;
    display:grid;
    grid-template-columns:auto 1fr auto;
    align-items:center;
    gap:32px;
    margin-bottom:40px;
    box-shadow:0 4px 18px rgba(13,27,76,0.08);
  }
  .status-banner.state-todo{ background:linear-gradient(120deg,#eaf2ff,#dcebff); }
  .status-banner.state-done{ background:linear-gradient(120deg,#e6f8ed,#d7f5e3); }

  .status-icon{
    width:120px; height:120px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    flex-shrink:0; overflow:hidden;
  }
  .state-todo .status-icon{ background:rgba(26,79,180,0.08); }
  .state-done .status-icon{ background:rgba(31,157,85,0.12); }
  .status-icon img{ width: 100%; height: 100%; object-fit: contain; }

  .status-text h2{
    font-family:'Poppins',sans-serif; font-weight:800; font-size:26px;
    display:flex; align-items:center; gap:10px; margin-bottom:8px;
  }
  .state-todo .status-text h2{ color:var(--bleu-nuit); }
  .state-done .status-text h2{ color:#177a41; }
  .status-text p{ color:var(--gris-texte); font-size:14.5px; margin-bottom:18px; max-width:420px; }

  .xp-badge{
    display:inline-flex; align-items:center; gap:8px;
    background:rgba(245,166,35,0.15); color:#c9860a;
    font-family:'Poppins',sans-serif; font-weight:700; font-size:13px;
    padding:8px 16px; border-radius:999px; margin-bottom:18px;
  }

  .status-progress{ min-width:260px; }
  .progress-label{ display:flex; justify-content:space-between; font-size:13px; font-weight:600; margin-bottom:8px; color:var(--bleu-nuit); }
  .progress-bar-track{ width:100%; height:9px; border-radius:999px; background:rgba(13,27,76,0.1); overflow:hidden; margin-bottom:14px; }
  .progress-bar-fill{ height:100%; border-radius:999px; }
  .state-todo .progress-bar-fill{ background:linear-gradient(90deg,#4a90d9,#1a4fb4); }
  .state-done .progress-bar-fill{ background:linear-gradient(90deg,#38c46f,#1f9d55); }
  .domain-count{
    display:flex; align-items:center; gap:8px;
    background:var(--white); border-radius:10px;
    padding:12px 16px; font-size:13.5px; font-weight:600;
  }
  .state-done .domain-count{ color:#177a41; }
  .state-todo .domain-count{ color:var(--bleu-profond); }

  /* DOMAINS SECTION */
  .domains-head{
    display:flex; align-items:center; justify-content:space-between;
    margin-bottom:18px; flex-wrap:wrap; gap:12px;
  }
  .domains-head h3{ font-family:'Poppins',sans-serif; font-weight:700; font-size:19px; color:var(--bleu-nuit);}
  .info-chip{
    display:flex; align-items:center; gap:8px;
    font-size:13px; font-weight:500; padding:9px 16px; border-radius:999px;
  }
  .state-todo .info-chip{ background:#eaf2ff; color:var(--bleu-profond); }
  .state-done .info-chip{ background:#e6f8ed; color:#177a41; }

  .domains-grid{
    display:grid; grid-template-columns:repeat(3,1fr); gap:20px; margin-bottom:40px;
  }
  .domain-card{
    background:var(--white); border-radius:14px;
    padding:22px; box-shadow:0 4px 18px rgba(13,27,76,0.08);
    display:flex; flex-direction:column; gap:14px;
    transition:transform .2s ease, box-shadow .2s ease;
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

  /* HELP CARD */
  .help-card{
    background:var(--white); border-radius:20px;
    display:grid; grid-template-columns:260px 1fr auto;
    align-items:center; gap:28px; padding:26px 32px; box-shadow:0 4px 18px rgba(13,27,76,0.08);
  }
  .help-card .thumb{ height:110px; border-radius:10px; overflow:hidden; }
  .help-card .thumb img { width: 100%; height: 100%; object-fit: contain; }
  .help-card h3{ font-family:'Poppins',sans-serif; font-weight:700; font-size:19px; margin-bottom:6px; color:var(--bleu-nuit);}
  .help-card p{ font-size:14px; color:var(--gris-texte); line-height:1.5; margin:0; }

  @media (max-width:960px){
    main.page-defis-main{ padding:28px 20px 60px; }
    .status-banner{ grid-template-columns:1fr; text-align:center; }
    .status-icon{ margin:0 auto; }
    .domains-grid{ grid-template-columns:1fr; }
    .domain-card.optional{ grid-column:auto; }
    .help-card{ grid-template-columns:1fr; text-align:left; }
  }
</style>

<main class="page-defis-main">

  <div class="page-head">
    <h1>Mes défis</h1>
    <p>Relève des défis chaque semaine et deviens la meilleure version de toi-même.</p>
  </div>

  <div class="tabs">
    <button class="tab active">Cette semaine</button>
  </div>

  {% if semaine_terminee %}
  <!-- ============ ÉTAT : TERMINÉ ============ -->
  <section class="status-banner state-done">
    <div class="status-icon">
      <img src="{% static 'images/defis/illu-defi-termine.png' %}" alt="Défi terminé">
    </div>
    <div class="status-text">
      <h2>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="#1f9d55" stroke-width="2"/><path d="M8 12L11 15L16 9" stroke="#1f9d55" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        Félicitations, {{ user.username|default:"Soso" }} ! Défi de la semaine terminé
      </h2>
      <p>
      {% if spiritualite_terminee %}
      Tu as complété les 7 domaines.
      {% else %}
      Tu as complété les 6 domaines essentiels.
      {% endif %}
      </p>
      <div class="xp-badge">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 2L14.5 8.5L21 9L16 13.5L17.5 20L12 16.5L6.5 20L8 13.5L3 9L9.5 8.5L12 2Z" fill="#c9860a"/></svg>
        +50 XP bonus
      </div>
      <br>
      <a href="{% url 'semaine_complete' semaine.id %}" class="btn btn-vert" style="display:inline-flex;">
        Voir mes réalisations
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M5 12H19M19 12L13 6M19 12L13 18" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </a>
    </div>
    <div class="status-progress">
      <div class="progress-label"><span>Progression globale</span><span>{{ prog_percent }}%</span></div>
      <div class="progress-bar-track"><div class="progress-bar-fill" style="width:{{ prog_percent }}%"></div></div>
      <div class="domain-count">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none"><rect x="3" y="5" width="18" height="16" rx="2" stroke="currentColor" stroke-width="2"/><path d="M8 3V7M16 3V7M3 10H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
        {{ prog_count }} / {{ prog_max }} domaines terminés
      </div>
    </div>
  </section>
  {% else %}
  <!-- ============ ÉTAT : À COMMENCER / EN COURS ============ -->
  <section class="status-banner state-todo">
    <div class="status-icon">
      <img src="{% static 'images/defis/illu-defi-objectif.png' %}" alt="Objectif">
    </div>
    <div class="status-text">
      <h2>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none"><path d="M12 2L14.5 8.5L21 9L16 13.5L17.5 20L12 16.5L6.5 20L8 13.5L3 9L9.5 8.5L12 2Z" stroke="#f5a623" stroke-width="1.8" stroke-linejoin="round"/></svg>
        {% if prog_count == 0 %}
        Ton défi de la semaine t'attend !
        {% else %}
        Continue ton défi de la semaine !
        {% endif %}
      </h2>
      <p>
        {% if prog_count == 0 %}
        Commence dès maintenant et progresse domaine par domaine.
        {% else %}
        Garde le rythme, tu es sur la bonne voie.
        {% endif %}
      </p>
      <a href="#domains-grid" class="btn btn-or" style="display:inline-flex;">
        {% if prog_count == 0 %}
        Commencer mes défis
        {% else %}
        Continuer mes défis
        {% endif %}
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M5 12H19M19 12L13 6M19 12L13 18" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </a>
    </div>
    <div class="status-progress">
      <div class="progress-label"><span>Progression globale</span><span>{{ prog_percent }}%</span></div>
      <div class="progress-bar-track"><div class="progress-bar-fill" style="width:{{ prog_percent }}%"></div></div>
      <div class="domain-count">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none"><rect x="3" y="5" width="18" height="16" rx="2" stroke="currentColor" stroke-width="2"/><path d="M8 3V7M16 3V7M3 10H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
        {{ prog_count }} / {{ prog_max }} domaines terminés
      </div>
    </div>
  </section>
  {% endif %}

  <!-- ============ LES DOMAINES ============ -->
  <div class="domains-head {% if semaine_terminee %}state-done{% else %}state-todo{% endif %}">
    <h3>Les domaines essentiels</h3>
    <div class="info-chip">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/><path d="M12 16V11M12 8H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
      <span>
      {% if semaine_terminee %}
      Chaque domaine terminé te rapproche de la meilleure version de toi-même.
      {% else %}
      Chaque domaine te rapproche de la meilleure version de toi-même.
      {% endif %}
      </span>
    </div>
  </div>

  <div class="domains-grid" id="domains-grid">
    {% for cat in categories_data %}
    <a href="{% url 'domaine_detail' cat.domaine.id %}" class="domain-card {% if cat.optionnel %}optional{% endif %}">
      <div class="domain-top">
        <div class="domain-icon" style="background:{% if cat.code == 'vie_pro' %}#eaf2ff{% elif cat.code == 'argent' %}#fff6e0{% elif cat.code == 'objectifs' %}#fff2e0{% elif cat.code == 'moi_meme' %}#fdeaf0{% elif cat.code == 'reseaux_sociaux' %}#e9f8ee{% elif cat.code == 'relation_amoureuse' %}#f2edfb{% elif cat.code == 'spiritualite' %}#f2edfb{% endif %};">
          {% if cat.code == 'vie_pro' %}
          <svg viewBox="0 0 24 24" fill="none"><rect x="4" y="7" width="16" height="12" rx="2" stroke="#1a4fb4" stroke-width="1.8"/><path d="M8 7V5.5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2V7" stroke="#1a4fb4" stroke-width="1.8"/></svg>
          {% elif cat.code == 'argent' %}
          <svg viewBox="0 0 24 24" fill="none"><path d="M5 9c0-2 3-3 7-3s7 1 7 3-3 3-7 3-7-1-7-3Z" stroke="#c9860a" stroke-width="1.8"/><path d="M5 9v6c0 2 3 3 7 3s7-1 7-3V9" stroke="#c9860a" stroke-width="1.8"/></svg>
          {% elif cat.code == 'objectifs' %}
          <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="8" stroke="#c9860a" stroke-width="1.8"/><circle cx="12" cy="12" r="3" stroke="#c9860a" stroke-width="1.8"/></svg>
          {% elif cat.code == 'moi_meme' %}
          <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="8" r="4" stroke="#c94f7c" stroke-width="1.8"/><path d="M4 20c0-4 4-6 8-6s8 2 8 6" stroke="#c94f7c" stroke-width="1.8" stroke-linecap="round"/></svg>
          {% elif cat.code == 'reseaux_sociaux' %}
          <svg viewBox="0 0 24 24" fill="none"><rect x="4" y="4" width="16" height="12" rx="2" stroke="#1f9d55" stroke-width="1.8"/><path d="M9 20h6M12 16v4" stroke="#1f9d55" stroke-width="1.8" stroke-linecap="round"/></svg>
          {% elif cat.code == 'relation_amoureuse' %}
          <svg viewBox="0 0 24 24" fill="none"><path d="M12 20s-7-4.5-7-10a4.5 4.5 0 0 1 7-3.7A4.5 4.5 0 0 1 19 10c0 5.5-7 10-7 10Z" stroke="#7a4fc9" stroke-width="1.8" stroke-linejoin="round"/></svg>
          {% elif cat.code == 'spiritualite' %}
          <svg viewBox="0 0 24 24" fill="none"><path d="M12 3c2 3 4 5 4 9a4 4 0 0 1-8 0c0-4 2-6 4-9Z" stroke="#7a4fc9" stroke-width="1.8" stroke-linejoin="round"/></svg>
          {% endif %}
        </div>
        <div class="domain-info">
          {% if cat.optionnel %}<span class="optional-badge">Optionnel</span>{% endif %}
          <h4>{{ cat.label }}</h4>
          <p>{{ cat.domaine.description|default:"" }}</p>
        </div>
      </div>
      <div class="domain-status-row">
        {% if cat.terminee %}
        <span class="status-done-tag">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="#1f9d55" stroke-width="2"/><path d="M8 12L11 15L16 9" stroke="#1f9d55" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          Terminé
        </span>
        {% else %}
        <span style="display:flex; align-items:center; justify-content:space-between; width:100%;">
          <span class="status-todo-tag">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><rect x="5" y="10" width="14" height="10" rx="2" stroke="#5a6472" stroke-width="1.8"/><path d="M8 10V7a4 4 0 0 1 8 0v3" stroke="#5a6472" stroke-width="1.8"/></svg>
            {% if cat.engagee %}En cours{% else %}À commencer{% endif %}
          </span>
          <span style="font-size:12px; font-weight:700; color:#5a6472;">{% if cat.engagee %}...{% else %}0%{% endif %}</span>
        </span>
        {% endif %}
      </div>
    </a>
    {% endfor %}
  </div>

  <!-- ============ AIDE ============ -->
  <div class="help-card">
    <div class="thumb">
      <img src="{% static 'images/programme/illu-communaute.png' %}" alt="communauté">
    </div>
    <div>
      <h3>Besoin d'aide ?</h3>
      <p>Notre communauté est là pour te soutenir et t'accompagner dans tes défis.</p>
    </div>
    <a href="{{ WHATSAPP_GROUP_LINK }}" target="_blank" class="btn btn-blue" style="display:inline-flex;">
      Rejoindre la communauté
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><path d="M5 12H19M19 12L13 6M19 12L13 18" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </a>
  </div>

</main>
{% endblock %}
"""

with open('templates/core/defi.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

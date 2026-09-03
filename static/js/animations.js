function initAnimations() {
    const observerOptions = {
        root: null,
        rootMargin: '100px',
        threshold: 0
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                // On arrête d'observer pour que l'animation ne se joue qu'une fois
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Sélectionner automatiquement les conteneurs majeurs pour leur appliquer l'animation
    // sans avoir besoin de modifier chaque template manuellement.
    const elementsToAnimate = document.querySelectorAll(`
        .domain-card, 
        .upcoming-card, 
        .completed-card, 
        .help-card, 
        .bg-white.rounded-\\[32px\\], 
        .bg-white.rounded-2xl, 
        .section-title, 
        .page-head, 
        .status-banner,
        .carte-profil,
        .bloc-parametre,
        main > section,
        main > div > section,
        .carte,
        .stat-item,
        .liste-programmes > div
    `);

    elementsToAnimate.forEach(el => {
        if (!el.classList.contains('animate-on-scroll')) {
            el.classList.add('animate-on-scroll');
        }
        observer.observe(el);
    });
}

document.addEventListener('DOMContentLoaded', initAnimations);
document.addEventListener('swup:contentReplaced', initAnimations);

// ==========================================
// LOGIQUE DE LA PAGE /REJOINDRE (AVEC SWUP)
// ==========================================
document.addEventListener('click', (e) => {
    // 1. Bouton "Rejoindre" -> afficher le formulaire
    const btnShowForm = e.target.closest('#btn-show-form');
    if (btnShowForm) {
        document.getElementById('screen-landing').style.display = 'none';
        document.getElementById('screen-form').style.display = 'flex';
    }

    // 2. Bouton "Retour" -> afficher l'accueil
    const btnShowLanding = e.target.closest('#btn-show-landing');
    if (btnShowLanding) {
        document.getElementById('screen-form').style.display = 'none';
        document.getElementById('screen-landing').style.display = 'flex';
    }

    // 3. Choix du genre
    const pill = e.target.closest('.pill');
    if (pill && pill.closest('.genre-row')) {
        const val = pill.id === 'pill-f' ? 'F' : 'M';
        document.getElementById('genre-input').value = val;
        document.getElementById('pill-f').classList.toggle('active', val === 'F');
        document.getElementById('pill-m').classList.toggle('active', val === 'M');
    }
});

document.addEventListener('submit', (e) => {
    if (e.target.id === 'adhesion-form') {
        let isValid = true;
        const prenom = document.getElementById('prenom');
        if (prenom && !prenom.value.trim()) { 
            document.getElementById('err-prenom').style.display = 'block'; isValid = false; 
        } else if (prenom) { 
            document.getElementById('err-prenom').style.display = 'none'; 
        }

        const age = document.getElementById('age');
        if (age && (!age.value || age.value < 10 || age.value > 99)) { 
            document.getElementById('err-age').style.display = 'block'; isValid = false; 
        } else if (age) { 
            document.getElementById('err-age').style.display = 'none'; 
        }

        const indicatif = document.getElementById('indicatif');
        const numeroLocal = document.getElementById('numero-local');
        const telHidden = document.getElementById('telephone');
        
        if (indicatif && numeroLocal && telHidden) {
            const numeroPropre = numeroLocal.value.trim().replace(/[\s-]/g, '');
            telHidden.value = indicatif.value + numeroPropre;
        }

        const tel = document.getElementById('telephone');
        if (tel && !tel.value.trim()) { 
            document.getElementById('err-tel').style.display = 'block'; isValid = false; 
        } else if (tel) { 
            document.getElementById('err-tel').style.display = 'none'; 
        }

        if (!isValid) e.preventDefault();
    }
});

// Focus effects using focusin/focusout for delegation
document.addEventListener('focusin', (e) => {
    if (e.target.matches('.input-shell input')) {
        e.target.parentElement.classList.add('focused');
    }
});
document.addEventListener('focusout', (e) => {
    if (e.target.matches('.input-shell input')) {
        e.target.parentElement.classList.remove('focused');
    }
});

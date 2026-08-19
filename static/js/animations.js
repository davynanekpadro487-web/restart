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

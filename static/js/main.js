
document.addEventListener('DOMContentLoaded', function() {
    // on sélectionne le bouton et les liens par leur ID
    const navToggle = document.getElementById('navToggle');
    const navLinks  = document.getElementById('navLinks');

    // si le bouton existe sur la page
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            // toggle('open') = ajoute la classe 'open' si absente, la retire si présente
            navLinks.classList.toggle('open');

            // on change l'icône selon l'état du menu
            const icon = navToggle.querySelector('i');
            if (navLinks.classList.contains('open')) {
                icon.className = 'ti ti-x'; // icône croix quand menu ouvert
            } else {
                icon.className = 'ti ti-menu-2'; // icône hamburger quand fermé
            }
        });
    }

    // ferme le menu si on clique en dehors
    document.addEventListener('click', function(event) {
        if (navToggle && navLinks) {
            // contains() = vérifie si l'élément cliqué est dans la navbar
            if (!navToggle.contains(event.target) && !navLinks.contains(event.target)) {
                navLinks.classList.remove('open');
                const icon = navToggle.querySelector('i');
                if (icon) icon.className = 'ti ti-menu-2';
            }
        }
    });

    // les messages disparaissent automatiquement après 5 secondes
    const messages = document.querySelectorAll('.message');
    messages.forEach(function(msg) {
        setTimeout(function() {
            // on vérifie que le message est encore dans la page
            if (msg.parentElement) {
                msg.style.opacity = '0';
                msg.style.transform = 'translateX(100%)';
                msg.style.transition = 'all 0.3s ease';
                // après l'animation, on supprime l'élément du DOM
                setTimeout(function() { msg.remove(); }, 300);
            }
        }, 5000); // 5000 millisecondes = 5 secondes
    });

    // tous les boutons avec data-confirm ont une boîte de confirmation
    const confirmButtons = document.querySelectorAll('[data-confirm]');
    confirmButtons.forEach(function(btn) {
        btn.addEventListener('click', function(event) {
            // data-confirm = le message à afficher
            const message = btn.getAttribute('data-confirm');
            // confirm() = boîte de dialogue native du navigateur
            // retourne true si l'utilisateur clique OK, false sinon
            if (!confirm(message)) {
                event.preventDefault(); // annule l'action si l'utilisateur dit Non
            }
        });
    });

});
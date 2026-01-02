
/* Correction du chargement des charts - Cabinet d'Avocats */

// Fonction pour initialiser les charts après le chargement complet
function initializeCharts() {
    console.log('Initialisation des charts...');
    
    // Attendre que tous les scripts soient chargés
    setTimeout(function() {
        // Forcer le redimensionnement des charts
        if (typeof window.dispatchEvent === 'function') {
            window.dispatchEvent(new Event('resize'));
        }
        
        // Réinitialiser les charts ApexCharts si présents
        if (typeof ApexCharts !== 'undefined') {
            console.log('ApexCharts détecté, réinitialisation...');
            // Trouver tous les éléments de charts
            document.querySelectorAll('[id*="chart"], [class*="chart"]').forEach(function(element) {
                if (element.id && !element.classList.contains('chart-initialized')) {
                    element.classList.add('chart-initialized');
                    // Forcer le rendu du chart
                    setTimeout(function() {
                        if (window[element.id + '_chart']) {
                            window[element.id + '_chart'].render();
                        }
                    }, 100);
                }
            });
        }
        
        // Réinitialiser les charts Morris si présents
        if (typeof Morris !== 'undefined') {
            console.log('Morris charts détecté, réinitialisation...');
            // Redessiner tous les charts Morris
            Morris.charts.forEach(function(chart) {
                if (chart && typeof chart.redraw === 'function') {
                    chart.redraw();
                }
            });
        }
        
        // Réinitialiser les charts Chart.js si présents
        if (typeof Chart !== 'undefined') {
            console.log('Chart.js détecté, réinitialisation...');
            Chart.helpers.each(Chart.instances, function(instance) {
                if (instance && typeof instance.update === 'function') {
                    instance.update();
                }
            });
        }
        
        // Réinitialiser les charts C3 si présents
        if (typeof c3 !== 'undefined') {
            console.log('C3 charts détecté, réinitialisation...');
            // Les charts C3 sont stockés globalement
            Object.keys(window).forEach(function(key) {
                if (key.includes('chart') && window[key] && typeof window[key].flush === 'function') {
                    window[key].flush();
                }
            });
        }
        
    }, 500);
}

// Initialiser les charts quand le DOM est prêt
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeCharts);
} else {
    initializeCharts();
}

// Réinitialiser les charts lors du redimensionnement de la fenêtre
window.addEventListener('resize', function() {
    setTimeout(initializeCharts, 100);
});

// Réinitialiser les charts lors des changements de page (pour les SPA)
window.addEventListener('popstate', function() {
    setTimeout(initializeCharts, 200);
});

// Observer les changements dans le DOM pour les charts ajoutés dynamiquement
if (typeof MutationObserver !== 'undefined') {
    const chartObserver = new MutationObserver(function(mutations) {
        let hasNewCharts = false;
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1) { // Element node
                        if (node.id && (node.id.includes('chart') || node.className.includes('chart'))) {
                            hasNewCharts = true;
                        }
                        // Vérifier les enfants aussi
                        const chartElements = node.querySelectorAll && node.querySelectorAll('[id*="chart"], [class*="chart"]');
                        if (chartElements && chartElements.length > 0) {
                            hasNewCharts = true;
                        }
                    }
                });
            }
        });
        
        if (hasNewCharts) {
            console.log('Nouveaux charts détectés, réinitialisation...');
            setTimeout(initializeCharts, 300);
        }
    });
    
    // Observer les changements dans le body
    chartObserver.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// Fonction globale pour forcer la réinitialisation des charts
window.forceChartsRefresh = function() {
    console.log('Forçage de la réinitialisation des charts...');
    initializeCharts();
};

// Auto-refresh des charts toutes les 30 secondes pour s'assurer qu'ils restent visibles
setInterval(function() {
    // Vérifier si des charts sont invisibles
    const charts = document.querySelectorAll('[id*="chart"], [class*="chart"]');
    let hasInvisibleCharts = false;
    
    charts.forEach(function(chart) {
        if (chart.offsetHeight === 0 || chart.offsetWidth === 0) {
            hasInvisibleCharts = true;
        }
    });
    
    if (hasInvisibleCharts) {
        console.log('Charts invisibles détectés, réinitialisation...');
        initializeCharts();
    }
}, 30000);

console.log('Script de correction des charts chargé');

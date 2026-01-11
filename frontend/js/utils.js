/**
 * Utilitaires pour le frontend
 */

/**
 * Affiche un loader
 */
function showLoader(containerId = 'loader-container') {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="loader-wrapper">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Chargement...</span>
                </div>
                <p class="mt-3">Chargement en cours...</p>
                <p class="text-muted small">Le serveur peut mettre quelques secondes à répondre</p>
            </div>
        `;
        container.style.display = 'block';
    }
}

/**
 * Cache un loader
 */
function hideLoader(containerId = 'loader-container') {
    const container = document.getElementById(containerId);
    if (container) {
        container.style.display = 'none';
    }
}

/**
 * Affiche un message d'erreur
 */
function showError(message, containerId = 'error-container') {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="fas fa-exclamation-circle"></i> ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        container.style.display = 'block';
    }
}

/**
 * Affiche un message de succès
 */
function showSuccess(message, containerId = 'success-container') {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                <i class="fas fa-check-circle"></i> ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        container.style.display = 'block';
        
        // Auto-hide après 5 secondes
        setTimeout(() => {
            container.style.display = 'none';
        }, 5000);
    }
}

/**
 * Formate une date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    });
}

/**
 * Formate un prix
 */
function formatPrice(price) {
    if (!price) return 'Gratuit';
    return `${parseFloat(price).toFixed(2)} MRU`;
}

/**
 * Formate l'URL de l'image
 */
function getImageUrl(imageUrl) {
    if (!imageUrl) return '/images/placeholder.jpg';
    // Si c'est déjà une URL complète
    if (imageUrl.startsWith('http')) return imageUrl;
    // Sinon, préfixer avec l'API base URL
    return `https://gestion-annonce.onrender.com${imageUrl}`;
}

/**
 * Gère les erreurs API et affiche un message approprié
 */
function handleAPIError(error, containerId = 'error-container') {
    let message = 'Une erreur est survenue';
    
    if (error instanceof APIError) {
        if (error.status === 401) {
            message = 'Vous devez être connecté pour effectuer cette action';
            if (window.location.pathname !== '/login.html') {
                setTimeout(() => {
                    window.location.href = '/login.html';
                }, 2000);
            }
        } else if (error.status === 403) {
            message = 'Vous n\'avez pas la permission d\'effectuer cette action';
        } else if (error.status === 404) {
            message = 'Ressource non trouvée';
        } else if (error.status === 0) {
            message = 'Le serveur ne répond pas. Il est peut-être en veille. Veuillez réessayer dans quelques instants.';
        } else {
            message = error.message || `Erreur ${error.status}`;
        }
    } else {
        message = error.message || 'Une erreur inattendue est survenue';
    }
    
    showError(message, containerId);
}

/**
 * Redirige vers login si non authentifié
 */
function requireAuth() {
    if (!api.isAuthenticated()) {
        window.location.href = '/login.html';
        return false;
    }
    return true;
}


/**
 * Client API pour communiquer avec le backend Django sur Render
 * Gère l'authentification JWT, les retries pour le sleep Render, et les erreurs
 */

const API_BASE_URL = 'https://gestion-annonce.onrender.com/api';
const MAX_RETRIES = 3;
const RETRY_DELAY = 2000; // 2 secondes entre les retries
const WAKE_UP_DELAY = 30000; // 30 secondes pour le réveil du serveur

class APIError extends Error {
    constructor(message, status, data = null) {
        super(message);
        this.name = 'APIError';
        this.status = status;
        this.data = data;
    }
}

class APIClient {
    constructor() {
        this.accessToken = localStorage.getItem('access_token');
        this.refreshToken = localStorage.getItem('refresh_token');
    }

    /**
     * Récupère le token d'accès depuis le localStorage
     */
    getAccessToken() {
        return localStorage.getItem('access_token');
    }

    /**
     * Stocke les tokens
     */
    setTokens(access, refresh) {
        this.accessToken = access;
        this.refreshToken = refresh;
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
    }

    /**
     * Supprime les tokens (logout)
     */
    clearTokens() {
        this.accessToken = null;
        this.refreshToken = null;
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    }

    /**
     * Rafraîchit le token d'accès
     */
    async refreshAccessToken() {
        if (!this.refreshToken) {
            throw new APIError('No refresh token available', 401);
        }

        try {
            const response = await fetch(`${API_BASE_URL}/token/refresh/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ refresh: this.refreshToken }),
            });

            if (!response.ok) {
                throw new APIError('Token refresh failed', response.status);
            }

            const data = await response.json();
            this.setTokens(data.access, this.refreshToken);
            return data.access;
        } catch (error) {
            this.clearTokens();
            throw error;
        }
    }

    /**
     * Effectue une requête avec retry logic pour gérer le sleep Render
     */
    async request(url, options = {}, retryCount = 0) {
        const token = this.getAccessToken();
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        if (token && !options.skipAuth) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const config = {
            ...options,
            headers,
        };

        try {
            const response = await fetch(`${API_BASE_URL}${url}`, config);

            // Si 401, essayer de rafraîchir le token
            if (response.status === 401 && token && !options.skipAuth) {
                try {
                    const newToken = await this.refreshAccessToken();
                    headers['Authorization'] = `Bearer ${newToken}`;
                    const retryResponse = await fetch(`${API_BASE_URL}${url}`, {
                        ...config,
                        headers,
                    });
                    if (retryResponse.ok) {
                        return await retryResponse.json();
                    }
                } catch (refreshError) {
                    // Refresh failed, redirect to login
                    this.clearTokens();
                    if (window.location.pathname !== '/login.html') {
                        window.location.href = '/login.html';
                    }
                    throw new APIError('Authentication failed', 401);
                }
            }

            // Si erreur serveur (503, 502, 504) - serveur en veille ou problème
            if ([502, 503, 504].includes(response.status) && retryCount < MAX_RETRIES) {
                const delay = retryCount === 0 ? WAKE_UP_DELAY : RETRY_DELAY;
                await this.sleep(delay);
                return this.request(url, options, retryCount + 1);
            }

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new APIError(
                    errorData.detail || errorData.message || `HTTP ${response.status}`,
                    response.status,
                    errorData
                );
            }

            // Si réponse vide (204 No Content)
            if (response.status === 204) {
                return null;
            }

            return await response.json();
        } catch (error) {
            if (error instanceof APIError) {
                throw error;
            }

            // Erreur réseau ou timeout
            if (retryCount < MAX_RETRIES) {
                const delay = retryCount === 0 ? WAKE_UP_DELAY : RETRY_DELAY;
                await this.sleep(delay);
                return this.request(url, options, retryCount + 1);
            }

            throw new APIError(
                'Network error or server unavailable. Please try again later.',
                0,
                { originalError: error.message }
            );
        }
    }

    /**
     * Helper pour sleep/delay
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    // ==================== AUTHENTICATION ====================

    /**
     * Login - obtient les tokens JWT
     */
    async login(username, password) {
        const data = await this.request('/token/', {
            method: 'POST',
            skipAuth: true,
            body: JSON.stringify({ username, password }),
        });
        this.setTokens(data.access, data.refresh);
        return data;
    }

    /**
     * Logout
     */
    logout() {
        this.clearTokens();
    }

    /**
     * Vérifie si l'utilisateur est authentifié
     */
    isAuthenticated() {
        return !!this.getAccessToken();
    }

    // ==================== ANNONCES ====================

    /**
     * Liste des annonces avec filtres optionnels
     */
    async getAnnonces(filters = {}) {
        const params = new URLSearchParams();
        Object.keys(filters).forEach(key => {
            if (filters[key] !== null && filters[key] !== undefined && filters[key] !== '') {
                params.append(key, filters[key]);
            }
        });
        const queryString = params.toString();
        const url = `/annonces/${queryString ? `?${queryString}` : ''}`;
        return this.request(url);
    }

    /**
     * Détail d'une annonce
     */
    async getAnnonce(id) {
        return this.request(`/annonces/${id}/`);
    }

    /**
     * Créer une annonce
     */
    async createAnnonce(annonceData) {
        // Pour les fichiers, utiliser FormData
        if (annonceData.image && annonceData.image instanceof File) {
            const formData = new FormData();
            Object.keys(annonceData).forEach(key => {
                if (key === 'image') {
                    formData.append('image', annonceData.image);
                } else if (annonceData[key] !== null && annonceData[key] !== undefined) {
                    formData.append(key, annonceData[key]);
                }
            });

            const token = this.getAccessToken();
            const response = await fetch(`${API_BASE_URL}/annonces/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new APIError(
                    errorData.detail || errorData.message || `HTTP ${response.status}`,
                    response.status,
                    errorData
                );
            }

            return await response.json();
        }

        return this.request('/annonces/', {
            method: 'POST',
            body: JSON.stringify(annonceData),
        });
    }

    /**
     * Modifier une annonce
     */
    async updateAnnonce(id, annonceData) {
        if (annonceData.image && annonceData.image instanceof File) {
            const formData = new FormData();
            Object.keys(annonceData).forEach(key => {
                if (key === 'image') {
                    formData.append('image', annonceData.image);
                } else if (annonceData[key] !== null && annonceData[key] !== undefined) {
                    formData.append(key, annonceData[key]);
                }
            });

            const token = this.getAccessToken();
            const response = await fetch(`${API_BASE_URL}/annonces/${id}/`, {
                method: 'PATCH',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new APIError(
                    errorData.detail || errorData.message || `HTTP ${response.status}`,
                    response.status,
                    errorData
                );
            }

            return await response.json();
        }

        return this.request(`/annonces/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(annonceData),
        });
    }

    /**
     * Supprimer une annonce
     */
    async deleteAnnonce(id) {
        return this.request(`/annonces/${id}/`, {
            method: 'DELETE',
        });
    }

    /**
     * Valider une annonce (admin)
     */
    async validerAnnonce(id) {
        return this.request(`/annonces/${id}/valider/`, {
            method: 'POST',
        });
    }

    /**
     * Rejeter une annonce (admin)
     */
    async rejeterAnnonce(id) {
        return this.request(`/annonces/${id}/rejeter/`, {
            method: 'POST',
        });
    }

    /**
     * Incrémenter les vues
     */
    async incrementerVues(id) {
        return this.request(`/annonces/${id}/incrementer_vues/`, {
            method: 'POST',
        });
    }

    // ==================== CATEGORIES ====================

    /**
     * Liste des catégories
     */
    async getCategories() {
        return this.request('/categories/');
    }

    /**
     * Détail d'une catégorie
     */
    async getCategorie(id) {
        return this.request(`/categories/${id}/`);
    }

    /**
     * Créer une catégorie (admin)
     */
    async createCategorie(categorieData) {
        return this.request('/categories/', {
            method: 'POST',
            body: JSON.stringify(categorieData),
        });
    }

    /**
     * Modifier une catégorie (admin)
     */
    async updateCategorie(id, categorieData) {
        return this.request(`/categories/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(categorieData),
        });
    }

    /**
     * Supprimer une catégorie (admin)
     */
    async deleteCategorie(id) {
        return this.request(`/categories/${id}/`, {
            method: 'DELETE',
        });
    }
}

// Instance globale
const api = new APIClient();


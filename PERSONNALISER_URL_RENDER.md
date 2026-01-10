# 🔗 Guide pour Personnaliser l'URL sur Render

Ce guide vous explique comment personnaliser l'URL de votre application sur Render.

## 🎯 Options Disponibles

Sur Render, vous avez **deux options** pour personnaliser votre URL :

1. **Changer le nom du service** (Gratuit) → Change l'URL de `gestion-annonce.onrender.com` à `votre-nom.onrender.com`
2. **Ajouter un domaine personnalisé** (Nécessite un domaine acheté) → Utilise votre propre domaine comme `adplus.com`

---

## 📝 Option 1 : Changer le Nom du Service (Recommandé pour commencer)

Cette option est **gratuite** et vous permet de choisir un nom personnalisé pour votre service.

### Étapes

1. **Allez dans votre Web Service sur Render**
   - Connectez-vous à [dashboard.render.com](https://dashboard.render.com)
   - Cliquez sur votre service Web

2. **Accédez aux paramètres**
   - Cliquez sur l'onglet **"Settings"** en haut

3. **Modifiez le nom du service**
   - Trouvez la section **"Name"** en haut de la page
   - Cliquez sur le bouton **"Edit"** (ou l'icône crayon) à côté du nom
   - Entrez votre nouveau nom (exemples : `adplus`, `annonces-plus`, `gestion-annonces`)
   - ⚠️ **Règles** :
     - Uniquement lettres minuscules, chiffres et tirets (-)
     - Pas d'espaces
     - Doit être unique sur Render
   - Cliquez sur **"Save"** ou **"Update"**

4. **Mettre à jour ALLOWED_HOSTS**
   - Allez dans l'onglet **"Environment"**
   - Trouvez ou créez la variable `ALLOWED_HOSTS`
   - Mettez à jour la valeur avec votre nouveau nom : `votre-nouveau-nom.onrender.com`
   - Exemple : Si vous avez renommé en `adplus`, mettez : `adplus.onrender.com`
   - Sauvegardez

5. **Redéployez** (automatique ou manuel)
   - Render redéploiera automatiquement après le changement de nom
   - Ou allez dans **"Manual Deploy"** → **"Deploy latest commit"**

6. **Nouvelle URL**
   - Votre nouvelle URL sera : `https://votre-nouveau-nom.onrender.com`
   - Testez-la pour vérifier que tout fonctionne

### Exemples de noms

✅ **Bons noms** :
- `adplus`
- `annonces-plus`
- `gestion-annonces`
- `adplus-app`
- `mes-annonces`

❌ **Noms invalides** :
- `AdPlus` (majuscules non autorisées)
- `ad plus` (espaces non autorisés)
- `ad_plus` (underscores pas recommandés, utilisez des tirets)
- `adplus.com` (ne mettez pas d'extension de domaine)

---

## 🌐 Option 2 : Domaine Personnalisé (Domaine acheté requis)

Si vous avez acheté un domaine (ex: `adplus.com`, `mesannonces.fr`), vous pouvez l'utiliser avec Render.

### Prérequis

- Un domaine acheté auprès d'un registraire (OVH, Namecheap, GoDaddy, etc.)
- Accès aux paramètres DNS de votre domaine

### Étapes

1. **Dans Render**
   - Allez dans votre Web Service → **"Settings"**
   - Scrollez jusqu'à la section **"Custom Domains"**
   - Cliquez sur **"Add Custom Domain"**
   - Entrez votre domaine : `adplus.com` ou `www.adplus.com`
   - Cliquez sur **"Save"**

2. **Render vous donnera des instructions DNS**
   - Notez l'enregistrement CNAME ou A à ajouter
   - Exemple : `CNAME: adplus.com → votre-service.onrender.com`

3. **Dans votre registraire de domaine**
   - Connectez-vous à votre compte (OVH, Namecheap, etc.)
   - Allez dans les paramètres DNS de votre domaine
   - Ajoutez l'enregistrement CNAME ou A fourni par Render
   - Sauvegardez

4. **Attendre la propagation DNS**
   - La propagation peut prendre de quelques minutes à 48 heures
   - Render vérifiera automatiquement la configuration

5. **Mettre à jour ALLOWED_HOSTS**
   - Dans Render → **"Environment"**
   - Ajoutez votre domaine dans `ALLOWED_HOSTS` : `adplus.com,www.adplus.com`
   - Sauvegardez et redéployez

6. **SSL automatique**
   - Render génère automatiquement un certificat SSL gratuit
   - Votre site sera accessible en HTTPS

### Configuration DNS exemple

**Pour un domaine nu** (`adplus.com`) :
```
Type: CNAME
Nom: @ ou (vide)
Valeur: votre-service.onrender.com
```

**Pour un sous-domaine** (`www.adplus.com`) :
```
Type: CNAME
Nom: www
Valeur: votre-service.onrender.com
```

---

## 🔧 Mise à Jour Automatique dans le Code

Le code est déjà configuré pour détecter automatiquement le domaine Render via la variable d'environnement `RENDER_EXTERNAL_URL`. Cependant, il est recommandé de définir explicitement `ALLOWED_HOSTS` dans les variables d'environnement.

### Variables d'environnement à configurer

Dans Render → **"Environment"**, ajoutez/modifiez :

**Si vous avez changé le nom du service :**
```
ALLOWED_HOSTS=votre-nouveau-nom.onrender.com
```

**Si vous utilisez un domaine personnalisé :**
```
ALLOWED_HOSTS=adplus.com,www.adplus.com,votre-service.onrender.com
```

---

## ✅ Après Personnalisation

1. ✅ Vérifiez que votre nouvelle URL fonctionne
2. ✅ Testez la connexion admin
3. ✅ Vérifiez que les fichiers statiques se chargent correctement
4. ✅ Testez toutes les fonctionnalités importantes

---

## 🔄 Revenir en Arrière

Si vous voulez revenir au nom précédent :
- Suivez les mêmes étapes et remettez l'ancien nom
- Mettez à jour `ALLOWED_HOSTS` avec l'ancien domaine
- Redéployez

---

## 📞 Support

- Documentation Render : [render.com/docs/custom-domains](https://render.com/docs/custom-domains)
- Support Render : [render.com/support](https://render.com/support)

---

## 💡 Conseils

1. **Choisissez un nom court et mémorable** pour votre service
2. **Vérifiez la disponibilité** avant de le configurer
3. **Testez bien après chaque changement** pour éviter les problèmes
4. **Gardez une copie de votre ancien ALLOWED_HOSTS** au cas où


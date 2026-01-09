"""
Script automatisé pour capturer toutes les pages de l'application
Utilise Playwright pour automatiser la navigation et les captures
"""
import os
import sys
import asyncio
from pathlib import Path

# Configuration Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plateforme_annonces.settings')

import django
django.setup()

try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

def get_urls():
    """Retourne la liste de toutes les URLs à capturer"""
    base = "http://127.0.0.1:8000"
    
    from annonces.models import Annonce, Categorie
    from authentification.models import Utilisateur
    
    try:
        first_annonce = Annonce.objects.first()
        first_categorie = Categorie.objects.first()
    except Exception as e:
        print(f"Erreur lors de la recuperation des donnees: {e}")
        first_annonce = None
        first_categorie = None
    
    urls = {
        'public': [],      # Pages publiques (pas besoin de connexion)
        'user': [],        # Pages utilisateur (nécessitent connexion client)
        'admin': []        # Pages admin (nécessitent connexion admin)
    }
    
    # Pages publiques
    urls['public'].append(('portfolio', f'{base}/', 'Portfolio (Accueil)', False))
    urls['public'].append(('liste_annonces', f'{base}/app/', 'Liste des annonces', False))
    urls['public'].append(('connexion', f'{base}/connexion/', 'Page de connexion', False))
    urls['public'].append(('inscription', f'{base}/inscription/', 'Page d\'inscription', False))
    
    if first_annonce:
        urls['public'].append(('detail_annonce', f'{base}/annonces/{first_annonce.id}/', f'Detail annonce #{first_annonce.id}', False))
    
    # Pages utilisateur (nécessitent connexion client)
    urls['user'].append(('mes_annonces', f'{base}/mes-annonces/', 'Mes annonces (utilisateur)', True))
    urls['user'].append(('creer_annonce', f'{base}/creer/', 'Creer annonce (utilisateur)', True))
    
    if first_annonce:
        urls['user'].append(('modifier_annonce', f'{base}/modifier/{first_annonce.id}/', f'Modifier annonce #{first_annonce.id} (utilisateur)', True))
    
    # Pages admin (nécessitent authentification admin)
    urls['admin'].append(('admin_dashboard', f'{base}/admins/', 'Tableau de bord admin', True))
    urls['admin'].append(('admin_categories', f'{base}/admins/categories/', 'Liste categories admin', True))
    urls['admin'].append(('admin_creer_annonce', f'{base}/admins/creer/', 'Creer annonce admin', True))
    urls['admin'].append(('admin_creer_categorie', f'{base}/admins/categories/creer/', 'Creer categorie admin', True))
    
    if first_annonce:
        urls['admin'].append(('admin_modifier_annonce', f'{base}/admins/modifier/{first_annonce.id}/', f'Modifier annonce #{first_annonce.id} admin', True))
    
    if first_categorie:
        urls['admin'].append(('admin_modifier_categorie', f'{base}/admins/categories/modifier/{first_categorie.id}/', f'Modifier categorie #{first_categorie.id} admin', True))
    
    return urls

async def capture_page(page, url_info, screenshot_dir):
    """Capture une page avec Playwright"""
    name, url, description, requires_auth = url_info
    try:
        print(f"Capture de: {description}")
        print(f"   URL: {url}")
        
        await page.goto(url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(3000)  # Attendre le chargement complet
        
        # Faire défiler la page pour charger les contenus lazy
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await page.wait_for_timeout(1500)
        await page.evaluate('window.scrollTo(0, 0)')
        await page.wait_for_timeout(1000)
        
        # Capture plein écran
        screenshot_path = screenshot_dir / f"{name}_full.png"
        await page.screenshot(path=str(screenshot_path), full_page=True)
        print(f"   OK Capture: {screenshot_path.name}\n")
        
        return True
    except Exception as e:
        print(f"   ERREUR: {str(e)}\n")
        return False

async def capture_all(urls_dict):
    """Capture toutes les pages"""
    screenshot_dir = Path('screenshots')
    screenshot_dir.mkdir(exist_ok=True)
    
    if not PLAYWRIGHT_AVAILABLE:
        print("Playwright n'est pas installe.")
        print("Installez-le avec:")
        print("   pip install playwright")
        print("   playwright install chromium")
        return
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            locale='fr-FR'
        )
        page = await context.new_page()
        
        total_pages = len(urls_dict['public']) + len(urls_dict['user']) + len(urls_dict['admin'])
        print(f"\nDemarrage de la capture de {total_pages} pages...\n")
        
        # 1. Pages publiques (pas besoin de connexion)
        print("=== ETAPE 1: PAGES PUBLIQUES ===\n")
        for url_info in urls_dict['public']:
            await capture_page(page, url_info, screenshot_dir)
        
        # 2. Pages utilisateur (nécessitent connexion client)
        print("\n" + "="*60)
        print("=== ETAPE 2: PAGES UTILISATEUR ===")
        print("="*60)
        print("\n📌 IMPORTANT: Vous devez etre connecte en tant qu'utilisateur client.")
        print("   Si vous n'etes pas encore connecte:")
        print("   1. Cliquez sur le navigateur qui vient de s'ouvrir")
        print("   2. Allez sur la page de connexion si necessaire")
        print("   3. Connectez-vous avec un compte utilisateur (client)")
        print("\n   Le script attendra 30 secondes pour vous donner le temps de vous connecter...")
        print("   Prenez votre temps! 💤\n")
        await page.wait_for_timeout(30000)  # Attendre 30 secondes
        
        # Vérifier qu'on est bien connecté en visitant une page utilisateur
        print("   🔍 Verification de la connexion utilisateur...")
        try:
            await page.goto("http://127.0.0.1:8000/mes-annonces/", wait_until='networkidle', timeout=15000)
            await page.wait_for_timeout(3000)
            current_url = page.url
            if 'connexion' in current_url:
                print("   ⚠️  ATTENTION: Vous n'etes pas encore connecte en tant qu'utilisateur.")
                print("   📝 Le script attendra encore 20 secondes pour que vous puissiez vous connecter...")
                print("   👆 N'hesitez pas a prendre votre temps!\n")
                await page.wait_for_timeout(20000)  # Attendre encore 20 secondes
            else:
                print("   ✅ Connexion utilisateur verifiee!\n")
        except Exception as e:
            print(f"   ⚠️  Verification impossible: {str(e)}")
            print("   ➡️  Continuons quand meme...\n")
        
        print("   🎬 Debut des captures utilisateur...\n")
        for url_info in urls_dict['user']:
            await capture_page(page, url_info, screenshot_dir)
        
        # 3. Pages admin (nécessitent connexion admin)
        print("\n" + "="*60)
        print("=== ETAPE 3: PAGES ADMIN ===")
        print("="*60)
        print("\n📌 IMPORTANT: Ces pages necessitent une connexion ADMIN.")
        print("   Actions a effectuer:")
        print("   1. Deconnectez-vous du compte utilisateur actuel")
        print("   2. Connectez-vous en tant qu'ADMIN dans le navigateur")
        print("   3. Allez sur le dashboard admin pour verifier")
        print("\n   ⏰ Le script attendra 45 secondes pour vous donner tout le temps necessaire...")
        print("   Prenez votre temps pour bien vous connecter! 💤\n")
        await page.wait_for_timeout(45000)  # Attendre 45 secondes
        
        # Vérifier qu'on est bien connecté en tant qu'admin
        print("   🔍 Verification de la connexion admin...")
        try:
            await page.goto("http://127.0.0.1:8000/admins/", wait_until='networkidle', timeout=15000)
            await page.wait_for_timeout(3000)
            current_url = page.url
            if 'connexion' in current_url:
                print("   ⚠️  ATTENTION: Vous n'etes pas encore connecte en tant qu'admin.")
                print("   📝 Le script attendra encore 25 secondes pour que vous puissiez vous connecter...")
                print("   👆 N'hesitez pas a prendre votre temps!\n")
                await page.wait_for_timeout(25000)  # Attendre encore 25 secondes
            else:
                print("   ✅ Connexion admin verifiee!\n")
        except Exception as e:
            print(f"   ⚠️  Verification impossible: {str(e)}")
            print("   ➡️  Continuons quand meme...\n")
        
        print("   🎬 Debut des captures admin...\n")
        
        for url_info in urls_dict['admin']:
            await capture_page(page, url_info, screenshot_dir)
        
        await browser.close()
    
    print(f"\n{'='*60}")
    print(f"Capture terminee! Toutes les captures sont dans: {screenshot_dir}")
    print(f"{'='*60}")

if __name__ == '__main__':
    if PLAYWRIGHT_AVAILABLE:
        # Récupérer les URLs AVANT d'entrer dans asyncio.run()
        # pour éviter les problèmes de contexte async avec Django
        try:
            urls_dict = get_urls()
            total = len(urls_dict['public']) + len(urls_dict['user']) + len(urls_dict['admin'])
            print(f"Pages a capturer: {total}")
            print(f"   - Publiques: {len(urls_dict['public'])}")
            print(f"   - Utilisateur: {len(urls_dict['user'])}")
            print(f"   - Admin: {len(urls_dict['admin'])}\n")
        except Exception as e:
            print(f"Erreur lors de la preparation: {e}")
            urls_dict = {'public': [], 'user': [], 'admin': []}
        
        if any(urls_dict.values()):
            asyncio.run(capture_all(urls_dict))
    else:
        print("Playwright n'est pas disponible.")
        print("Generation de la liste des URLs uniquement...")
        import capture_screenshots
        capture_screenshots.create_urls_list()


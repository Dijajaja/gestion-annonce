"""
Script pour compiler les fichiers de traduction .po en .mo
Utilise la bibliothèque babel si disponible, sinon utilise polib
"""
import os
import sys
from pathlib import Path

try:
    from babel.messages import catalog, pofile
    USE_BABEL = True
except ImportError:
    try:
        import polib
        USE_BABEL = False
    except ImportError:
        print("Erreur: Aucune bibliothèque de traduction trouvée.")
        print("Installez babel ou polib:")
        print("  pip install babel")
        print("  ou")
        print("  pip install polib")
        sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / 'locale'

def compile_po_to_mo(po_file, mo_file):
    """Compile un fichier .po en .mo"""
    try:
        if USE_BABEL:
            from babel.messages import mofile
            with open(po_file, 'rb') as f:
                catalog_obj = pofile.read_po(f)
            
            with open(mo_file, 'wb') as f:
                mofile.write_mo(f, catalog_obj)
        else:
            po = polib.pofile(str(po_file))
            po.save_as_mofile(str(mo_file))
        
        print(f"OK: Compile {po_file.name} -> {mo_file.name}")
        return True
    except Exception as e:
        print(f"ERROR: Erreur lors de la compilation de {po_file}: {e}")
        return False

def main():
    """Compile tous les fichiers .po dans locale/"""
    if not LOCALE_DIR.exists():
        print(f"Le répertoire {LOCALE_DIR} n'existe pas.")
        return
    
    compiled = 0
    failed = 0
    
    # Parcourir tous les répertoires de langue
    for lang_dir in LOCALE_DIR.iterdir():
        if not lang_dir.is_dir():
            continue
        
        lc_messages_dir = lang_dir / 'LC_MESSAGES'
        if not lc_messages_dir.exists():
            continue
        
        po_file = lc_messages_dir / 'django.po'
        mo_file = lc_messages_dir / 'django.mo'
        
        if po_file.exists():
            if compile_po_to_mo(po_file, mo_file):
                compiled += 1
            else:
                failed += 1
        else:
            print(f"WARNING: Fichier .po introuvable: {po_file}")
    
    print(f"\nRésumé: {compiled} fichier(s) compilé(s), {failed} échec(s)")

if __name__ == '__main__':
    main()


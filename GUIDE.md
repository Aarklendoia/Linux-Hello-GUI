# Guide d'Utilisation – Linux Hello GUI

## Démarrage Rapide

### 1. Installation

#### Debian/Ubuntu
```bash
sudo apt-get install linux-hello-gui
```

#### Depuis les sources
```bash
git clone https://github.com/ebiton/Linux-Hello
cd Linux-Hello-GUI
./install.sh
```

### 2. Lancement

#### Via le menu de KDE
1. Ouvrir le menu d'applications KDE (généralement en bas à gauche)
2. Chercher "Linux Hello" ou "Configuration Linux Hello"
3. Cliquer sur l'application

#### Depuis le terminal
```bash
linux-hello-gui
```

## Interface Principale

L'application contient 3 onglets principaux:

### 🎥 Onglet "Visage" – Inscription Faciale

**Objectif:** Enregistrer vos données faciales pour l'authentification

#### Étapes:

1. **Sélectionner la caméra**
   - Ouvrir le menu déroulant "Caméra"
   - Sélectionner votre caméra
   - Cliquer sur "Rafraîchir" pour détecter les caméras

2. **Démarrer l'aperçu vidéo**
   - Cliquer sur "Démarrer caméra"
   - Vous verrez l'image en direct de votre caméra

3. **Configurer l'enregistrement**
   - Entrer votre nom d'utilisateur (ex: `john.doe`)
   - Ajuster le nombre de photos (entre 10 et 100)
     - Plus de photos = meilleure précision
     - Moins de photos = plus rapide

4. **Inscrire votre visage**
   - Cliquer sur "Inscrire le visage"
   - L'application capturera automatiquement les photos
   - Votre progression s'affichera: "Capture X/Y"

5. **Confirmation**
   - Un message de succès confirmera l'enregistrement
   - Les images seront stockées dans `/etc/linux-hello/faces/<username>/`

#### Conseils:
- 🔆 Bonne luminosité (de face, pas en contre-jour)
- 😊 Visage dégagé (cheveux qui ne couvrent pas les yeux)
- 📍 Position stable (ne pas bouger entre les captures)
- 👕 Vêtements contrastants avec le fond

### 🔐 Onglet "PAM" – Authentification Système

**Objectif:** Configurer comment Linux Hello s'intègre à l'authentification système

#### Concepts:

**PAM (Pluggable Authentication Modules)** = système d'authentification Linux

Trois niveaux de sécurité:

| Mode | Description | Utilisation |
|------|-------------|-------------|
| **Strict** | ✋ Reconnaissance faciale OBLIGATOIRE | Sécurité maximale |
| **Moyenne** | ✋ Faciale OU mot de passe | Équilibre |
| **Souple** | ✓ Faciale optionnelle, mot de passe par défaut | Confort |

#### Configuration:

1. **Voir la configuration actuelle**
   - La zone de texte affiche `/etc/pam.d/linux-hello`

2. **Appliquer une configuration prédéfinie**
   - Sélectionner le mode souhaité
   - Cliquer "Appliquer"
   - La preview s'actualise

3. **Enregistrer**
   - Cliquer "Enregistrer la configuration"
   - Entrer votre mot de passe (requis pour la sécurité)
   - La configuration est appliquée au système

#### Cas d'usage:

- **Bureaux** → Mode strict (sécurité)
- **Ordinateurs personnels** → Mode moyen
- **Développement** → Mode souple (confort)

### ⚙️ Onglet "Paramètres" – Configuration Avancée

**Objectif:** Affiner les performances et comportements

#### Sections:

##### 1️⃣ **Paramètres de la caméra**
- **Index caméra par défaut**: numéro de caméra à utiliser (0 = première)
- **Largeur vidéo**: 1280px ou 1920px (plus large = plus de détails)
- **Hauteur vidéo**: 720px ou 1080px

##### 2️⃣ **Paramètres de reconnaissance**
- **Seuil de ressemblance**: 0.0 (tout accepte) à 1.0 (très strict)
  - 0.35 = reconnaît bien
  - 0.50 = très strict
- **Confiance minimale**: 0.0 à 1.0
  - 0.80 = standard
  - 0.90 = très strict

##### 3️⃣ **Paramètres de performance**
- **Délai d'expiration**: 1-30 secondes
  - Combien de temps attendre avant d'accepter/refuser
- **Nombre max de frames**: 1-1000
  - Combien d'images analyser avant décision

##### 4️⃣ **Journalisation**
- **Niveau de journalisation**: DEBUG/INFO/WARNING/ERROR
- **Activer la journalisation**: on/off
  - Utile pour déboguer les problèmes

#### Procédure d'enregistrement:

1. Ajuster les paramètres
2. Cliquer "Enregistrer"
3. Confirmer (mot de passe requis)
4. Message de confirmation

#### Pour réinitialiser:

1. Cliquer "Réinitialiser par défaut"
2. Les valeurs par défaut sont restaurées

---

## Résolution de Problèmes

### ❌ "Impossible d'ouvrir la caméra"

**Causes possibles:**
- Caméra non connectée
- Caméra utilisée par une autre application
- Permissions insuffisantes

**Solutions:**
1. Vérifier que la caméra est connectée
2. Fermer autres applications (Skype, Zoom, etc.)
3. Redémarrer l'application

### ❌ "Permission refusée" en sauvegardant

**Cause:** Accès administrateur requis

**Solution:**
1. Vous devez être administrateur ou utiliser `sudo`
2. L'application demandera votre mot de passe

### ❌ "Reconnaissance faciale ne fonctionne pas"

**Vérifier:**
1. Avez-vous inscrit un visage? (onglet Visage)
2. La luminosité est-elle bonne?
3. Votre caméra fonctionne-t-elle?

**Affiner:**
1. Aller à ⚙️ Paramètres
2. Diminuer le "Seuil de ressemblance" (ex: 0.30 au lieu de 0.35)
3. Enregistrer et essayer de nouveau

### ❌ "La fenêtre ne s'ouvre pas"

**Essayer:**
```bash
# Depuis le terminal pour voir les erreurs
linux-hello-gui
```

---

## Fichiers de Configuration

L'application gère plusieurs fichiers système:

| Fichier | Objectif | Accès |
|---------|----------|-------|
| `/etc/linux-hello/config.json` | Paramètres (seuils, caméra, etc.) | 🔒 Admin |
| `/etc/pam.d/linux-hello` | Configuration authentification | 🔒 Admin |
| `/etc/linux-hello/faces/<user>/` | Photos faciales | 🔒 Admin |

💡 Tous les fichiers sont protégés et nécessitent l'authentification.

---

## Intégration avec Linux Hello

Cette interface graphique configure le service **linux-hello**, qui:

- Fournit l'authentification système (PAM)
- Gère le daemon de reconnaissance
- Offre une CLI pour usage avancé

**Pour plus d'informations:**
- Site: https://github.com/ebiton/Linux-Hello
- Documentation: Voir Linux-Hello/README.md

---

## Support & Assistance

### Logs

Pour déboguer, vérifier les logs du système:
```bash
sudo journalctl -u linux-hello.service -f
```

### Rapporter un bug

1. Ouvrir une issue sur GitHub: https://github.com/ebiton/Linux-Hello/issues
2. Inclure:
   - Version de l'OS (Ubuntu, Debian, etc.)
   - Version de Python
   - Description du problème
   - Logs d'erreur si possible

---

## Raccourcis Clavier

| Raccourci | Action |
|-----------|--------|
| `Alt+F4` | Fermer l'application |
| `Ctrl+Q` | Quitter |
| `Alt+F` | Menu Fichier |

---

## Conseils de Sécurité

✅ **À faire:**
- Utiliser une caméra de bonne qualité
- Bien illuminer votre visage lors de l'inscription
- Actualiser les données faciales régulièrement
- Garder votre mot de passe secret

❌ **À éviter:**
- Ne pas partager votre caméra avec d'autres utilisateurs
- Ne pas modifier directement les fichiers config
- Ne pas désactiver les checks de sécurité

---

## Foire Aux Questions

**Q: Puis-je avoir plusieurs visages enregistrés?**
A: Actuellement, un visage par utilisateur. Pour un utilisateur, les nouvelles inscriptions remplacent les anciennes.

**Q: Combien de photos dois-je enregistrer?**
A: Entre 20 et 50 photos. 30 est un bon compromis.

**Q: La reconnaissance faciale fonctionne-t-elle avec des lunettes?**
A: Oui, mais moins bien. Enregistrez avec les lunettes que vous porterez habituellement.

**Q: Puis-je utiliser une webcam USB?**
A: Oui, aucun problème. Sélectionnez-la dans le menu caméra.

---

*Guide mis à jour pour Linux Hello GUI 1.0.0*

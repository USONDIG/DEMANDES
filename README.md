# Demandes

Ébauche fonctionnelle du portail en ligne destiné aux services émetteurs pour créer et suivre leurs demandes.

## Fonctionnalités

- bouton unique de création ouvrant une fenêtre modale ;
- sélection du type de demande et des options par menus déroulants ;
- six types de demandes et formulaires contextuels ;
- coordonnées de l'établissement, du service et du demandeur ;
- référence unique, horodatage et accusé de réception simulé ;
- consultation et recherche dans les demandes envoyées ;
- historique de suivi en lecture seule ;
- conservation locale des données dans le navigateur.

## Version Streamlit

L'application principale est disponible dans `app.py`.

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Prototype HTML

Ouvrir `dist/index.html` dans un navigateur, ou servir le dossier `dist` avec un serveur HTTP local.

Cette version couvre uniquement le front-office demandeur. Les données Streamlit sont conservées pendant la session de démonstration. Le back-office des gestionnaires de compte, l'authentification, la base de données partagée, l'envoi réel de courriels et la supervision de disponibilité devront être ajoutés dans les étapes suivantes.

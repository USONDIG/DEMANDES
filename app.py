from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Demandes — Portail des services émetteurs",
    page_icon="📨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

PARIS = ZoneInfo("Europe/Paris")
TYPES = {
    "Assistance technique": {
        "icon": "⌁",
        "description": "Aide de niveau 1 à 3",
    },
    "Demande de devis": {
        "icon": "€",
        "description": "Chiffrage d’un besoin",
    },
    "Demande d’expertise": {
        "icon": "◇",
        "description": "Architecture et conseil",
    },
    "Licences et souscriptions": {
        "icon": "⌘",
        "description": "Création, renouvellement, évolution",
    },
    "Déclaration de problème": {
        "icon": "!",
        "description": "Incident ou dysfonctionnement",
    },
    "Question diverse": {
        "icon": "?",
        "description": "Question administrative ou autre",
    },
}

SAMPLE_REQUESTS = [
    {
        "id": "DEM-2026-0042",
        "subject": "Renouvellement des licences collaboratives",
        "type": "Licences et souscriptions",
        "organization": "Métropole Nord",
        "service": "Direction du numérique",
        "requester": "Camille Martin",
        "email": "camille.martin@example.fr",
        "priority": "Haute",
        "status": "En cours",
        "created": "08/09/2026 09:14",
        "description": "Renouvellement de 240 licences arrivant à échéance.",
        "history": [
            "08/09/2026 09:14 — Demande reçue et accusé envoyé",
            "08/09/2026 09:31 — Prise en charge par l’équipe dédiée",
        ],
    },
    {
        "id": "DEM-2026-0041",
        "subject": "Accompagnement à la montée de version",
        "type": "Demande d’expertise",
        "organization": "Ville de Montreuil",
        "service": "Infrastructures",
        "requester": "Alex Bernard",
        "email": "alex.bernard@example.fr",
        "priority": "Normale",
        "status": "Nouvelle",
        "created": "07/09/2026 15:42",
        "description": "Expertise sur les prérequis et les étapes de la montée de version.",
        "history": ["07/09/2026 15:42 — Demande reçue et accusé envoyé"],
    },
    {
        "id": "DEM-2026-0040",
        "subject": "Blocage de l’accès à la plateforme",
        "type": "Déclaration de problème",
        "organization": "CHU Atlantique",
        "service": "Support utilisateurs",
        "requester": "Sarah Petit",
        "email": "sarah.petit@example.fr",
        "priority": "Critique",
        "status": "En cours",
        "created": "06/09/2026 08:21",
        "description": "Plusieurs utilisateurs ne peuvent plus accéder à la plateforme.",
        "history": ["06/09/2026 08:21 — Demande reçue et accusé envoyé"],
    },
    {
        "id": "DEM-2026-0039",
        "subject": "Chiffrage de 80 licences supplémentaires",
        "type": "Demande de devis",
        "organization": "Ville de Lyon",
        "service": "Achats numériques",
        "requester": "Nora Garcia",
        "email": "nora.garcia@example.fr",
        "priority": "Haute",
        "status": "Nouvelle",
        "created": "05/09/2026 16:05",
        "description": "Demande de chiffrage pour une extension du parc de licences.",
        "history": ["05/09/2026 16:05 — Demande reçue et accusé envoyé"],
    },
    {
        "id": "DEM-2026-0038",
        "subject": "Diagnostic de performance applicative",
        "type": "Assistance technique",
        "organization": "Région Centre",
        "service": "Exploitation",
        "requester": "Jean Morel",
        "email": "jean.morel@example.fr",
        "priority": "Normale",
        "status": "Résolue",
        "created": "04/09/2026 11:32",
        "description": "Analyse de lenteurs constatées sur l’environnement de production.",
        "history": ["04/09/2026 11:32 — Demande reçue", "05/09/2026 10:12 — Résolution proposée"],
    },
    {
        "id": "DEM-2026-0037",
        "subject": "Question sur la facturation trimestrielle",
        "type": "Question diverse",
        "organization": "Département du Rhône",
        "service": "Finances",
        "requester": "Marc Leroy",
        "email": "marc.leroy@example.fr",
        "priority": "Faible",
        "status": "Clôturée",
        "created": "03/09/2026 14:18",
        "description": "Demande de précision sur le détail d’une facture trimestrielle.",
        "history": ["03/09/2026 14:18 — Demande reçue", "04/09/2026 09:02 — Demande clôturée"],
    },
    {
        "id": "DEM-2026-0036",
        "subject": "Atelier d’optimisation de l’architecture",
        "type": "Demande d’expertise",
        "organization": "Région Centre",
        "service": "Architecture",
        "requester": "Inès Roux",
        "email": "ines.roux@example.fr",
        "priority": "Haute",
        "status": "En cours",
        "created": "02/09/2026 10:10",
        "description": "Préparation d’un atelier d’optimisation de l’architecture cible.",
        "history": ["02/09/2026 10:10 — Demande reçue et accusé envoyé"],
    },
    {
        "id": "DEM-2026-0035",
        "subject": "Création de comptes de test",
        "type": "Assistance technique",
        "organization": "Métropole Nord",
        "service": "Recette",
        "requester": "Luc Dubois",
        "email": "luc.dubois@example.fr",
        "priority": "Normale",
        "status": "Résolue",
        "created": "01/09/2026 13:45",
        "description": "Création de cinq comptes pour la campagne de recette.",
        "history": ["01/09/2026 13:45 — Demande reçue", "02/09/2026 08:30 — Comptes créés"],
    },
]


def initialize_state() -> None:
    if "requests" not in st.session_state:
        st.session_state.requests = [item.copy() for item in SAMPLE_REQUESTS]
    if "success_request" not in st.session_state:
        st.session_state.success_request = None


def next_reference() -> str:
    year = datetime.now(PARIS).year
    numbers = [
        int(item["id"].split("-")[-1])
        for item in st.session_state.requests
        if item["id"].split("-")[-1].isdigit()
    ]
    return f"DEM-{year}-{max(numbers, default=0) + 1:04d}"


def render_type_fields(request_type: str) -> dict[str, str | int]:
    details: dict[str, str | int] = {}
    if request_type == "Assistance technique":
        col1, col2 = st.columns(2)
        details["Niveau sollicité"] = col1.selectbox(
            "Niveau sollicité *", ["Niveau 1", "Niveau 2", "Niveau 3"]
        )
        details["Produit ou service"] = col2.text_input(
            "Produit ou service concerné *", placeholder="Nom du produit ou service"
        )
    elif request_type == "Demande de devis":
        col1, col2 = st.columns(2)
        details["Nature du devis"] = col1.selectbox(
            "Nature du devis *", ["Licences", "Prestations", "Formation", "Autre"]
        )
        details["Volume estimé"] = col2.text_input(
            "Quantité ou volume estimé", placeholder="Ex. 250 utilisateurs"
        )
    elif request_type == "Demande d’expertise":
        col1, col2 = st.columns(2)
        details["Domaine"] = col1.selectbox(
            "Domaine d’expertise *",
            ["Architecture", "Optimisation", "Migration", "Montée de version", "Autre"],
        )
        details["Modalité"] = col2.selectbox(
            "Modalité souhaitée", ["À distance", "Sur site", "À définir"]
        )
    elif request_type == "Licences et souscriptions":
        col1, col2 = st.columns(2)
        details["Opération"] = col1.selectbox(
            "Opération demandée *",
            ["Création", "Renouvellement", "Évolution du périmètre", "Résiliation"],
        )
        details["Nombre de licences"] = col2.number_input(
            "Nombre de licences *", min_value=1, value=1
        )
    elif request_type == "Déclaration de problème":
        col1, col2 = st.columns(2)
        details["Impact"] = col1.selectbox(
            "Impact constaté *",
            ["Un utilisateur", "Plusieurs utilisateurs", "Un service complet", "Établissement complet"],
        )
        details["Début du problème"] = col2.text_input(
            "Début du problème", placeholder="JJ/MM/AAAA HH:MM"
        )
    else:
        col1, col2 = st.columns(2)
        details["Thème"] = col1.selectbox(
            "Thème *", ["Administratif", "Contractuel", "Facturation", "Livraison", "Autre"]
        )
        details["Réponse souhaitée par"] = col2.selectbox(
            "Réponse souhaitée par", ["Courriel", "Téléphone"]
        )
    return details


def submit_request(values: dict) -> None:
    now = datetime.now(PARIS)
    values.update(
        {
            "id": next_reference(),
            "status": "Nouvelle",
            "created": now.strftime("%d/%m/%Y %H:%M"),
            "history": [now.strftime("%d/%m/%Y %H:%M — Demande reçue et accusé envoyé")],
        }
    )
    st.session_state.requests.insert(0, values)
    st.session_state.success_request = values


@st.dialog("Créer une demande", width="large")
def request_dialog() -> None:
    st.caption("Sélectionnez le type de demande, puis complétez les informations utiles.")
    notice = st.empty()
    request_type = st.selectbox(
        "Type de demande *",
        list(TYPES),
        key="dialog_request_type",
        format_func=lambda value: f"{TYPES[value]['icon']}  {value}",
    )
    st.caption(TYPES[request_type]["description"])

    with st.form("request-dialog-form", clear_on_submit=True):
        st.markdown("#### Vos coordonnées")
        col1, col2 = st.columns(2)
        organization = col1.text_input("Établissement *", placeholder="Nom de l’établissement")
        service = col2.text_input("Service émetteur *", placeholder="Direction ou service")
        col3, col4 = st.columns(2)
        requester = col3.text_input("Nom du demandeur *", placeholder="Prénom et nom")
        email = col4.text_input("Adresse électronique *", placeholder="nom@etablissement.fr")

        st.markdown("#### Votre besoin")
        subject = st.text_input(
            "Objet de la demande *", placeholder="Résumez votre demande en une phrase"
        )
        details = render_type_fields(request_type)
        col5, col6 = st.columns(2)
        priority = col5.selectbox("Priorité *", ["Normale", "Haute", "Critique", "Faible"])
        wanted_date = col6.date_input("Date souhaitée", value=None)
        description = st.text_area(
            "Description détaillée *",
            placeholder="Décrivez le contexte, le résultat attendu et toute information utile.",
            height=140,
        )
        consent = st.checkbox(
            "Je confirme l’exactitude des informations saisies et accepte leur traitement."
        )
        submitted = st.form_submit_button("Envoyer ma demande →", type="primary")

    if submitted:
        required = [organization, service, requester, email, subject, description]
        if not all(str(value).strip() for value in required):
            st.error("Veuillez compléter tous les champs obligatoires.")
        elif "@" not in email or "." not in email.split("@")[-1]:
            st.error("Veuillez saisir une adresse électronique valide.")
        elif not consent:
            st.error("Veuillez confirmer l’exactitude des informations.")
        else:
            submit_request(
                {
                    "type": request_type,
                    "organization": organization,
                    "service": service,
                    "requester": requester,
                    "email": email,
                    "subject": subject,
                    "priority": priority,
                    "wanted_date": str(wanted_date or ""),
                    "description": description,
                    "details": details,
                }
            )
            item = st.session_state.success_request
            notice.success(
                f"Demande {item['id']} enregistrée. "
                f"L’accusé de réception a été préparé pour {item['email']}."
            )


def render_brand_header() -> None:
    st.markdown(
        """
        <div class="portal-header">
          <div class="portal-identity">
            <span class="portal-symbol">◆</span>
            <div><strong>demandes</strong><small>Portail des services émetteurs</small></div>
          </div>
          <span class="availability"><i></i> Service disponible</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def creation_page() -> None:
    st.markdown('<p class="eyebrow">ACCUEIL</p>', unsafe_allow_html=True)
    st.title("Vos demandes, au même endroit")
    st.write(
        "Déposez une nouvelle demande en quelques étapes. Un numéro unique et un "
        "accusé de réception sont générés immédiatement."
    )

    st.markdown(
        """
        <div class="launch-card">
          <div class="launch-copy">
            <span>NOUVELLE DEMANDE</span>
            <strong>Comment pouvons-nous vous aider ?</strong>
            <p>Assistance, devis, expertise, licences, problème ou question diverse.</p>
          </div>
          <div class="launch-orb">＋</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "Créer une demande",
        type="primary",
        use_container_width=True,
        key="open-request-dialog",
    ):
        st.session_state.success_request = None
        request_dialog()

    st.markdown("### Un parcours simple")
    col1, col2, col3 = st.columns(3)
    col1.markdown("**01 — Choisissez**  \nSélectionnez le type dans le menu déroulant.")
    col2.markdown("**02 — Décrivez**  \nComplétez uniquement les informations utiles.")
    col3.markdown("**03 — Suivez**  \nConservez la référence transmise après l’envoi.")


def follow_page() -> None:
    st.markdown('<p class="eyebrow">ESPACE DEMANDEUR</p>', unsafe_allow_html=True)
    st.title("Suivre mes demandes")
    st.write("Consultez les demandes enregistrées pendant cette session de démonstration.")
    col1, col2 = st.columns([2, 1])
    query = col1.text_input("Rechercher", placeholder="Référence, objet ou établissement")
    status = col2.selectbox("Statut", ["Tous", "Nouvelle", "En cours", "Résolue", "Clôturée"])
    filtered = [
        item
        for item in st.session_state.requests
        if (status == "Tous" or item["status"] == status)
        and (
            not query
            or query.lower()
            in f"{item['id']} {item['subject']} {item['organization']}".lower()
        )
    ]
    st.caption(f"{len(filtered)} demande{'s' if len(filtered) != 1 else ''}")
    for item in filtered:
        with st.expander(f"{item['id']} · {item['subject']} — {item['status']}"):
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Type", item["type"])
            col_b.metric("Priorité", item["priority"])
            col_c.metric("Créée le", item["created"])
            st.write(f"**Établissement :** {item['organization']} — {item['service']}")
            st.write(item["description"])
            st.markdown("**Historique**")
            for event in item["history"]:
                st.markdown(f"- {event}")
    if not filtered:
        st.info("Aucune demande ne correspond aux critères sélectionnés.")


def reporting_page() -> None:
    st.markdown('<p class="eyebrow">PILOTAGE</p>', unsafe_allow_html=True)
    st.title("Tableau de bord des demandes")
    st.write("Filtrez les indicateurs et le détail pour préparer vos points de pilotage.")

    data = pd.DataFrame(st.session_state.requests)
    data["created_dt"] = pd.to_datetime(data["created"], dayfirst=True, errors="coerce")

    with st.container(border=True):
        st.markdown('<p class="filter-title">FILTRES DU RAPPORT</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        organizations = col1.multiselect(
            "Établissement",
            sorted(data["organization"].dropna().unique()),
            placeholder="Tous les établissements",
        )
        request_types = col2.multiselect(
            "Type de demande",
            sorted(data["type"].dropna().unique()),
            placeholder="Tous les types",
        )
        col3, col4 = st.columns(2)
        statuses = col3.multiselect(
            "Statut",
            ["Nouvelle", "En cours", "Résolue", "Clôturée"],
            placeholder="Tous les statuts",
        )
        priorities = col4.multiselect(
            "Priorité",
            ["Critique", "Haute", "Normale", "Faible"],
            placeholder="Toutes les priorités",
        )

    filtered = data.copy()
    if organizations:
        filtered = filtered[filtered["organization"].isin(organizations)]
    if request_types:
        filtered = filtered[filtered["type"].isin(request_types)]
    if statuses:
        filtered = filtered[filtered["status"].isin(statuses)]
    if priorities:
        filtered = filtered[filtered["priority"].isin(priorities)]

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Demandes", len(filtered))
    kpi2.metric("Nouvelles", int((filtered["status"] == "Nouvelle").sum()))
    kpi3.metric("En cours", int((filtered["status"] == "En cours").sum()))
    kpi4.metric("Priorité critique", int((filtered["priority"] == "Critique").sum()))

    if filtered.empty:
        st.info("Aucune donnée ne correspond à cette combinaison de filtres.")
        return

    chart1, chart2 = st.columns(2)
    with chart1:
        st.markdown("#### Répartition par statut")
        status_order = ["Nouvelle", "En cours", "Résolue", "Clôturée"]
        status_data = (
            filtered["status"].value_counts().reindex(status_order, fill_value=0).rename("Demandes")
        )
        st.bar_chart(status_data, color="#5B38E8", height=280)
    with chart2:
        st.markdown("#### Répartition par type")
        type_data = filtered["type"].value_counts().sort_values().rename("Demandes")
        st.bar_chart(type_data, color="#FF8B7C", horizontal=True, height=280)

    st.markdown("### Détail des demandes")
    table = filtered[
        ["id", "subject", "type", "organization", "service", "priority", "status", "created"]
    ].rename(
        columns={
            "id": "Référence",
            "subject": "Objet",
            "type": "Type",
            "organization": "Établissement",
            "service": "Service",
            "priority": "Priorité",
            "status": "Statut",
            "created": "Créée le",
        }
    )
    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        height=min(520, 38 * (len(table) + 1)),
    )
    st.download_button(
        "Exporter la vue en CSV",
        data=table.to_csv(index=False, sep=";").encode("utf-8-sig"),
        file_name="reporting-demandes.csv",
        mime="text/csv",
    )


st.markdown(
    """
    <style>
      :root { --violet: #5b38e8; --ink: #32185f; --coral: #ff8b7c; --aqua: #45d5cf; --yellow: #ffd84d; }
      [data-testid="stHeader"] { background: transparent; }
      .stApp { background: #f2f2f5; color: #3e3157; }
      .block-container { max-width: 1220px; padding-top: 1.4rem; padding-bottom: 4rem; }
      h1, h2, h3, h4 { color: var(--ink); letter-spacing: -.035em; }
      h1 { font-size: clamp(2rem, 4vw, 3.2rem); line-height: 1.05; }
      .portal-header { display: flex; align-items: center; justify-content: space-between; gap: 1rem; background: white; border-radius: 0 0 24px 24px; padding: 1.15rem 1.4rem; margin: -1.4rem 0 1.8rem; box-shadow: 0 8px 30px rgba(52, 29, 98, .07); border-top: 4px solid var(--coral); }
      .portal-identity { display: flex; align-items: center; gap: .75rem; color: var(--ink); }
      .portal-symbol { display: grid; place-items: center; width: 2.4rem; height: 2.4rem; border-radius: 50%; background: var(--violet); color: white; font-size: 1rem; }
      .portal-identity strong, .portal-identity small { display: block; }
      .portal-identity strong { color: var(--violet); font-size: 1.35rem; line-height: 1; letter-spacing: -.04em; }
      .portal-identity small { color: #746b83; margin-top: .18rem; }
      .availability { color: var(--ink); background: #f2efff; border-radius: 999px; padding: .5rem .8rem; font-size: .78rem; font-weight: 700; }
      .availability i { display: inline-block; width: .5rem; height: .5rem; margin-right: .35rem; border-radius: 50%; background: var(--aqua); }
      .eyebrow, .filter-title { color: var(--violet); font-size: .72rem; font-weight: 850; letter-spacing: .14em; margin: 0 0 .3rem; }
      div[data-testid="stVerticalBlock"] { gap: .8rem; }
      div[data-testid="stForm"], div[data-testid="stVerticalBlockBorderWrapper"] > div { background: white; border-color: #e5e0ed !important; border-radius: 20px !important; }
      div[data-testid="stForm"] { padding: 1.5rem; box-shadow: 0 14px 38px rgba(52, 29, 98, .08); }
      .stButton button, .stFormSubmitButton button, .stDownloadButton button { border-radius: 999px; min-height: 2.8rem; font-weight: 750; border: 0; }
      .stButton button[kind="primary"], .stFormSubmitButton button[kind="primary"] { background: var(--violet); box-shadow: 0 8px 20px rgba(91, 56, 232, .22); }
      .launch-card { position: relative; overflow: hidden; display: flex; align-items: center; justify-content: space-between; gap: 2rem; color: white; background: linear-gradient(120deg, #4d24dc 0%, #6948f0 100%); border-radius: 28px; padding: 2.2rem 2.4rem; margin: 1.6rem 0 .8rem; box-shadow: 0 22px 50px rgba(80, 43, 198, .22); }
      .launch-copy { position: relative; z-index: 1; }
      .launch-copy span { color: #ddd5ff; font-size: .72rem; font-weight: 800; letter-spacing: .14em; }
      .launch-copy strong { display: block; color: white; font-size: clamp(1.35rem, 3vw, 2.1rem); margin: .45rem 0; letter-spacing: -.035em; }
      .launch-copy p { color: #eeeaff; margin: 0; }
      .launch-orb { display: grid; place-items: center; min-width: 6.2rem; height: 6.2rem; border-radius: 50%; color: var(--ink); background: var(--coral); font-size: 3rem; font-weight: 300; box-shadow: -18px 16px 0 var(--yellow); }
      [data-testid="stMetric"] { background: white; border: 0; border-radius: 18px; padding: 1rem 1.1rem; box-shadow: 0 8px 24px rgba(52, 29, 98, .06); border-top: 4px solid var(--violet); }
      [data-testid="stMetric"] label { color: #756c82; }
      [data-testid="stMetricValue"] { color: var(--ink); }
      [data-testid="stDataFrame"] { background: white; border-radius: 18px; overflow: hidden; box-shadow: 0 8px 24px rgba(52, 29, 98, .06); }
      .stTabs [data-baseweb="tab-list"] { gap: .25rem; background: white; border-radius: 999px; padding: .3rem; width: fit-content; box-shadow: 0 6px 20px rgba(52, 29, 98, .06); }
      .stTabs [data-baseweb="tab"] { border-radius: 999px; padding: .55rem 1rem; color: #6e647c; }
      .stTabs [aria-selected="true"] { background: #f1edff; color: var(--violet) !important; }
      .stTabs [data-baseweb="tab-highlight"] { display: none; }
      [data-testid="stExpander"] { background: white; border: 0; border-radius: 16px; box-shadow: 0 6px 20px rgba(52, 29, 98, .05); }
      @media (max-width: 700px) {
        .availability { display: none; }
        .launch-card { padding: 1.7rem; }
        .launch-orb { min-width: 4rem; height: 4rem; font-size: 2rem; box-shadow: -10px 10px 0 var(--yellow); }
      }
    </style>
    """,
    unsafe_allow_html=True,
)

initialize_state()
render_brand_header()
tab_create, tab_follow, tab_reporting = st.tabs(
    [
        "Créer une demande",
        f"Suivre mes demandes ({len(st.session_state.requests)})",
        "Reporting",
    ]
)
with tab_create:
    creation_page()
with tab_follow:
    follow_page()
with tab_reporting:
    reporting_page()

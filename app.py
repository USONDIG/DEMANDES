from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

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


def creation_page() -> None:
    st.markdown('<p class="eyebrow">PORTAIL DES SERVICES ÉMETTEURS</p>', unsafe_allow_html=True)
    st.title("Vos demandes, au même endroit")
    st.write(
        "Déposez une nouvelle demande en quelques étapes. Un numéro unique et un "
        "accusé de réception sont générés immédiatement."
    )

    st.markdown(
        """
        <div class="launch-card">
          <div class="launch-icon">＋</div>
          <div>
            <strong>Nouvelle demande</strong>
            <p>Assistance, devis, expertise, licences, problème ou question diverse.</p>
          </div>
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

    st.markdown("### Comment ça fonctionne ?")
    col1, col2, col3 = st.columns(3)
    col1.markdown("**1. Choisissez**  \nSélectionnez le type dans le menu déroulant.")
    col2.markdown("**2. Décrivez**  \nComplétez uniquement les informations utiles.")
    col3.markdown("**3. Suivez**  \nConservez la référence transmise après l’envoi.")


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


st.markdown(
    """
    <style>
      [data-testid="stHeader"] { background: transparent; }
      .stApp { background: #f4f6f9; color: #17253b; }
      .block-container { max-width: 1180px; padding-top: 2.2rem; padding-bottom: 4rem; }
      h1, h2, h3 { color: #17253b; letter-spacing: -.025em; }
      .eyebrow { color: #2866e8; font-size: .72rem; font-weight: 800; letter-spacing: .12em; margin: 0 0 .25rem; }
      div[data-testid="stVerticalBlock"] { gap: .8rem; }
      div[data-testid="stForm"] { background: white; border: 1px solid #dfe5ee; border-radius: 14px; padding: 1.5rem; box-shadow: 0 12px 32px rgba(19,38,67,.07); }
      .stButton button, .stFormSubmitButton button { border-radius: 9px; min-height: 2.75rem; font-weight: 700; }
      .receipt { background: #edf3ff; border: 1px solid #bfd0f7; border-radius: 12px; padding: 1.4rem; margin: 1rem 0; text-align: center; }
      .receipt span, .receipt strong, .receipt small { display: block; }
      .receipt span, .receipt small { color: #657188; }
      .receipt strong { color: #17253b; font-size: 1.7rem; margin: .3rem 0; letter-spacing: .04em; }
      .launch-card { display: flex; align-items: center; gap: 1rem; background: white; border: 1px solid #dfe5ee; border-radius: 14px; padding: 1.35rem; margin: 1.5rem 0 .75rem; box-shadow: 0 12px 32px rgba(19,38,67,.07); }
      .launch-card strong { display: block; color: #17253b; font-size: 1.05rem; }
      .launch-card p { margin: .2rem 0 0; color: #657188; }
      .launch-icon { display: grid; place-items: center; width: 3rem; height: 3rem; flex: 0 0 3rem; border-radius: 10px; color: white; background: #2866e8; font-size: 1.5rem; font-weight: 700; }
      [data-testid="stMetric"] { background: white; border: 1px solid #dfe5ee; border-radius: 9px; padding: .75rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

initialize_state()
tab_create, tab_follow = st.tabs(
    ["Créer une demande", f"Suivre mes demandes ({len(st.session_state.requests)})"]
)
with tab_create:
    creation_page()
with tab_follow:
    follow_page()

// chat.js  –  Messagerie IFRI MentorLink

const COULEURS_AV = [
  '#1a4a8a',
  '#6b3a1f',
  '#e07b39',
  '#2e7d52',
  '#7b3fa0',
  '#b04040',
];

// couleur fixe selon le nom
function couleurAvatar(nom) {
  let total = 0;
  for (let i = 0; i < nom.length; i++) total += nom.charCodeAt(i);
  return COULEURS_AV[total % COULEURS_AV.length];
}

// initiales depuis nom + prénom
function initiales(nom, prenom) {
  return (nom.charAt(0) + (prenom ? prenom.charAt(0) : '')).toUpperCase();
}

// couleur fixe pour MOI (toujours la même)
const COULEUR_MOI = '#1a4a8a';
const INI_MOI = 'Moi';

// -------------------------------------------------------
// DONNÉES DE TEST
// -------------------------------------------------------
const conversations = [
  {
    id: 1,
    nom: 'Fanou', prenom: 'Rodrigue',
    filiere: 'GL',
    dernier_msg: 'Ok donc on se retrouve mercredi à 15h ?',
    heure: '14:32',
    non_lu: 2,
    en_ligne: true,
    messages: [
      { id: 1, texte: "Salut ! Tu peux m'aider en algo ?", heure: '14:05', envoye: false, sep: "Aujourd'hui" },
      { id: 2, texte: "Bien sûr, t'as des difficultés sur quoi ?", heure: '14:08', envoye: true },
      { id: 3, texte: "Les arbres binaires surtout, les parcours…", heure: '14:10', envoye: false },
      { id: 4, texte: "C'est pas si dur quand on comprend la récursivité. Je peux t'expliquer.", heure: '14:15', envoye: true },
      { id: 5, texte: "Ouiii ça m'arrangerait trop !!", heure: '14:28', envoye: false },
      { id: 6, texte: "Ok donc on se retrouve mercredi à 15h ?", heure: '14:32', envoye: false }
    ]
  },
  {
    id: 2,
    nom: 'Agossa', prenom: 'Clarisse',
    filiere: 'IA',
    dernier_msg: 'Merci pour ton aide avec les requêtes SQL 🙏',
    heure: '11:18',
    non_lu: 0,
    en_ligne: false,
    messages: [
      { id: 1, texte: "T'as compris la jointure avec GROUP BY ?", heure: '10:42', envoye: false, sep: "Aujourd'hui" },
      { id: 2, texte: "Oui ! Tu fais le JOIN d'abord puis tu regroupes.", heure: '10:45', envoye: true },
      { id: 3, texte: "Et pour HAVING c'est pareil que WHERE ?", heure: '10:50', envoye: false },
      { id: 4, texte: "Presque, mais HAVING s'applique après le GROUP BY. WHERE c'est avant.", heure: '10:53', envoye: true },
      { id: 5, texte: "Merci pour ton aide avec les requêtes SQL 🙏", heure: '11:18', envoye: false }
    ]
  },
  {
    id: 3,
    nom: 'Vodounou', prenom: 'Séraphin',
    filiere: 'SI',
    dernier_msg: "T'as vu le cours de M. Houndji sur le ML ?",
    heure: 'Hier',
    non_lu: 0,
    en_ligne: true,
    messages: [
      { id: 1, texte: "Frère tu fais quoi pour le projet intégrateur ?", heure: '18:00', envoye: false, sep: 'Hier' },
      { id: 2, texte: "On travaille sur la messagerie, c'est pas simple lol", heure: '18:04', envoye: true },
      { id: 3, texte: "Courage 😅 moi je galère sur le matching", heure: '18:06', envoye: false },
      { id: 4, texte: "T'as vu le cours de M. Houndji sur le ML ?", heure: '18:10', envoye: false }
    ]
  },
  {
    id: 4,
    nom: 'Dossou', prenom: 'Pélagie',
    filiere: 'IM',
    dernier_msg: "Je t'envoie mes notes sur Flask ce soir",
    heure: 'Lun',
    non_lu: 1,
    en_ligne: false,
    messages: [
      { id: 1, texte: "Tu maîtrises Flask toi ?", heure: '09:00', envoye: false, sep: 'Lundi' },
      { id: 2, texte: "Un peu, j'ai fait un projet l'an dernier. Ton problème c'est quoi ?", heure: '09:05', envoye: true },
      { id: 3, texte: "Les blueprints je comprends pas trop comment ça s'organise", heure: '09:10', envoye: false },
      { id: 4, texte: "Je t'envoie mes notes sur Flask ce soir", heure: '09:15', envoye: false }
    ]
  }
];

let convActuelle = null;

// -------------------------------------------------------
// LISTE DES CONVERSATIONS
// -------------------------------------------------------
function afficherListeConvs() {
  const conteneur = document.getElementById('listeConvs');
  conteneur.innerHTML = '';

  conversations.forEach(function (conv) {
    const actif = convActuelle && convActuelle.id === conv.id ? ' active' : '';
    const couleur = couleurAvatar(conv.nom);
    const ini = initiales(conv.nom, conv.prenom);

    const item = document.createElement('div');
    item.className = 'conv-item' + actif;

    item.innerHTML =
      '<div class="av" style="background:' + couleur + '">'
      + ini
      + (conv.en_ligne ? '<span class="online-dot"></span>' : '')
      + '</div>'
      + '<div class="conv-info">'
      + '<div class="conv-nom">'
      + '<span>' + conv.prenom + ' ' + conv.nom + '</span>'
      + '<span class="conv-heure">' + conv.heure + '</span>'
      + '</div>'
      + '<div class="conv-apercu">'
      + '<span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:160px">'
      + conv.dernier_msg
      + '</span>'
      + (conv.non_lu > 0 ? '<span class="badge">' + conv.non_lu + '</span>' : '')
      + '</div>'
      + '</div>';

    item.addEventListener('click', function () { ouvrirConversation(conv.id); });
    conteneur.appendChild(item);
  });
}

// -------------------------------------------------------
// OUVRIR UNE CONVERSATION
// -------------------------------------------------------
function ouvrirConversation(convId) {
  const conv = conversations.find(function (c) { return c.id === convId; });
  if (!conv) return;

  convActuelle = conv;
  conv.non_lu = 0;

  // -- header --
  const couleur = couleurAvatar(conv.nom);
  const chAv = document.getElementById('chAv');
  chAv.style.background = couleur;
  chAv.textContent = initiales(conv.nom, conv.prenom);

  document.getElementById('chNom').textContent = conv.prenom + ' ' + conv.nom;

  // statut : en ligne en vert, hors ligne en gris (sans "depuis quand")
  const statutEl = document.getElementById('chStatut');
  if (conv.en_ligne) {
    statutEl.textContent = '● En ligne';
    statutEl.className = 'en-ligne';
  } else {
    statutEl.textContent = 'Hors ligne';
    statutEl.className = '';
  }

  document.getElementById('etatVide').style.display = 'none';
  document.getElementById('chatHeader').style.display = 'flex';
  document.getElementById('messagesZone').style.display = 'flex';
  document.getElementById('barreEnvoi').style.display = 'flex';

  document.querySelector('.page-messagerie').classList.add('conv-ouverte');

  afficherMessages(conv);
  afficherListeConvs();

  document.getElementById('champMsg').focus();
}

// -------------------------------------------------------
// AFFICHER LES MESSAGES
// -------------------------------------------------------
function afficherMessages(conv) {
  const zone = document.getElementById('messagesZone');
  zone.innerHTML = '';

  // couleur et initiales de l'interlocuteur
  const couleurLui = couleurAvatar(conv.nom);
  const iniLui = initiales(conv.nom, conv.prenom);

  conv.messages.forEach(function (msg, idx) {

    // séparateur de date
    if (msg.sep) {
      const sep = document.createElement('div');
      sep.className = 'date-sep';
      sep.textContent = msg.sep;
      zone.appendChild(sep);
    }

    const div = document.createElement('div');
    div.className = 'msg ' + (msg.envoye ? 'envoye' : 'recu');

    const dernier = (idx === conv.messages.length - 1);

    if (msg.envoye) {
      div.innerHTML =
        '<div style="display:flex;flex-direction:column;align-items:flex-end;flex:1">'
        + '<div class="bulle">' + msg.texte + '</div>'
        + '<div class="msg-meta" style="text-align:right;color:var(--gris-txt)">'
        + msg.heure
        + (dernier ? ' <span class="vu">✓✓</span>' : '')
        + '</div>'
        + '</div>'
        + '<div class="msg-av" style="background:' + COULEUR_MOI + ';margin-left:7px;flex-shrink:0">Moi</div>';

    } else {
      div.innerHTML =
        '<div class="msg-av" style="background:' + couleurLui + ';margin-right:7px;flex-shrink:0">' + iniLui + '</div>'
        + '<div style="display:flex;flex-direction:column;align-items:flex-start;flex:1">'
        + '<div class="bulle">' + msg.texte + '</div>'
        + '<div class="msg-meta" style="color:var(--gris-txt)">' + msg.heure + '</div>'
        + '</div>';
    }

    zone.appendChild(div);
  });

  zone.scrollTop = zone.scrollHeight;
}

// -------------------------------------------------------
// ENVOYER UN MESSAGE
// -------------------------------------------------------
function envoyerMessage() {
  if (!convActuelle) return;

  const champ = document.getElementById('champMsg');
  const texte = champ.value.trim();
  if (!texte) return;

  const now = new Date();
  const heure = now.getHours().toString().padStart(2, '0')
    + ':' + now.getMinutes().toString().padStart(2, '0');

  convActuelle.messages.push({ id: Date.now(), texte: texte, heure: heure, envoye: true });
  convActuelle.dernier_msg = texte;
  convActuelle.heure = heure;

  champ.value = '';
  champ.style.height = 'auto';

  afficherMessages(convActuelle);
  afficherListeConvs();

  simulerReponse();
}

// réponse auto (test seulement)
function simulerReponse() {
  const reponses = [
    'Ok merci !',
    "D'accord, je note.",
    'Ah oui je vois 👍',
    "Je regarderai ça demain.",
    "Tu peux m'envoyer un exemple ?",
    "J'avais pas pensé à ça…",
    'Super, ça marche !'
  ];

  const delai = 1400 + Math.random() * 1600;

  setTimeout(function () {
    if (!convActuelle) return;

    const now = new Date();
    const h = now.getHours().toString().padStart(2, '0')
      + ':' + now.getMinutes().toString().padStart(2, '0');

    const rep = reponses[Math.floor(Math.random() * reponses.length)];

    convActuelle.messages.push({ id: Date.now(), texte: rep, heure: h, envoye: false });
    convActuelle.dernier_msg = rep;
    convActuelle.heure = h;

    afficherMessages(convActuelle);
    afficherListeConvs();
  }, delai);
}

// -------------------------------------------------------
// FERMER LE CHAT
// -------------------------------------------------------
function fermerChat() {
  convActuelle = null;
  document.getElementById('etatVide').style.display = 'flex';
  document.getElementById('chatHeader').style.display = 'none';
  document.getElementById('messagesZone').style.display = 'none';
  document.getElementById('barreEnvoi').style.display = 'none';
  document.querySelector('.page-messagerie').classList.remove('conv-ouverte');
  afficherListeConvs();
}

// -------------------------------------------------------
// CLAVIER + TEXTAREA
// -------------------------------------------------------
function gererTouche(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    envoyerMessage();
  }
}

function ajusterHauteur(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 100) + 'px';
}

// -------------------------------------------------------
// INIT
// -------------------------------------------------------
afficherListeConvs();

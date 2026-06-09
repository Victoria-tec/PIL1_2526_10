 // profil.js  –  Page Profil IFRI MentorLink

// ──────────────────────────────────────────
// DONNÉES (dans la vraie version : fetch API)
// ──────────────────────────────────────────
const profil = {
  nom:     'Koffi',
  prenom:  'Aimé',
  email:   'aime.koffi@etud.ifri.uac.bj',
  tel:     '+229 01 00 00 00',
  filiere: 'IA',
  niveau:  'L2'
};

// labels lisibles pour filière et niveau
const labelFiliere = {
  IA:     'Intelligence Artificielle (IA)',
  IM:     'Ingénierie Mathématique (IM)',
  GL:     'Génie Logiciel (GL)',
  SE_IoT: 'Systèmes Embarqués & IoT',
  SI:     "Systèmes d'Information (SI)"
};

const labelNiveau = {
  L1: 'Licence 1 (L1)',
  L2: 'Licence 2 (L2)',
  L3: 'Licence 3 (L3)',
  M1: 'Master 1 (M1)',
  M2: 'Master 2 (M2)'
};

// ──────────────────────────────────────────
// ÉDITION INLINE (stylet)
// ──────────────────────────────────────────

// ouvre le champ d'édition pour un champ donné
function editer(champ) {
  const aff   = document.getElementById('aff'   + majuscule(champ));
  const input = document.getElementById('input' + majuscule(champ));
  const ligne = aff.parentElement;  // .champ-ligne

  aff.classList.add('cache');
  ligne.querySelector('.btn-stylet').classList.add('cache');
  input.classList.remove('cache');
  input.focus();

  // sélectionner tout le texte pour faciliter la modification
  if (input.tagName === 'INPUT') {
    input.select();
  }
}

// sauvegarde quand on quitte le champ (blur) ou appuie sur Entrée
function sauverChamp(champ) {
  const aff   = document.getElementById('aff'   + majuscule(champ));
  const input = document.getElementById('input' + majuscule(champ));
  const ligne = aff ? aff.parentElement : null;

  let valeur = input.value.trim();
  if (!valeur) {
    // si vide on remet l'ancienne valeur
    input.value = aff.textContent;
    valeur = aff.textContent;
  }

  // mettre à jour l'affichage
  if (champ === 'filiere') {
    aff.textContent = labelFiliere[input.value] || input.value;
    profil.filiere  = input.value;
    // mettre à jour la sidebar aussi
    mettreAJourSidebar();
  } else if (champ === 'niveau') {
    aff.textContent = labelNiveau[input.value] || input.value;
    profil.niveau   = input.value;
    mettreAJourSidebar();
  } else {
    aff.textContent   = valeur;
    profil[champ]     = valeur;
  }

  // si c'est nom ou prénom, mettre à jour l'avatar et la sidebar
  if (champ === 'nom' || champ === 'prenom') {
    mettreAJourSidebar();
  }

  // cacher l'input, remontrer l'affichage
  aff.classList.remove('cache');
  if (ligne) ligne.querySelector('.btn-stylet').classList.remove('cache');
  input.classList.add('cache');
}

// Entrée = sauvegarder, Echap = annuler
function enterChamp(e, champ) {
  if (e.key === 'Enter') {
    e.preventDefault();
    sauverChamp(champ);
  }
  if (e.key === 'Escape') {
    annulerEdition(champ);
  }
}

function annulerEdition(champ) {
  const aff   = document.getElementById('aff'   + majuscule(champ));
  const input = document.getElementById('input' + majuscule(champ));
  const ligne = aff.parentElement;

  aff.classList.remove('cache');
  ligne.querySelector('.btn-stylet').classList.remove('cache');
  input.classList.add('cache');
}

// ──────────────────────────────────────────
// GESTION DES TAGS (compétences / lacunes)
// ──────────────────────────────────────────

// activer le mode édition des tags (montrer les × et l'input)
// liste prédéfinie pour les checkboxes
const optionsComp = ['Python', 'Machine Learning', 'Algorithmique', 'JavaScript', 'C/C++', 'Réseaux', 'Bases de données', 'Mathématiques', 'Linux', 'Git'];
const optionsLacune = ['Réseaux', 'Bases de données', 'Algorithmique', 'Mathématiques', 'Python', 'Machine Learning', 'JavaScript', 'C/C++', 'Linux', 'Git'];

function activerTags(type) {
  const zone = document.getElementById('zone' + majuscule(type));
  const add  = document.getElementById('add'  + majuscule(type));

  // montrer les boutons ×
  zone.querySelectorAll('.tag-x').forEach(function(b) {
    b.classList.remove('cache-tag-x');
  });

  // construire la liste de checkboxes si pas encore fait
  if (!add.querySelector('.liste-checkbox')) {
    const liste = document.createElement('div');
    liste.className = 'liste-checkbox';

    const options = type === 'comp' ? optionsComp : optionsLacune;

    options.forEach(function(opt) {
      // récupérer les tags déjà cochés
      const dejaCoche = zone.querySelector('[data-val="' + opt + '"]') !== null;

      const label = document.createElement('label');
      label.className = 'checkbox-item';

      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.value = opt;
      cb.checked = dejaCoche;

      cb.addEventListener('change', function() {
        if (cb.checked) {
          // ajouter le tag s'il n'existe pas
          if (!zone.querySelector('[data-val="' + opt + '"]')) {
            const classeTag = type === 'comp' ? 'tag-comp' : 'tag-lacune';
            const span = document.createElement('span');
            span.className = 'tag ' + classeTag;
            span.setAttribute('data-val', opt);
            span.innerHTML = opt + ' <button onclick="supprimerTag(\'' + type + '\',\'' + opt + '\')" class="tag-x">×</button>';
            zone.appendChild(span);
          }
        } else {
          // supprimer le tag
          supprimerTag(type, opt);
        }
      });

      label.appendChild(cb);
      label.appendChild(document.createTextNode(' ' + opt));
      liste.appendChild(label);
    });

    add.appendChild(liste);
  }

  // montrer la zone d'ajout
  add.classList.remove('cache');
}

// ajouter un tag avec la touche Entrée
function ajouterTag(e, type) {
  if (e.key !== 'Enter') return;
  e.preventDefault();

  const input = document.getElementById('input' + majuscule(type));
  const valeur = input.value.trim();
  if (!valeur) return;

  const zone = document.getElementById('zone' + majuscule(type));
  const classeTag = type === 'comp' ? 'tag-comp' : 'tag-lacune';

  // créer le nouveau tag
  const span = document.createElement('span');
  span.className = 'tag ' + classeTag;
  span.setAttribute('data-val', valeur);
  span.innerHTML = valeur
    + ' <button onclick="supprimerTag(\'' + type + '\',\'' + valeur + '\')" class="tag-x">×</button>';

  zone.appendChild(span);
  input.value = '';
}

// supprimer un tag
function supprimerTag(type, valeur) {
  const zone = document.getElementById('zone' + majuscule(type));
  zone.querySelectorAll('.tag').forEach(function(tag) {
    if (tag.getAttribute('data-val') === valeur) {
      tag.remove();
    }
  });
}

// ──────────────────────────────────────────
// SIDEBAR : mettre à jour nom, avatar, filière
// ──────────────────────────────────────────
function mettreAJourSidebar() {
  const nomComplet = profil.prenom + ' ' + profil.nom;
  document.getElementById('sideNom').textContent = nomComplet;

  // initiales pour l'avatar
  const ini = (profil.nom.charAt(0) + profil.prenom.charAt(0)).toUpperCase();
  document.getElementById('sideAvatar').textContent = ini;

  // badge filière + niveau
  document.getElementById('sideFiliere').textContent = profil.filiere + ' — ' + profil.niveau;
}

// ──────────────────────────────────────────
// UTILITAIRE : mettre la première lettre en majuscule
// ──────────────────────────────────────────
function majuscule(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

// ──────────────────────────────────────────
// INIT
// ──────────────────────────────────────────
mettreAJourSidebar();

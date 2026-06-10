// profil.js  –  Page Profil IFRI MentorLink

const profil = window.profilData || {};

// labels lisibles pour filière et niveau
const labelFiliere = {
  IA: 'Intelligence Artificielle (IA)',
  IM: 'Internet et Multimédia (IM)',
  GL: 'Génie Logiciel (GL)',
  SE_IoT: 'Systèmes Embarqués & IoT',
  SI: "Systèmes d'Information (SI)"
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
  const aff = document.getElementById('aff' + majuscule(champ));
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
  const aff = document.getElementById('aff' + majuscule(champ));
  const input = document.getElementById('input' + majuscule(champ));
  const ligne = aff ? aff.parentElement : null;

  let valeur = input.value.trim();
  if (!valeur) {
    input.value = aff.textContent;
    valeur = aff.textContent;
  }

  // mettre à jour l'affichage
  if (champ === 'filiere') {
    aff.textContent = labelFiliere[input.value] || input.value;
    profil.filiere = input.value;
    mettreAJourSidebar();
  } else if (champ === 'niveau') {
    aff.textContent = labelNiveau[input.value] || input.value;
    profil.niveau = input.value;
    mettreAJourSidebar();
  } else {
    aff.textContent = valeur;
    profil[champ] = valeur;
  }

  if (champ === 'nom' || champ === 'prenom') {
    mettreAJourSidebar();
  }

  aff.classList.remove('cache');
  if (ligne) ligne.querySelector('.btn-stylet').classList.remove('cache');
  input.classList.add('cache');

  // envoyer au serveur
  envoyerAuServeur(champ, valeur);
}

function envoyerAuServeur(champ, valeur) {
  var body = {};
  var map = { nom: 'last_name', prenom: 'first_name', tel: 'telephone' };
  var key = map[champ] || champ;
  body[key] = valeur;
  if (window.profilSaveUrl) {
    fetch(window.profilSaveUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCSRF() },
      body: JSON.stringify(body)
    });
  }
}

function getCSRF() {
  var name = 'csrftoken';
  var cookies = document.cookie.split(';');
  for (var i = 0; i < cookies.length; i++) {
    var c = cookies[i].trim();
    if (c.indexOf(name + '=') === 0) return c.substring(name.length + 1);
  }
  return '';
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
  const aff = document.getElementById('aff' + majuscule(champ));
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
  const add = document.getElementById('add' + majuscule(type));

  // construire la liste de checkboxes si pas encore fait
  if (!add.querySelector('.liste-checkbox')) {
    const liste = document.createElement('div');
    liste.className = 'liste-checkbox';

    // si c'est lacune, on ajoute la classe orange
    if (type === 'lacune') {
      liste.classList.add('lacune-checkbox');
    }

    const options = type === 'comp' ? optionsComp : optionsLacune;

    options.forEach(function (opt) {
      const dejaCoche = zone.querySelector('[data-val="' + opt + '"]') !== null;

      const label = document.createElement('label');
      label.className = 'checkbox-item';

      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.value = opt;
      cb.checked = dejaCoche;

      label.appendChild(cb);
      label.appendChild(document.createTextNode(' ' + opt));
      liste.appendChild(label);
    });

    // bouton enregistrer
    const btnClass = type === 'comp' ? 'btn-enregistrer-comp' : 'btn-enregistrer-lacune';
    const btn = document.createElement('button');
    btn.className = btnClass;
    btn.textContent = 'Enregistrer';

    btn.addEventListener('click', function () {
      zone.innerHTML = '';

      const classeTag = type === 'comp' ? 'tag-comp' : 'tag-lacune';
      var tags = [];
      liste.querySelectorAll('input[type="checkbox"]').forEach(function (cb) {
        if (cb.checked) {
          const span = document.createElement('span');
          span.className = 'tag ' + classeTag;
          span.setAttribute('data-val', cb.value);
          span.textContent = cb.value;
          zone.appendChild(span);
          tags.push(cb.value);
        }
      });

      add.classList.add('cache');

      // sauvegarder côté serveur
      var body = {};
      var champ = type === 'comp' ? 'competences' : 'lacunes';
      body[champ] = tags.join(' ');
      if (window.profilSaveUrl) {
        fetch(window.profilSaveUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCSRF() },
          body: JSON.stringify(body)
        });
      }
    });

    add.appendChild(liste);
    add.appendChild(btn);
  }

  // montrer la zone
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
  zone.querySelectorAll('.tag').forEach(function (tag) {
    if (tag.getAttribute('data-val') === valeur) {
      tag.remove();
    }
  });
}

// ──────────────────────────────────────────
// SIDEBAR : mettre à jour nom, avatar, filière
// ──────────────────────────────────────────
function mettreAJourSidebar() {
  var prenom = profil.first_name || profil.prenom || '';
  var nom = profil.last_name || profil.nom || '';
  var nomComplet = prenom + ' ' + nom;
  document.getElementById('sideNom').textContent = nomComplet;

  var ini = (nom.charAt(0) + prenom.charAt(0)).toUpperCase();
  document.getElementById('sideAvatar').textContent = ini;

  var fil = profil.filiere || '';
  var niv = profil.niveau || '';
  document.getElementById('sideFiliere').textContent = fil + ' — ' + niv;
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

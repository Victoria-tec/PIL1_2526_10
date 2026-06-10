class PageHeader extends HTMLElement{
    connectedCallback(){
        let type = this.getAttribute("variante")
        this.innerHTML = `
                <div class="logo"><img src="/static/images/logo.png" alt="logo"></div>
                <div class="header-buttons">
                    ${type === "accueil" ? `
                            <a href="/">
                                <h3>Accueil</h3>
                            </a>
                            <a href="/comptes/inscription/">
                                <h3>S'inscrire</h3>
                            </a>
                            <a href="/comptes/connexion/">
                                <h3>Se connecter</h3>
                            </a>
                        ` : `
                            <a href="/">
                                <h3>Accueil</h3>
                            </a>
                        `}
                </div>
        `
    }
}

class PageFooter extends HTMLElement{
    connectedCallback(){
        this.innerHTML = `
                <h4>Nous contacter</h4>
                <div>
                    <a href="#">IFRIMentorLink@gmail.com</a>
                </div>
                <h4>© 2026 IFRI MentorLink - Tous droits réservés - Mentions légales - Politique de confidentialité</h4>
        `
    }
}

function getCSRF() {
    var name = "csrftoken";
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        var c = cookies[i].trim();
        if (c.indexOf(name + "=") === 0) return c.substring(name.length + 1);
    }
    return "";
}

function allerProfil(userId) {
    window.location.href = "/profil/" + userId + "/";
}

customElements.define("page-header", PageHeader)
customElements.define("page-footer", PageFooter)

/*Début config base.html*/
class Block extends HTMLElement{
    connectedCallback(){
        const titre = this.getAttribute("titre")
        const texte = this.getAttribute("texte")
        const image = this.getAttribute("image")
        this.innerHTML = `
            <h1>${titre}</h1>
            <div class="block-child">
                <p>${texte}</p>
                <img src=${image} alt="">
            </div>
        `
    }
}

customElements.define("page-block", Block)

const observer = new IntersectionObserver ((elements) =>{
    elements.forEach(element =>{
        if(element.isIntersecting){
            element.target.style.animationPlayState = "running"
        }
    })
})

document.querySelectorAll("page-block").forEach(block =>{
    observer.observe(block)
})

if(document.querySelector(".presentation-block")){
    observer.observe(document.querySelector(".presentation-block"))
}
/*Fin config base.html*/

/*Config formulaire d'inscription*/
let inscription_form = document.getElementById("inscription-form")
let pwd_submission = document.getElementById("password-submission")
let inscription_text = document.getElementById("inscription-text")

const pwd_submission_error_message = document.createElement("p")
pwd_submission_error_message.textContent = "Les mots de passe ne correspondent pas"
pwd_submission_error_message.classList.add("pwd-different")

if(inscription_form){
    inscription_form.addEventListener("submit", (e) =>{
        const pwd = document.getElementById("mot_de_passe").value
        const confirmed_pwd = document.getElementById("confirmation_mot_de_passe").value
        if (pwd !== confirmed_pwd){
            e.preventDefault()
            pwd_submission.appendChild(pwd_submission_error_message)
        }
    })
}
/*Fin config formulaire d'inscription*/

/* Gestion modification mot de passe*/
let modify_pwd_form = document.getElementById("modify-password-form")

if(modify_pwd_form){
    let step = 1

    const handleSubmit = (e) => {
        e.preventDefault()

        if(step === 1){
            step = 2
            document.querySelector("h2").textContent = "Entrez le code reçu"
            document.getElementById("mail").type = "text"
            document.getElementById("mail").placeholder = "1234"
            document.getElementById("mail").value = ""
            modify_pwd_form.querySelector("label").textContent = ""
            modify_pwd_form.querySelector("button").textContent = "Soumettre"

        } else if(step === 2){
            step = 3
            document.querySelector("h2").textContent = "Modifier le mot de passe"
            modify_pwd_form.innerHTML = `
                <div id="password-submission">
                    <label for="pwd">Nouveau mot de passe</label>
                    <input type="password" id="pwd" name="mot_de_passe" required>
                    <label for="confirm-pwd">Confirmez votre nouveau mot de passe</label>
                    <input type="password" id="confirm-pwd" name="confirmation_mot_de_passe" required>
                </div>
                <p class="pwd-different" id="pwd-error" style="display:none;">Les mots de passe ne correspondent pas</p>
                <button class="blue-button">Soumettre</button>
            `

        } else if(step === 3){
            const pwd = document.getElementById("pwd").value
            const confirmedPwd = document.getElementById("confirm-pwd").value
            const errorMsg = document.getElementById("pwd-error")

            if(pwd !== confirmedPwd){
                errorMsg.style.display = "block"
                return
            }

            window.location.href = "/hub/"
        }
    }

    modify_pwd_form.addEventListener("submit", handleSubmit)
}

/*Main Page*/
class SideBar extends HTMLElement{
    connectedCallback(){
        let user_name = this.getAttribute("user-name")
        let profil_url = this.getAttribute("profil-url") || "/comptes/profil/"
        this.innerHTML = `
                <div class="profile-pic-box"></div>
                <div style="text-align: center"><p style="margin-top: 0; margin-bottom: 0; color: white;">${user_name}</p></div>
                <div class="side-bar-button" path="${profil_url}">
                    <img src="/static/images/user-icon.png" alt="profil" class="side-bar-icon">
                    <p>Profil</p>
                </div>
                <div class="side-bar-button" path="/messagerie/">
                    <img src="/static/images/message-bubble.png" alt="messagerie" class="side-bar-icon">
                    <p>Messagerie</p>
                </div>
                <div class="side-bar-button" path="/">
                    <img src="/static/images/exit.png" alt="deconnexion" class="side-bar-icon">
                    <p>Accueil</p>
                </div>
                <p>IFRI, Nous visons l'excellence !</p>
        `
        setTimeout(() => {
            this.querySelectorAll(".side-bar-button").forEach((button) =>{
                button.addEventListener("click", ()=>{
                    window.location.href = button.getAttribute("path")
                })
            })
        }, 0)
    }
}

customElements.define("side-bar", SideBar)

let creation_btn = document.getElementById("creation-button")
if(creation_btn){
    creation_btn.addEventListener("click", () =>{
        window.location.href = "/proposals/creer/"
    })
}

class MatchBlock extends HTMLElement{
    connectedCallback(){
        let variant = this.getAttribute("variant") || ""
        let student_nom = this.getAttribute("student-nom")
        let student_prenom = this.getAttribute("student-prenom")
        let mentor_nom = this.getAttribute("mentor-nom")
        let mentor_prenom = this.getAttribute("mentor-prenom")
        let topic = this.getAttribute("topic")
        let status = this.getAttribute("status")
        let compatibility_score = this.getAttribute("compatibility-score")
        let userId = this.getAttribute("user-id")
        let matchId = this.getAttribute("match-id")

        if (variant === "suggestion") {
            this.innerHTML = `
                <div style="display: flex; height: 50%; width: 100%;">
                    <div class="block-half" data-usertype="student">
                        <div class="mini-profile-pic" data-user-id="${userId}"></div>
                        <h5>${student_nom} <br> ${student_prenom}</h5>
                    </div>
                    <div class="block-half" data-usertype="mentor">
                        <h5>${mentor_nom} <br> ${mentor_prenom}</h5>
                        <div class="mini-profile-pic" data-user-id="${userId}"></div>
                    </div>
                </div>
                <h4>--${topic}--</h4>
                <div style="display: flex; gap: 3px; align-items: center; justify-content: center; margin-top: 0">
                    <div class="compatibility" style="width: 40%; height: 27%; height: 40%; margin-top: 0"><h5>Compatibilité : ${compatibility_score}%</h5></div>
                    <button class="validation matcher-btn" data-user-id="${userId}" data-score="${compatibility_score}" data-matiere="${topic}" style="border-style: none; width: 27%; height: 40%; margin-top: 0; background-color: var(--bleu);"><h5>Matcher</h5></button>
                </div>
            `
            return;
        }

        this.innerHTML = `
                    <div style="display: flex; height: 50%; width: 100%;">
                        <div class="block-half" data-usertype="student">
                            <div class="mini-profile-pic" data-user-id="${userId}"></div>
                            <h5>${student_nom} <br> ${student_prenom}</h5>
                        </div>
                        <div class="block-half" data-usertype="mentor">
                            <h5>${mentor_nom} <br> ${mentor_prenom}</h5>
                            <div class="mini-profile-pic" data-user-id="${userId}"></div>
                        </div>
                    </div>
                    <h4>--${topic}--</h4>
                    <div style="display: flex; gap: 3px; align-items: center; justify-content: center; margin-top: 0">
                        <div class="compatibility" style="width: 40%; height: 27%; height: 40%; margin-top: 0"><h5>Compatibilité : ${compatibility_score}%</h5></div>
                        <button class="validation" data-action="${status==="validated" ? "conversation" : status==="waiting-for-validation" ? "annuler" : "valider"}" data-match-id="${matchId}" style="border-style: none; width: 27%; height: 40%; margin-top: 0"><h5>${status==="validated" ? `Conversation` : status==="waiting-for-validation" ? `Annuler` : `Valider`}</h5></button>
                        ${status !=="waiting-for-validation" ? `<button class="validation" data-action="${status==="validated" ? "terminer" : "rejeter"}" data-match-id="${matchId}" style="border-style: none; width: 27%; height: 40%; margin-top: 0; background-color: rgb(189, 22, 22);"><h5>${status==="validated" ? `Achever` : `Rejeter`}</h5></button>` : ``}
                    </div>
        `
    }
}

customElements.define("match-block", MatchBlock)

/* Click handlers */
document.body.addEventListener("click", function(e) {
    /* Profile pic → profile page */
    var pic = e.target.closest(".mini-profile-pic");
    if (pic && pic.getAttribute("data-user-id")) {
        allerProfil(pic.getAttribute("data-user-id"));
        return;
    }

    /* Matcher button (suggestion variant) */
    var matcher = e.target.closest(".matcher-btn");
    if (matcher) {
        var userId = matcher.getAttribute("data-user-id");
        var score = matcher.getAttribute("data-score");
        var matiere = matcher.getAttribute("data-matiere") || "";
        fetch("/matching/accepter/", {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRF() },
            body: JSON.stringify({ user_id: parseInt(userId), score: parseInt(score), matiere: matiere })
        }).then(function(r){ return r.json() }).then(function(d){
            window.location.href = "/hub/";
        });
        return;
    }

    /* Match-block action buttons */
    var btn = e.target.closest("[data-action]");
    if (btn && btn.getAttribute("data-match-id")) {
        var action = btn.getAttribute("data-action");
        var matchId = btn.getAttribute("data-match-id");
        if (action === "conversation") {
            window.location.href = "/messagerie/";
            return;
        }
        if (action === "valider" || action === "rejeter" || action === "terminer" || action === "annuler") {
            fetch("/matching/repondre/", {
                method: "POST",
                headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRF() },
                body: JSON.stringify({ match_id: parseInt(matchId), action: action })
            }).then(function(r){ return r.json() }).then(function(d){
                window.location.reload();
            });
        }
        return;
    }
});

/* Fin main page*/

/*Page résultats matching*/
class MatchProposition extends HTMLElement{
    connectedCallback(){
        let match_nom = this.getAttribute("nom")
        let match_prenom = this.getAttribute("prenom")
        let match_niveau = this.getAttribute("niveau")
        let score = this.getAttribute("score")
        let userId = this.getAttribute("user-id")
        this.innerHTML = `
                <div class="block-half" data-type="mentor">
                    <div class="mini-profile-pic" data-user-id="${userId}"></div>
                    <div class="match-infos">
                        <h3>${match_nom} <br> ${match_prenom}</h3>
                        <div><h5 style="font-style: italic;">${match_niveau}</h5></div>
                    </div>
                    <button class="blue-button accept-match">Matcher</button>
                    <div style="display: flex; flex-direction: column; align-items: center; width: 30%; height: 100%; margin-left: auto;">
                        <div class="circle-out">
                            <svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="100" height="100">
                                <defs>
                                    <linearGradient id="GradientColor">
                                    <stop offset="0%" stop-color="#e91e63" />
                                    <stop offset="100%" stop-color="#673ab7" />
                                    </linearGradient>
                                </defs>
                                <circle cx="50" cy="50" r="42" stroke-linecap="round" />
                            </svg>
                            <div class="circle-in">
                                <h3>${score}%</h3>
                            </div>
                        </div>
                        <h5>Compatibilité</h5>
                    </div>
                </div>
        `
        this.querySelector("circle").style.strokeDashoffset = 262-262*(score/100)
    }
}

customElements.define("match-proposition", MatchProposition)

/* Accept-match button on match-proposition (page resultats matching) */
document.body.addEventListener("click", function(e) {
    var btn = e.target.closest(".accept-match");
    if (btn) {
        var mp = btn.closest("match-proposition");
        if (!mp) return;
        var userId = mp.getAttribute("user-id");
        var score = mp.getAttribute("score");
        var matiere = mp.getAttribute("matiere") || "";
        fetch("/matching/accepter/", {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRF() },
            body: JSON.stringify({ user_id: parseInt(userId), score: parseInt(score), matiere: matiere })
        }).then(function(r){ return r.json() }).then(function(d){
            window.location.href = "/hub/";
        });
    }
});

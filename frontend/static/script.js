class PageHeader extends HTMLElement{
    connectedCallback(){
        let type = this.getAttribute("variante")
        this.innerHTML = `
                <div class="logo"><img src="../static/images/logo.png" alt="logo"></div>
                <div class="header-buttons">
                    ${type === "accueil" ? `
                            <a href="base.html">
                                <h3>Accueil</h3>
                            </a>
                            <a href="gestion_comptes/inscription.html">
                                <h3>S'inscrire</h3>
                            </a>
                            <a href="gestion_comptes/connexion.html">
                                <h3>Se connecter</h3>
                            </a>
                        ` : `
                            <a href="base.html">
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

/*Animations dynamiques à base d'un observateur*/
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

/*Gestion mot de passe*/
const pwd_submission_error_message = document.createElement("p")
pwd_submission_error_message.textContent = "Les motes de passe ne correspondent pas"
pwd_submission_error_message.classList.add("pwd-different")

const password_gestion = (pwd, confirmed_pwd, e) => {
    if (pwd !== confirmed_pwd){
        e.preventDefault()
        pwd_submission.appendChild(pwd_submission_error_message)
        return
    }else{
        pwd_submission_error_message.remove()
        e.preventDefault()

        inscription_text.textContent = "Finaliser votre inscription"
        inscription_form.innerHTML = `
            <form action="#" id="inscription-form">
                <label for="level">Votre niveau d'études</label>
                <select id="level" name="level" required>
                    <option>L1</option>
                    <option>L2</option>
                    <option>L3</option>
                    <option>M3</option>
                    <option>M2</option>
                </select>
                <label for="filiere">Votre filière</label>
                <select id="filiere" name="filiere" required>
                    <option>IA</option>
                    <option>GL</option>
                    <option>SEIoT</option>
                    <option>SI</option>
                    <option>IM</option>
                </select>
                <fieldset style="width: 80%;">
                    <legend>Vos points forts</legend>
                    <div class="points-forts-line">
                        <label for="algo">Algorithmique</label>
                        <input type="checkbox" id="algo" name="algo">

                        <label for="python">Python</label>
                        <input type="checkbox" id="python" name="python">

                        <label for="machine-learning>Machine-learning</label>
                        <input type="checkbox" id="machine-learning" name="machine-learning">

                        <label for="javascript">Javascript</label>
                        <input type="checkbox" id="javascript" name="javascript">

                        <label for="c/c++">C/C++</label>
                        <input type="checkbox" id="c/c++" name="c/c++">

                        <label for="reseaux">Réseaux</label>
                        <input type="checkbox" id="reseaux" name="reseaux">

                        <label for="base de données">Base de données</label>
                        <input type="checkbox" id="base de données" name="base de données">

                        <label for="mathematiques">Mathématiques</label>
                        <input type="checkbox" id="mathematiques" name="mathematiques">

                        <label for="linux">Linux</label>
                        <input type="checkbox" id="linux" name="linux">

                        <label for="git">Git</label>
                        <input type="checkbox" id="git" name="git">
                    </div>
                </fieldset>
                <fieldset style="width: 80%;">
                    <legend>Vos points faibles</legend>
                    <div class="points-forts-line">
                        <label for="algo">Algorithmique</label>
                        <input type="checkbox" id="algo" name="algo">

                        <label for="python">Python</label>
                        <input type="checkbox" id="python" name="python">

                        <label for="machine-learning>Machine-learning</label>
                        <input type="checkbox" id="machine-learning" name="machine-learning">

                        <label for="javascript">Javascript</label>
                        <input type="checkbox" id="javascript" name="javascript">

                        <label for="c/c++">C/C++</label>
                        <input type="checkbox" id="c/c++" name="c/c++">

                        <label for="reseaux">Réseaux</label>
                        <input type="checkbox" id="reseaux" name="reseaux">

                        <label for="base de données">Base de données</label>
                        <input type="checkbox" id="base de données" name="base de données">

                        <label for="mathematiques">Mathématiques</label>
                        <input type="checkbox" id="mathematiques" name="mathematiques">

                        <label for="linux">Linux</label>
                        <input type="checkbox" id="linux" name="linux">

                        <label for="git">Git</label>
                        <input type="checkbox" id="git" name="git">
                    </div>
                </fieldset>

                <button class="blue-button" id="submission-button">Soumettre</button>
            </form>
        `
        
        document.getElementById("inscription-form").addEventListener("submit", (e) => {
            e.preventDefault()
            window.location.href = "../hub.html"
        })
    }
}

if(pwd_submission){
    let submitted_password = ""
    let confirmed_submitted_password = ""

    document.getElementById("pwd").addEventListener("input", () =>{
        submitted_password = document.getElementById("pwd").value
    })

    document.getElementById("confirm-pwd").addEventListener("input", () =>{
        confirmed_submitted_password = document.getElementById("confirm-pwd").value
    })

    inscription_form.addEventListener("submit", (e) =>{
        password_gestion(submitted_password, confirmed_submitted_password, e)
    })
}

/*Fin gestion mot de passe*/


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

            window.location.href = "../hub.html"
        }
    }

    modify_pwd_form.addEventListener("submit", handleSubmit)
}

/*Main Page*/

class SideBar extends HTMLElement{
    connectedCallback(){
        let user_name = this.getAttribute("user-name")
        this.innerHTML = `
                <div class="profile-pic-box"></div>
                <div style="text-align: center"><p style="margin-top: 0; margin-bottom: 0; color: white;">${user_name}</p></div>
                <div class="side-bar-button" path="#">
                    <img src="../static/images/message-bubble.png" alt="profil" class="side-bar-icon">
                    <p>Profil</p>
                </div>
                <div class="side-bar-button" path="./chat.html">
                    <img src="../static/images/user-icon.png" alt="messagerie" class="side-bar-icon">
                    <p>Messagerie</p>
                </div>
                <div class="side-bar-button" path="./base.html">
                    <img src="../static/images/exit.png" alt="deconnexion" class="side-bar-icon">
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
        window.location.href = "formulaire.html"
    })

}

class MatchBlock extends HTMLElement{
    connectedCallback(){
        let student_nom = this.getAttribute("student-nom")
        let student_prenom = this.getAttribute("student-prenom")
        let student_pic = this.getAttribute("student-pic")
        let mentor_nom = this.getAttribute("mentor-nom")
        let mentor_prenom = this.getAttribute("mentor-prenom")
        let mentor_pic = this.getAttribute("mentor-pic")
        let topic = this.getAttribute("topic")
        let status = this.getAttribute("status")
        let compatibility_score = this.getAttribute("compatibility-score")
        this.innerHTML = `
                    <div style="display: flex; height: 50%; width: 100%;">
                        <div class="block-half" data-usertype = "student">
                            <div class="mini-profile-pic"></div>
                            <h5>${student_nom} <br> ${student_prenom}</h5>
                        </div>
                        <div class="block-half" data-usertype="mentor">
                            <h5>${mentor_nom} <br> ${mentor_prenom}</h5>
                            <div class="mini-profile-pic"></div>
                        </div>
                    </div>
                    <h4>--${topic}--</h4>
                    <div style="display: flex; gap: 3px; align-items: center; justify-content: center; margin-top: 0">
                        <div class="compatibility" style="width: 40%; height: 27%; height: 40%; margin-top: 0"><h5>Compatibilité : ${compatibility_score}%</h5></div>
                        <button class="validation" style="border-style: none; width: 27%; height: 40%; margin-top: 0"><h5>${status==="validated" ? `Conversation` : status==="waiting-for-validation" ? `Annuler` : `Valider`}</h5></button>
                        ${status !=="waiting-for-validation" ? `<button class="validation" style="border-style: none; width: 27%; height: 40%; margin-top: 0; background-color: rgb(189, 22, 22);"><h5>${status==="validated" ? `Achever` : `Rejeter`}</h5></button>` : ``}
                    </div>
        `
    }
}

customElements.define("match-block", MatchBlock)

document.body.addEventListener("click", (e) => {
    if(e.target.classList.contains("mini-profile-pic")){
        window.location.href = "profil-visiteur.html"
    }
})

/* Fin main page*/

/*Page formulaire de soumission*/

let creation_form = document.getElementById("formulaire-offre-demande")
if(creation_form){
    creation_form.addEventListener("submit", () =>{
        window.location.href = "resultats_matching.html"
    })
}

/*Page résultats matching*/

class MatchProposition extends HTMLElement{
    connectedCallback(){
        let match_nom = this.getAttribute("nom")
        let match_prenom = this.getAttribute("prenom")
        let match_niveau = this.getAttribute("niveau")
        let score = this.getAttribute("score")
        this.innerHTML = `
                <div class="block-half" data-type="mentor">
                    <div class="mini-profile-pic"></div>
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

        setTimeout(() => {
            this.querySelector(".accept-match").addEventListener("click", () =>{
                window.location.href = "hub.html"
            })
        }, 0)

    }
}

customElements.define("match-proposition", MatchProposition)
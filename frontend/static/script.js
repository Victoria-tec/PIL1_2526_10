class PageHeader extends HTMLElement{
    connectedCallback(){
        let type = this.getAttribute("variante")
        this.innerHTML = `
                <div><img class="logo" src="../static/images/logo.png" alt="logo"></div>
                <div class="header-buttons">
                    <a href="#">
                        <h3>Profil</h3>
                    </a>
                    ${type === "accueil" ? `
                            <a href="gestion_comptes/inscription.html">
                                <h3>S'inscrire</h3>
                            </a>
                            <a href="connexion.html">
                                <h3>Se connecter</h3>
                            </a>
                        ` : `
                            <a href="base.html" id="deconnexion-button">
                                <h3>Déconnexion</h3>
                            </a>
                        `}
                    <a href="base.html">
                        <h3>Accueil</h3>
                    </a>
                </div>
        `
    }
}

class PageFooter extends HTMLElement{
    connectedCallback(){
        this.innerHTML = `
                <h4>Nous contacter</h4>
                <div>
                    <a href="#">WhatsApp</a>
                    <a href="#">Facebook</a>
                </div>
                <h4>Copyright IFRI - 2026</h4>
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

/*Gestion mot de passe*/
const pwd_submission_error_message = document.createElement("p")
pwd_submission_error_message.textContent = "Les motes de passe ne correspondent pas"
pwd_submission_error_message.classList.add("pwd-different")

const password_gestion = (pwd, confirmed_pwd, e) => {
    if (pwd !== confirmed_pwd){
        pwd_submission.appendChild(pwd_submission_error_message)
        e.preventDefault()
    }else{
        pwd_submission_error_message.remove()
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

    inscription_form.querySelector(".blue-button").addEventListener("click", (e) =>{
        password_gestion(submitted_password, confirmed_submitted_password, e)
    })
}

/*Fin config formulaire d'inscription*/

/* Gestion modification mot de passe*/
let modify_pwd_form = document.getElementById("modify-password-form")

if(modify_pwd_form){
    let step = 1
    modify_pwd_form.addEventListener("submit", (e) =>{
        e.preventDefault()

        if(step === 1){
            document.querySelector("h1").textContent = "Entrez le code à 4 chiffres reçu"
            document.getElementById("mail").type = "text"
            document.getElementById("mail").placeholder = "1234"
            document.getElementById("mail").value = ""
            modify_pwd_form.querySelector("label").textContent = ""
            modify_pwd_form.querySelector("button").textContent = "Soumettre"

            modify_pwd_form.querySelector("button").addEventListener("click", () =>{
                step += 1
            })
        }else{
            document.querySelector("h1").textContent = "MODIFIER MOT DE PASSE"
            modify_pwd_form.innerHTML = `
                    <div id="password-submission">
                        <label for="pwd">Nouveau mot de passe</label>
                        <input type="password" id="pwd" name="mot_de_passe" required>

                        <label for="confirm-pwd">Confirmez votre nouveau mot de passe</label>
                        <input type="password" id="confirm-pwd" name="confirmation_mot_de_passe" required>
                    </div>

                    <button class="blue-button">Soumettre</button>
            `
        }
    })
}

/*Main Page*/

class SideBar extends HTMLElement{
    connectedCallback(){
        let user_name = this.getAttribute("user-name")
        this.innerHTML = `
                <div class="profile-pic-box"></div>
                <div style="text-align: center"><p style="margin-top: 0; margin-bottom: 0; color: white;">${user_name}</p></div>
                <div class="brown-button">
                    <img src="../static/images/message-bubble.png" alt="messagerie" class="side-bar-icon">
                    <p>Messagerie</p>
                </div>
                <div class="brown-button">
                    <img src="../static/images/help.png" alt="messagerie" class="side-bar-icon">
                    <p>Demandes</p>
                </div>
                <div class="brown-button">
                    <img src="../static/images/annonce.png" alt="messagerie" class="side-bar-icon">
                    <p>Annonces</p>
                </div>
                <p>IFRI, Nous visons l'excellence !</p>
        `
    }
}

customElements.define("side-bar", SideBar)

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
                    <h4><a href="#">--${topic}--</a></h4>
                    <div style="display: flex; gap: 3px; align-items: center; justify-content: center; margin-top: 0">
                        <div class="compatibility" style="width: 40%; height: 27%; height: 40%; margin-top: 0"><h5>Compatibilité : ${compatibility_score}%</h5></div>
                        <button class="validation" style="border-style: none; width: 27%; height: 40%; margin-top: 0"><h5>${status==="validated" ? `Conversation` : `Valider`}</h5></button>
                        <button class="validation" style="border-style: none; width: 27%; height: 40%; margin-top: 0; background-color: rgb(189, 22, 22);"><h5>${status==="validated" ? `Achever` : `Rejeter`}</h5></button>
                    </div>
        `
    }
}

customElements.define("match-block", MatchBlock)

/* Fin main page*/
class PageHeader extends HTMLElement{
    connectedCallback(){
        this.innerHTML = `
                <div><img class="logo" src="../static/images/logo.png" alt="logo"></div>
                <div class="header-buttons">
                    <a href="#">
                        <h3>Profil</h3>
                    </a>
                    <a href="inscription.html">
                        <h3>S'inscrire</h3>
                    </a>
                    <a href="connexion.html">
                        <h3>Se connecter</h3>
                    </a>
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
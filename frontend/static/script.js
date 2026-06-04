class PageHeader extends HTMLElement{
    connectedCallback(){
        this.innerHTML = `
                <div><img class="logo" src="../static/images/logo.png" alt="logo"></div>
                <div class="header-buttons">
                    <a href="#">
                        <img class="header-icon" src="../static/images/user.png" alt="profil">
                        <h3>Profil</h3>
                    </a>
                    <a href="#">
                        <h3>S'inscrire</h3>
                    </a>
                    <a href="#">
                        <h3>Se connecter</h3>
                    </a>
                    <a href="#">
                        <h3>Statistiques</h3>
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

customElements.define("page-header", PageHeader)
customElements.define("page-footer", PageFooter)
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

observer.observe(document.querySelector(".presentation-block"))
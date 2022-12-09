var ready = (callback) => {
    if (document.readyState != "loading") callback();
    else document.addEventListener("DOMContentLoaded", callback);
}
ready(() => {
    document.querySelector(".header").style.height = window.innerHeight + "px";
})

class Navbar extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `<nav class="navbar navbar-expand-md">
        <a class="title_library" href="index.html">1 Public Library</a>
        <button class="navbar-toggler navbar-dark" type="button" data-toggle="collapse" data-target="#main-navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="main-navigation">
            <ul class="navbar-nav">
                <li class="nav_item">
                    <a class="nav-link" href="explore.html">Explore</a>
                </li>
                <li class="nav_item">
                    <a class="nav-link" href="my_transactions.html">My Transactions</a>
                </li>
                <li class="nav_item">
                    <a class="nav-link" href="admin.html">Admin</a>
                </li>
                <li class="nav_item">
                    <a class="nav-link" href="contact.html">Contact Us</a>
                </li>
            </ul>
        </div>
    </nav>`;
    }
}
customElements.define('navbar-element', Navbar);

class BackgroundImage extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `<div class="bg-image" 
        style="background-image: url('images/background-min.png');
        background-size: cover;
        background-position: center;
        margin: 0;
        padding: 0;">
   </div>`
    }
}
customElements.define('background-image', BackgroundImage);

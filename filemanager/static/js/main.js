const xhr = new XMLHttpRequest();
const html = document.getElementsByTagName("html")[0]
const theme = document.getElementById("theme-input")
const light = document.getElementById("light")
const dark = document.getElementById("dark")
const themes = {light: "dark", dark: "light"}


function changeTheme(){
    let form = {theme: theme.checked}
    xhr.open("POST", "/theme")
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.send(JSON.stringify(form));
    setTimeout(() => { html.className = themes[html.className]; }, 250);
}

function closeNotify(event) {
    let target = event.path[2];
    target.className = target.className.replace("fadeIn", "fadeOut");
    setTimeout(() => {
        target.parentNode.removeChild(target);
    }, 1000)
}



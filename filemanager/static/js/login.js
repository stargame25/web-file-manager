function loginState(state=false){
    let username = document.getElementById("username-input");
    let password = document.getElementById("password-input");
    let button = document.getElementById("submit");
    username.disabled = state;
    password.disabled = state;
    button.disabled = state;
}

function doLogin() {
    let username = document.getElementById("username-input");
    let password = document.getElementById("password-input");
    loginState(true);
}
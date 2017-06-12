function change(button_name) {
    var elem = document.getElementsByName(button_name);
    if (elem.innerHTML =="Link") elem.innerHTML = "Unlink";
    else elem.innerHTML = "Link";
}

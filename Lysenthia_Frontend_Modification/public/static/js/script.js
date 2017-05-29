function change(button_name) // no ';' here
{
    var elem = document.getElementsByName(button_name);
    if (elem.innerHTML =="Link") elem.innerHTML = "Unlink";
    else elem.innerHTML = "Link";
}
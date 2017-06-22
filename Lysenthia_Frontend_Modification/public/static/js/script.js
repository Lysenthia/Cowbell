function change(button_name) {
    var elem = document.getElementsByName(button_name);
    if (elem.innerHTML =="Link") elem.innerHTML = "Unlink";
    else elem.innerHTML = "Link";
}

for(i=0;i<document.getElementsByClassName("individualslider").length;i++) {
	console.log("Slider" + i)
}
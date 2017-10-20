//Live Playback Script
function play_preview(){
	var slider_values = [];
	for (i = 0; i < document.getElementsByClassName('individualslider').length; i++) {
		slider_values.push(document.getElementById("slider" + i).value);
	}
	var slider_string = slider_values.join('');
	$.getJSON($SCRIPT_ROOT + "/preview", {
		param_send: slider_string
	}, 
	function(data){
		var audio_source = data.previewname
		document.getElementById('preview_audio').src = audio_source;
		preview_audio.play();
	})
}
window.addEventListener("DOMContentLoaded", function(event) {
	document.getElementById("play_button").addEventListener("click", play_preview);
})

window.addEventListener("DOMContentLoaded", function(event) {
	document.getElementById("stop_button").addEventListener("click", stop_preview);
});
function stop_preview(){
	preview_audio.pause();
	preview_audio.currentTime = 0;
}


// Link Button Script
function linkNote(linkButton) {
	console.log("changed" + linkButton);
};
window.addEventListener("DOMContentLoaded", function(event) {
	for (var i = 0; i < document.getElementsByClassName('synthbuttons').length; i++) {
		console.log(i)
		document.getElementById("linkbutton" + i).addEventListener('change', function() {
			if(this.checked) {
				console.log(this.id)
				var slider_number = Number(this.id.replace("linkbutton", ""))
				var value_to_place = document.getElementById("slider" + slider_number).value
				document.getElementById("slider" + (slider_number + 1)).value = value_to_place
				document.getElementById("slider" + (slider_number + 1)).disabled = true
				$(document).on('input', '#slider' + (slider_number), function() {
					$('#slider' + (slider_number + 1)).val($('#slider' + (slider_number)).html( $(this).val() ));
				});

			} else {
				console.log(this.id)
				var slider_number = Number(this.id.replace("linkbutton", ""))
				document.getElementById("slider" + (slider_number + 1)).disabled = false
			}
		})
	}
});

$('#synthform').submit(function() {
  for (var i = 0; i < document.getElementsByClassName("synthbuttons").length; i++) {
  if (document.getElemtById("linkbutton" + i).checked) {
      document.getElementById("linkbutton" + i + "Hidden").disabled = true;
  }
  };
  for (var i = 0; i < document.getElementsByClassName("individualslider").length; i++) {
      document.getElemtById("slider" + i).disabled = false
}});
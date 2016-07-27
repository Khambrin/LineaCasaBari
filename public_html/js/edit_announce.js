
function editannForm() {// aggiungi annuncio

	var titolo  = editannounceform.titolo.value;
	var testo  = editannounceform.testo.value;
			
	if(titolo==false){ document.getElementById("edittitolo").innerHTML = "Completa il campo titolo"; return false;}
	if(testo==false){ document.getElementById("edittesto").innerHTML = "Completa il campo testo"; return false;}
}

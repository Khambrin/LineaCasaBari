
function newannForm() {// aggiungi annuncio

	var titolo  = announceform.titolo.value;
	var testo  = announceform.testo.value;
			
	if(titolo==false){ document.getElementById("newtitolo").innerHTML = "Completa il campo titolo"; return false;}
	if(testo==false){ document.getElementById("newtesto").innerHTML = "Completa il campo testo"; return false;}
}

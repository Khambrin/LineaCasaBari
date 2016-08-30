
function newReviewForm() {// aggiungi annuncio

	var titoloReview  = addReviewForm.titolo.value;
	var nomeReview  = addReviewForm.nome.value;
	var testoReview  = addReviewForm.testo.value;

	if(titoloReview==false){ document.getElementById("titolo_error").innerHTML = "Inserisci un titolo"; }
	else{document.getElementById("titolo_error").innerHTML = "";}
	if(nomeReview==false){ document.getElementById("nome_error").innerHTML = "Inserisci un nome"; }
	else{document.getElementById("titolo_error").innerHTML = "";}
	if(testoReview==false){ document.getElementById("testo_error").innerHTML = "Inserisci una testo"; }
	else{document.getElementById("testo_error").innerHTML = ""; }

	if(titoloReview==false|nomeReview==false|testoReview==false){return false;}
	else{return true;} 
}

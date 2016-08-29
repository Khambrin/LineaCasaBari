
function prForm() {//form aggiunta prodotto


	var nome1  = productform.nome.value;
	var descrizione1  = productform.descrizione.value;
	var prezzo1  = productform.prezzo.value;
	
			
	if(nome1==false){ document.getElementById("newnome").innerHTML = "Inserisci un nome";}
	else{document.getElementById("newnome").innerHTML = "";}
	if(descrizione1==false){ document.getElementById("newdescrizione").innerHTML = "Inserisci una descrizione";}
	else{document.getElementById("newdescrizione").innerHTML = "";}


	var rgprezzo = /^[0-9]+(\,[0-9]{2})?$/;
	var dprezzo = rgprezzo.test(prezzo1);
	if(dprezzo==false) {document.getElementById("formatoprezzo").innerHTML = "Inserisci un prezzo valido, ad esempio 1,00 oppure 12";}
	else{document.getElementById("formatoprezzo").innerHTML = "";}

	if(nome1==false|descrizione1==false|dprezzo==false){return false;}
    	return true;
}

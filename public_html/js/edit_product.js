
function editProdottoFunzione() {//form aggiunta prodotto


	var nome1  = editProdottoForm.nome.value;
	var descrizione1  = editProdottoForm.descrizione.value;
	var prezzo1  = editProdottoForm.prezzo.value;
	
			
	if(nome1==false){ document.getElementById("editNome").innerHTML = "Inserisci un nome";}
	else{document.getElementById("editNome").innerHTML = "";}
	if(descrizione1==false){ document.getElementById("editDescrizione").innerHTML = "Inserisci una descrizione";}
	else{document.getElementById("editDescrizione").innerHTML = "";}


	var rgprezzo = /^[0-9]+(\,[0-9]{2})?$/;
	var dprezzo = rgprezzo.test(prezzo1);
	if(dprezzo==false){ document.getElementById("editFormatoPrezzo").innerHTML = "Inserisci un prezzo valido, ad esempio 1,00 oppure 12";}
	else{document.getElementById("editFormatoPrezzo").innerHTML = "";}

	if(nome1==false|descrizione1==false|dprezzo==false|prezzo1==false){return false;}
    	else{return true;}
}

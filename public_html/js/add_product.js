
function prForm() {//form aggiunta prodotto



	var prezzo1  = productform.prezzo.value;



	var rgprezzo = /^[0-9]*\,[0-9]{2,2}$/ ;
	var dprezzo = rgprezzo.test(prezzo1);
	if(dprezzo==false) {
		document.getElementById("formatoprezzo").innerHTML = "Inserisci un prezzo valido, ad esempio 1,00 oppure 12";
        	return false;
	}


    	return true;
}

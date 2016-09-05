
function editForm() {// modifica indirizzo


	var via1  = editaddressform.via.value;
	var num1  = editaddressform.numero.value;
	var cit1  = editaddressform.citta.value;
	var pro1  = editaddressform.provincia.value;//2 letters
	var cap1  = editaddressform.cap.value;//5 digits


	if(via1==false){ document.getElementById("editvia").innerHTML = "Inserisci una via"; }
	else{document.getElementById("editvia").innerHTML = "";}
	if(num1==false){ document.getElementById("editnum").innerHTML = "Inserisci un numero civico"; }
	else{document.getElementById("editnum").innerHTML = "";}
	if(cit1==false){ document.getElementById("editcit").innerHTML = "Inserisci una citt&agrave;"; }
	else{document.getElementById("editcit").innerHTML = "";}

	var rgprov = /^([A-Za-z]){2,2}$/ ;
	var dprov = rgprov.test(pro1);
	if(dprov==false) {document.getElementById("edittwoprov").innerHTML = "Inserisci una provincia valida, ad esempio PD";}
	else{document.getElementById("edittwoprov").innerHTML = "";}

  
			
	var rgcap = /^([0-9]){5,5}$/ ;
	var dcap = rgcap.test(cap1);
	if(dcap==false) {document.getElementById("editdigitscap").innerHTML = "Inserisci un CAP valido";}
	else{document.getElementById("editdigitscap").innerHTML = "";}


	if(via1==false|num1==false|cit1==false|dprov==false|dcap==false){return false;}
    	return true;
}

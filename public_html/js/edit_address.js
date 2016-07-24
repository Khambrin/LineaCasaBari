
function editForm() {// modifica indirizzo


	var via1  = editaddressform.via.value;
	var num1  = editaddressform.numero.value;
	var cit1  = editaddressform.citta.value;
	var pro1  = editaddressform.provincia.value;//2 letters
	var cap1  = editaddressform.cap.value;//5 digits

    	var lpro1 = pro1.length;
	var lcap1 = cap1.length;
			
	if(via1==false){ document.getElementById("editvia").innerHTML = "Inserisci una via"; return false;}
	if(num1==false){ document.getElementById("editnum").innerHTML = "Inserisci un numero civico"; return false;}
	if(cit1==false){ document.getElementById("editcit").innerHTML = "Inserisci una città"; return false;}

	var rgprov = /^([A-Za-z]){2,2}$/ ;
	var dprov = rgprov.test(pro1);
	if(dprov==false) {
		document.getElementById("edittwoprov").innerHTML = "Inserisci una provincia valida, ad esempio PD";
        	return false;
	}

  
			
	var rgcap = /^([0-9]){5,5}$/ ;
	var dcap = rgcap.test(cap1);
	if(dcap==false) {
		document.getElementById("editdigitscap").innerHTML = "Inserisci un CAP valido";
        	return false;
	}
    	return true;
}

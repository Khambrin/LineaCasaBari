
function addForm() {// aggiungi indirizzo

	var via1  = addressform.via.value;
	var num1  = addressform.numero.value;
	var cit1  = addressform.citta.value;
	var pro1  = addressform.provincia.value;//2 letters
	var cap1  = addressform.cap.value;//5 digits

    	var lpro1 = pro1.length;
	var lcap1 = cap1.length;
			
	if(via1==false){ document.getElementById("addvia").innerHTML = "Inserisci una via"; return false;}
	if(num1==false){ document.getElementById("addnum").innerHTML = "Inserisci un numero civico"; return false;}
	if(cit1==false){ document.getElementById("addcit").innerHTML = "Inserisci una città"; return false;}

	var rgprov = /^([A-Za-z]){2,2}$/ ;
	var dprov = rgprov.test(pro1);
	if(dprov==false) {
		document.getElementById("addtwoprov").innerHTML = "Inserisci una provincia valida, ad esempio PD";
        	return false;
	}

  
			
	var rgcap = /^([0-9]){5,5}$/ ;
	var dcap = rgcap.test(cap1);
	if(dcap==false) {
		document.getElementById("adddigitscap").innerHTML = "Inserisci un CAP valido";
        	return false;
	}
    	return true;
}

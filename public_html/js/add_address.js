
function addForm() {// aggiungi indirizzo





	var pro1  = addressform.provincia.value;//2 letters
	var cap1  = addressform.cap.value;//5 digits

    	var lpro1 = pro1.length;
	var lcap1 = cap1.length;
			


	var rgprov = /^([A-Za-z]){2,2}$/ ;
	var dprov = rgprov.test(pro1);
	if(dprov==false) {
		document.getElementById("twoprov").innerHTML = "Inserisci una provincia valida, ad esempio PD";
        	return false;
	}

  
			
	var rgcap = /^([0-9]){5,5}$/ ;
	var dcap = rgcap.test(cap1);
	if(dcap==false) {
		document.getElementById("digitscap").innerHTML = "Inserisci un CAP valido";
        	return false;
	}
    	return true;
}

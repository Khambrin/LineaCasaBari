
function addForm() {// aggiungi indirizzo

	var via1  = addressform.via.value;
	var num1  = addressform.numero.value;
	var cit1  = addressform.citta.value;
	var pro1  = addressform.provincia.value;//2 letters
	var cap1  = addressform.cap.value;//5 digits

			
	if(via1==false){ document.getElementById("addvia").innerHTML = "Inserisci una via"; }
	else{document.getElementById("addvia").innerHTML = "";}
	if(num1==false){ document.getElementById("addnum").innerHTML = "Inserisci un numero civico"; }
	else{document.getElementById("addnum").innerHTML = "";}
	if(cit1==false){ document.getElementById("addcit").innerHTML = "Inserisci una citt&agrave;"; }
	else{document.getElementById("addcit").innerHTML = ""; }

	var rgprov = /^([A-Za-z]){2,2}$/ ;
	var dprov = rgprov.test(pro1);
	if(dprov==false) {
		document.getElementById("addtwoprov").innerHTML = "Inserisci una provincia valida, ad esempio PD";
        	
	}
	else{document.getElementById("addtwoprov").innerHTML = "";}

  
			
	var rgcap = /^([0-9]){5,5}$/ ;
	var dcap = rgcap.test(cap1);
	if(dcap==false) {
		document.getElementById("adddigitscap").innerHTML = "Inserisci un CAP valido";
        	
	}
	else{document.getElementById("adddigitscap").innerHTML = "";}
	if(via1==false|num1==false|cit1==false|dprov==false|dcap==false){return false;}
    	return true;
}

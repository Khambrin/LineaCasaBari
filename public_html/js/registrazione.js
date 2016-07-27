
function validateForm() {
    	
	var nom  = recform.nome.value;
	var cog  = recform.cognome.value;
    	var ema  = recform.email.value;
	var str  = recform.password.value;
	var cfp  = recform.conf_password.value;

	if(nom==false){ document.getElementById("nom").innerHTML = "Completare il campo Nome"; }
	else{document.getElementById("nom").innerHTML = "";}
	if(cog==false){ document.getElementById("cog").innerHTML = "Completare il campo Cognome"; }
	else{document.getElementById("cog").innerHTML = "";}
	if(ema==false){ document.getElementById("ema").innerHTML = "Completare il campo Email"; }
	else{document.getElementById("ema").innerHTML = "";}

	var rgxstr = /^[^\s@]+@[^\s@]+\.[^\s@]+$/ ; 
	var gem = rgxstr.test(ema);
	if(gem==false){
		document.getElementById("emailrec").innerHTML = "Email non valida"; 
		//return false;
	}
	else{document.getElementById("emailrec").innerHTML = "";}
	
	if(str==false){ document.getElementById("cem").innerHTML = "Completare il campo Password"; }
	else{document.getElementById("cem").innerHTML = "";}

	

	var n = str.length;
	
    	if(n<8) {
		document.getElementById("shortpassword").innerHTML = "Password troppo corta, minimo 8 caratteri";
		//document.getElementById("longpassword").innerHTML = "";
        	//return false;
    	}
	else{ document.getElementById("shortpassword").innerHTML = "";}
	if(n>20) {
		//document.getElementById("shortpassword").innerHTML = "";
		document.getElementById("longpassword").innerHTML = "Password troppo lunga, massimo 20 caratteri";
        	//return false;
    	}
	else{ document.getElementById("longpassword").innerHTML = "";}
	
	if(nom==false|cog==false|ema==false|gem==false|str==false|n<8|n>20){return false;}
    	
	return true;
}
	

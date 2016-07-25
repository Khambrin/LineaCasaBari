
function validateForm() {
    	
	var nom  = recform.nome.value;
	var cog  = recform.cognome.value;
    	var ema  = recform.email.value;
	var str  = recform.password.value;

	if(nom==false){ document.getElementById("nom").innerHTML = "Completare il campo Nome"; return false;}
	if(cog==false){ document.getElementById("cog").innerHTML = "Completare il campo Cognome"; return false;}
	if(ema==false){ document.getElementById("ema").innerHTML = "Completare il campo Email"; return false;}

	var rgxstr = /^[^\s@]+@[^\s@]+\.[^\s@]+$/ ;
	var gem = rgem.test(str);
	if(gem==false){
		document.getElementById("emai").innerHTML = "Email non valida"; 
		return false;
	}

	var n = str.length;
    	if(n<8) {
		document.getElementById("shortpassword").innerHTML = "Password troppo corta, minimo 8 caratteri";
		document.getElementById("longpassword").innerHTML = "";
        	return false;
    	}
	else if(n>20) {
		document.getElementById("shortpassword").innerHTML = "";
		document.getElementById("longpassword").innerHTML = "Password troppo lunga, massimo 20 caratteri";
        	return false;
    	}
    	
	return true;
}
	

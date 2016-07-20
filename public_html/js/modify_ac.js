
		function validateForm() {
    			var str  = modacform.nuova_password.value;
			var snt  = modacform.nuovo_telefono.value;
			var sem  = modacform.nuova_email.value;
    			var n = str.length;
			var t = snt.length;
    			if(n<8) {
				document.getElementById("shortpassword").innerHTML = "Nuova Password troppo corta, minimo 8 caratteri";
				document.getElementById("longpassword").innerHTML = "";
        			return false;
	
    			}
			else if(n>20) {
				document.getElementById("shortpassword").innerHTML = "";
				document.getElementById("longpassword").innerHTML = "Nuova Password troppo lunga, massimo 20 caratteri";
        			return false;
    			}
			if(t<8 | t>15) { //ITU-T recommendation E.164
				document.getElementById("ernumber").innerHTML = "Numero non valido";
        			return false;
	
    			}
			var rgx = /^\+?([0-9]){8,15}$/;
    			var scr = rgx.test(snt);
			if(scr==false){
				document.getElementById("ernumber").innerHTML = "Numero non valido, uso di caratteri proibiti"; 
				return false;
			}
    			
			
			var rgem = /^[^\s@]+@[^\s@]+\.[^\s@]+$/ ;
			var gem = rgem.test(sem);
			if(gem==false){
				document.getElementById("eremail").innerHTML = "mail non valida"; 
				return false;
			}
			return true;
		}	
		

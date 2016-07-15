//"use strict";

if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
	xmlhttp = new XMLHttpRequest();
} 
else {// code for IE6, IE5
	xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
}

xmlhttp.open("GET", "../Annunci.xml", false);
xmlhttp.send();
xmlDoc = xmlhttp.responseXML;



var x = xmlDoc.getElementsByTagName("Annuncio");
for ( i = 0; i < x.length; i++) {
	document.write('<div id="info-container"> <h3>');
	document.write(x[i].getElementsByTagName("Titolo")[0].childNodes[0].nodeValue);
	document.write('</h3> <div class="info-text"><p>');
	document.write(x[i].getElementsByTagName("Data")[0].childNodes[0].nodeValue);
	document.write('</p><p>');
	document.write(x[i].getElementsByTagName("Testo")[0].childNodes[0].nodeValue);
	document.write('</p><div id="immagine_annuncio"><img src="');
	document.write(x[i].getElementsByTagName("Immagine")[0].childNodes[0].nodeValue);
	document.write('"></div></div></div>');
}

document.write("<p>Java ABILITATO</p>");

/*if (window.XMLHttpRequest) {// code for IE7+, Firefox, Chrome, Opera, Safari
 +				xmlhttp = new XMLHttpRequest();
 +			} else {// code for IE6, IE5
 +				xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
 +			}
 +			xmlhttp.open("GET", "listaAnnunci.xml", false);
 +			xmlhttp.send();
 +			xmlDoc = xmlhttp.responseXML;
 +
 +			
 +			var x = xmlDoc.getElementsByTagName("annuncio");
 +			for ( i = 0; i < x.length; i++) {
 +                document.write("<div class='post'>");
 +                document.write("<h2>");
 +				document.write(x[i].getElementsByTagName("titolo")[0].childNodes[0].nodeValue);
 +				document.write("</h2> <h3>");
 +				document.write(x[i].getElementsByTagName("data")[0].childNodes[0].nodeValue);
 +                document.write("</h3> <p>");
 +                document.write(x[i].getElementsByTagName("contenuto")[0].childNodes[0].nodeValue);
 +                document.write("</p>");
 +                document.write("</div>");
 +			}
*/

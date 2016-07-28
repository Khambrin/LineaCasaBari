#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use Switch;
use XML::LibXML;
use File::Basename;

my $cgi=new CGI;

my $session = CGI::Session->load();
my $email=$session->param("email");
my $pagina=param("pagina");
my $ind=$cgi->param("index_script");
my @errors=();
my %values;

#
my $parser=XML::LibXML->new;
#

foreach my $p (param())
{
	$values{$p}=lc param($p);
}

if (!$values{"via"})
{
	push @errors, "Devi completare il campo via.";
}
if (!$values{"numero"})
{
	push @errors, "Devi completare il campo numero civico.";
}
if (!$values{"citta"})
{
	push @errors, "Devi completare il campo città.";
}
if (!$values{"provincia"})
{
	push @errors, "Devi completare il campo provincia.";
}
if (!$values{"cap"})
{
	push @errors, "Devi completare il campo CAP.";
}

my $regex=$values{"provincia"}=~ /^[a-zA-Z][a-zA-Z]+$/;
{
	if(!$regex){push @errors, "Inserisci una provincia valida, ad esempio PD";}
}
my $regex=$values{"cap"}=~ /^[0-9]{5}$/;
{
	if(!$regex){push @errors, "Inserisci un CAP valido";}
}

if (@errors)
{
	print $cgi->header('text/html');
	my $file='indirizzi_temp.html';
	my $error_message_aux;
	foreach my $i (@errors)
	{
		my $x="<li>$i".'</li>';
		$error_message_aux=$error_message_aux.$x;
	}

	my $error_message="<ul>"."$error_message_aux"."</ul>";

	my $parser=XML::LibXML->new;
	my $doc=$parser->parse_file("../data/Indirizzi.xml");
	my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
		});
	
	#my $indirizzo_via=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo[position()='$ind']/Via");
	#my $indirizzo_numero_civico=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo[$ind]/Numero_civico/text()");
	#my $indirizzo_citta=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo[$ind]/Città/text()");
	#my $indirizzo_provincia=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo[$ind]/Provincia/text()");
	#my $indirizzo_cap=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo[$ind]/CAP/text()");

	my $indirizzo_via=$values{via};
	my $indirizzo_numero_civico=$values{numero};
	my $indirizzo_citta=$values{citta};
	my $indirizzo_provincia=$values{provincia};
	my $indirizzo_cap=$values{cap};

	my $via_form='<input class= "input" type="text" name="via" value="'."$indirizzo_via".'"/>';
	my $numero_form='<input class= "input" type="text" name="numero" value="'."$indirizzo_numero_civico".'"/>';
	my $citta_form='<input class= "input" type="text" name="citta" value="'."$indirizzo_citta".'"/>';
	my $provincia_form='<input class= "input" type="text" name="provincia" value="'."$indirizzo_provincia".'"/>';
	my $cap_form='<input class= "input" type="text" name="cap" value="'."$indirizzo_cap".'"/>';
	my $hidden='<input type="hidden" name="index_script" value="'."$ind".'"/>';

	
	
	my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'error' => $error_message,
		'pagina' => "edit",
		'vvia'=>$via_form,
		'vnumero'=>$numero_form,
		'vcitta'=>$citta_form,
		'vprovincia'=>$provincia_form,
		'vcap'=>$cap_form,
		'hidden'=>$hidden,
		'indice_controllo'=>$ind,
	};
	my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
	$template->process($file,$vars) || die $template->error();
}
else
{
	
	my $doc,my $root;
	
	my $parser=XML::LibXML->new();
	$doc=$parser->parse_file("../data/Indirizzi.xml");
	$root=$doc->documentElement();

	$ind--;
	my $indirizzo_canc=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo");
	$indirizzo_canc->[$ind]->parentNode->removeChild($indirizzo_canc->[$ind]);

	#my $indirizzo_canc=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo[Via=][Numero_civico]");
	#$indirizzo_canc->[0]->parentNode->removeChild($indirizzo_canc->[0]);

	my $indirizzi_node=$doc->findnodes("Indirizzi/Utente[Email='$email']");

	my $indirizzo_tag=$doc->createElement("Indirizzo");	
	$indirizzi_node->[0]->appendChild($indirizzo_tag);

	my $via_tag=$doc->createElement("Via");
	$via_tag->appendTextNode($values{'via'});
	$indirizzo_tag->appendChild($via_tag);
	
	my $numero_tag=$doc->createElement("Numero_civico");
	$numero_tag->appendTextNode($values{'numero'});
	$indirizzo_tag->appendChild($numero_tag);

	my $citta_tag=$doc->createElement("Città");
	$citta_tag->appendTextNode($values{'citta'});
	$indirizzo_tag->appendChild($citta_tag);
	
	my $provincia_tag=$doc->createElement("Provincia");
	$provincia_tag->appendTextNode($values{'provincia'});
	$indirizzo_tag->appendChild($provincia_tag);

	my $cap_tag=$doc->createElement("CAP");
	$cap_tag->appendTextNode($values{'cap'});
	$indirizzo_tag->appendChild($cap_tag);

	

	open (XML,">","../data/Indirizzi.xml");
	print XML $doc->toString();
	close(XML);
	print $cgi->redirect("check_session.cgi?stampa_indirizzi_modifica");

}

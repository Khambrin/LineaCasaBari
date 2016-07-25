#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use XML::LibXML;
use File::Basename;

my $cgi=new CGI;

my $session = CGI::Session->load();
my $email=$session->param("email");
my $pagina=param("pagina");
my @messaggi=();
my %values;
my $via_value="";
my $numero_value="";
my $citta_value="";
my $provincia_value="";
my $cap_value="";
foreach my $p (param())
{
	$values{$p}=lc param($p);
}

if (!$values{"via"})
{
	push @messaggi, "Devi completare il campo via.";
}
else
{
	$via_value=$values{"via"};
		
}
if (!$values{"numero"})
{
	push @messaggi, "Devi completare il campo numero civico.";
}
else
{
	$numero_value=$values{"numero"};
}
if (!$values{"citta"})
{
	push @messaggi, "Devi completare il campo citta.";
}
else
{
	$citta_value=$values{"citta"};
}
if (!$values{"provincia"})
{
	push @messaggi, "Devi completare il campo provincia.";
}
else
{
	$provincia_value=$values{"provincia"};
	my $regex=$values{"provincia"}=~ /^[a-zA-Z][a-zA-Z]$/;
	if(!$regex)
	{
		push @messaggi, "Inserisci una provincia valida, ad esempio PD";
		$provincia_value="";
	}
}

if (!$values{"cap"})
{
	push @messaggi, "Devi completare il campo CAP.";
}
else
{
	$cap_value=$values{"cap"};
	my $regex=$values{"cap"}=~ /^[0-9]{5}$/;
	if(!$regex)
	{
		push @messaggi, "Inserisci un CAP valido";
		$cap_value="";
	}
}

if (@messaggi)
{
	print $cgi->header('text/html');
	my $file='indirizzi_temp.html';
	my $error_message_aux;
	foreach my $i (@messaggi)
	{
		my $x="<li>$i".'</li>';
		$error_message_aux=$error_message_aux.$x;
	}
	my $error_message="<ul>"."$error_message_aux"."</ul>";
	my $vars={
		'sessione' => "true",
		'email' => $email,
		'via_value' => 'value="'."$via_value".'"',
		'numero_value' => 'value="'."$numero_value".'"',
		'citta_value' => 'value="'."$citta_value".'"',
		'provincia_value' => 'value="'."$provincia_value".'"',
		'cap_value' => 'value="'."$cap_value".'"',
		'messaggio' => $error_message,
		'pagina' => "aggiungi",
	};
	my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
	$template->process($file,$vars) || die $template->error();
}
else
{
	my $doc,my $root;
	if (-e "../data/Indirizzi.xml")
	{
		my $parser=XML::LibXML->new();
		$doc=$parser->parse_file("../data/Indirizzi.xml");
		$root=$doc->documentElement();
	}
	else
	{
		$doc=XML::LibXML::Document->new("1.0","UTF-8");
		$root=$doc->createElement("Indirizzi");
		$doc->setDocumentElement($root);
	}

	my $indirizzi_node=$doc->findnodes("Indirizzi/Utente[Email='$email']");	

	if($indirizzi_node)	
	{
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
	}
	else
	{
##
		my $utente_tag=$doc->createElement("Utente");	
		$root->appendChild($utente_tag);

		my $email_tag=$doc->createElement("Email");
		$email_tag->appendTextNode($email);	
		$utente_tag->appendChild($email_tag);

		my $indirizzo_tag=$doc->createElement("Indirizzo");	
		$utente_tag->appendChild($indirizzo_tag);
##
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

}
open (XML,">","../data/Indirizzi.xml");
print XML $doc->toString();
close(XML);
print $cgi->redirect("check_session.cgi?aggiungi-indirizzo-ok");
}

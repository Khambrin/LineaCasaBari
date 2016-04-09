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
	$values{$p}=param($p);
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
	my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'error' => $error_message,
		'pagina' => $pagina,
		#passare tutti i dati di edit_account.cgi
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
	print $cgi->redirect("stampa_indirizzi.cgi");

}

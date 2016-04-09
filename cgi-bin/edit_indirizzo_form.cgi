#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use Switch;
use XML::LibXML;

my $cgi=new CGI;


my $session = CGI::Session->load();
my $email=$session->param("email");
my $amministratore=$session->param("amministratore");
my $index=$cgi->param("indice_indirizzo_edit");

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Indirizzi.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});


my $ind=++$index;

my $indirizzo_via=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo[position()='$ind']/Via");
my $indirizzo_numero_civico=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo[$ind]/Numero_civico/text()");
my $indirizzo_citta=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo[$ind]/Città/text()");
my $indirizzo_provincia=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo[$ind]/Provincia/text()");
my $indirizzo_cap=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo[$ind]/CAP/text()");


my $via_form='<input class= "input" type="text" name="via" value="'."$indirizzo_via".'"/>';
my $numero_form='<input class= "input" type="text" name="numero" value="'."$indirizzo_numero_civico".'"/>';
my $citta_form='<input class= "input" type="text" name="citta" value="'."$indirizzo_citta".'"/>';
my $provincia_form='<input class= "input" type="text" name="provincia" value="'."$indirizzo_provincia".'"/>';
my $cap_form='<input class= "input" type="text" name="cap" value="'."$indirizzo_cap".'"/>';

#my $hiddentitle='<input class= "input" type="hidden" name="oldtitolo" value="'."$titolo".'"/>';
#my $hidden='<input class="input" type="hidden" name="indice_indirizzo" value="'."$ind".'"/>';
$ind=--$index;
my $hidden='<input type="hidden" name="index_script" value="'."$ind".'"/>';

my $file='indirizzi_temp.html';
my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => $amministratore,
		'pagina' => "edit",
		'vvia'=>$via_form,
		'vnumero'=>$numero_form,
		'vcitta'=>$citta_form,
		'vprovincia'=>$provincia_form,
		'vcap'=>$cap_form,
		'hidden'=>$hidden,
		'indice_controllo'=>$ind,
	};

print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

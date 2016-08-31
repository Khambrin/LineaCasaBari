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




my $indirizzo_via=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo[position()='$index']/Via");
my $indirizzo_numero_civico=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo[$index]/Numero_civico/text()");
my $indirizzo_citta=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo[$index]/Città/text()");
my $indirizzo_provincia=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo[$index]/Provincia/text()");
my $indirizzo_cap=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo[$index]/CAP/text()");


my $via_form='<input id="via" class= "input" type="text" name="via" value="'."$indirizzo_via".'"/>';
my $numero_form='<input id="numero" class= "input" type="text" name="numero" value="'."$indirizzo_numero_civico".'"/>';
my $citta_form='<input id="citta" class= "input" type="text" name="citta" value="'."$indirizzo_citta".'"/>';
my $provincia_form='<input id="provincia" class= "input" type="text" name="provincia" value="'."$indirizzo_provincia".'"/>';
my $cap_form='<input id="cap" class= "input" type="text" name="cap" value="'."$indirizzo_cap".'"/>';

my $hidden='<input type="hidden" name="index_script" value="'."$index".'"/>';

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
		'indice_controllo'=>$index,
	};

print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

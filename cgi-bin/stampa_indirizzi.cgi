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
my $mex=$cgi->param("messaggio");
my $ias=$cgi->param("iscrizione_avvenuta");

my $vars;

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Indirizzi.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
#
#
my @indirizzo_via=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo/Via/text()");
my @indirizzo_numero_civico=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo/Numero_civico/text()");
my @indirizzo_citta=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo/Città/text()");
my @indirizzo_provincia=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo/Provincia/text()");
my @indirizzo_cap=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo/CAP/text()");

my $file='indirizzi_temp.html';
my $tot;
for (my $index=0; $index <=$#indirizzo_via; $index++)
{	
	my $x='<div class="form-container2"><ul class="form-Block"><h2>'."Indirizzo n. $index</h2>";
	$tot=$tot.$x;
	my $x='<li><label>'."via @indirizzo_via[$index]</label></li>";
	$tot=$tot.$x;
	my $x='<li><label>'."numero @indirizzo_numero_civico[$index]</label></li>";
	$tot=$tot.$x;
	my $x='<li><label>'."@indirizzo_citta[$index]</label></li>";
	$tot=$tot.$x;
	my $x='<li><label>'."@indirizzo_provincia[$index]</label></li>";
	$tot=$tot.$x;
	my $x='<li><label>'."@indirizzo_cap[$index]</label></li>";
	$tot=$tot.$x;	
	my $x='<li><form action="remove_indirizzo.cgi" method="post"><div><button class="button" type="submit">Rimuovi</button><input type="hidden" name="indice_indirizzo" value="'."$index".'"/></div></form><form action="edit_indirizzo_form.cgi" method="post"><div><button class="button" type="submit">Modifica</button><input type="hidden" name="indice_indirizzo_edit" value="'."$index".'"/></div></form></li></ul></div>';
	$tot=$tot.$x;
}

my $lista_indirizzi=$tot;

$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => $amministratore,
		'lista_indirizzi' => $lista_indirizzi,
		'messaggio'=>$mex,
		'iscrizione_avvenuta'=>$ias,
	};

print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

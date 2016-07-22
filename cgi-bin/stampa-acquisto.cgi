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


my $vars;

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Indirizzi.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my @indirizzo_via=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo/Via/text()");
my $num_indi=$doc->findvalue("count(Indirizzi/Utente[Email='$email']/Indirizzo)");
my @indirizzo_numero_civico=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo/Numero_civico/text()");
my @indirizzo_citta=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo/Città/text()");
my @indirizzo_provincia=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo/Provincia/text()");
my @indirizzo_cap=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo/CAP/text()");

my $file='acquisto_temp.html';
my $tot;
my $counter=0;
if($num_indi)
{
	my $x='<li><p>'."Indirizzo n. 1</p>".'<input type="checkbox" name="indirizzo" value="1" checked/></li>';
	$tot=$tot.$x;
	my $x='<li><p>'."Via: @indirizzo_via[$counter]</p></li>";
	$tot=$tot.$x;
	my $x='<li><p>'."Numero: @indirizzo_numero_civico[$counter]</p></li>";
	$tot=$tot.$x;
	my $x='<li><p>'."Citt&agrave;: @indirizzo_citta[$counter]</p></li>";
	$tot=$tot.$x;
	my $x='<li><p>'."Provincia: @indirizzo_provincia[$counter]</p></li>";
	$tot=$tot.$x;
	my $x='<li><p>'."CAP: @indirizzo_cap[$counter]</p></li>";
	$tot=$tot.$x;	
	$counter++;

for (my $index=1; $index <=$#indirizzo_via; ++$index)
{	
	my $num_x=$index+1;
	my $x='<li><label id="acquisto-indirizzoLabel">'."Indirizzo n. $num_x </label>".'<input type="checkbox" name="indirizzo" value="'."$index".'"/></li>';
	$tot=$tot.$x;
	my $x='<li><p>'."Via: @indirizzo_via[$index]</p></li>";
	$tot=$tot.$x;
	my $x='<li><label>'."Numero: @indirizzo_numero_civico[$index]</label></li>";
	$tot=$tot.$x;
	my $x='<li><label>'."Citt&agrave;: @indirizzo_citta[$index]</label></li>";
	$tot=$tot.$x;
	my $x='<li><label>'."Provincia: @indirizzo_provincia[$index]</label></li>";
	$tot=$tot.$x;
	my $x='<li><label>'."CAP: @indirizzo_cap[$index]</label></li>";
	$tot=$tot.$x;	
	
}

my $lista_indirizzi=$tot;

$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => $amministratore,
		'lista_indirizzi' => $lista_indirizzi,
		'messaggio'=> "false",
	};
}
else
{
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => $amministratore,
		'messaggio'=> "Aggiungi un indirizzo dalla specifica sezione di Account",
		
	};
}
print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

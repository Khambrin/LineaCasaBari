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
if ($session->is_empty) {
	print $cgi->redirect('check_session.cgi?stampa_desideri');
}
my $email=$session->param("email");

my $amministratore=$session->param("amministratore");
my $mex=$cgi->param("messaggio_newsletter");
my $ias=$cgi->param("iscrizione_avvenuta");

my $vars;

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Desideri.xml");
my $pro=$parser->parse_file("../data/Prodotti.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my @prodotti=$doc->findnodes("Liste/Lista[Utente='$email']/Prodotto/text()");


my $file='lista_desideri_temp.html';
my $tot;

my $index=0;
for (; $index <=$#prodotti; $index++)
{	
	my $x='<fieldset><ul class="lista-desideri-block"><li><p>Prodotto: '."@prodotti[$index]".'</p></li>';
	$tot=$tot.$x;
	my $prodotto_immagine=$pro->findnodes("Prodotti/Prodotto[Codice='@prodotti[$index]']/Immagine/text()");
	my $alt= "immagine del prodotto @prodotti[$index]";
	my $stampa_immagine='<img src="'."$prodotto_immagine".'" alt="'."$alt".'" class="img-product"/>';
	my $x='<li>'."$stampa_immagine".'</li>';
	$tot=$tot.$x;
	my $x='<li><form action="remove_desiderio.cgi" method="post" class="side-element"><div class="side-element"><button class="button" type="submit">Rimuovi Prodotto</button><input type="hidden" name="indice_desiderio" value="'."$index".'"/></div></form>';
	$tot=$tot.$x;
	my $x='<form action="aggiungi_carrello.cgi" method="post" class="side-element"><div class="side-element"><button class="button" type="submit">Aggiungi al Carrello</button><input type="hidden" name="codice_prodotto" value="'."@prodotti[$index]".'"/></div></form></li></ul></fieldset>';
	$tot=$tot.$x;
}
my $lista_desideri;
my $messaggio="false";
if($index)
{
	if($ENV{'QUERY_STRING'} eq 'rimosso')
	{
		$messaggio="Prodotto rimosso con successo";
	}
	$lista_desideri='<div class="generic-container"><div class="form-container2"><h2>Lista dei Desideri</h2>'."$tot".'</div></div>';
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => $amministratore,
		'lista_desideri' => $lista_desideri,
		'messaggio'=> $messaggio,
		'messaggio_newsletter'=>$mex,
		'iscrizione_avvenuta'=>$ias,
	};
}
else
{
	if($ENV{'QUERY_STRING'} eq 'rimosso')
	{
		$messaggio='Prodotto rimosso con successo, ora la tua lista &egrave; vuota, per aggiungere qualcosa visita la pagina<a href="check_session.cgi?prodotti">Prodotti</a>';
	}
	else
	{
		$messaggio='La tua lista &egrave; vuota, per aggiungere qualcosa visita la pagina <a href="check_session.cgi?prodotti">Prodotti</a>';
	}
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => $amministratore,
		'messaggio'=> $messaggio,
		'messaggio_newsletter'=> $mex,
		'iscrizione_avvenuta'=>$ias,
	};
}
print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

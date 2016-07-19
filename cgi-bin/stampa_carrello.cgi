#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use XML::LibXML;

my $cgi=new CGI;
my $session = CGI::Session->load();
if ($session->is_empty) {
	print $cgi->redirect('check_session.cgi?carrello');
}
print $cgi->header('text/html');
my $email=$session->param("email");

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Utenti.xml");
my $amministratore=$doc->findnodes("Utenti/Utente[Email='$email']/Amministratore/text()");
my $doc=$parser->parse_file("../data/Carrelli.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my $messaggio="false";
my @utente_carrello=$doc->findnodes("Carrelli/Carrello[Utente='$email']");
my $vars;
my $key=$ENV{'QUERY_STRING'};
if(!@utente_carrello[0])
{
	if ($key eq 'false')
	{
		$messaggio="Il tuo carrello &egrave; vuoto, visita la pagina Prodotti per comporne uno";
	}
	elsif ($key eq 'modificato')
	{
		$messaggio="Modifica effettuata con successo, ora il tuo carrello &egrave; vuoto";
	}
	elsif ($key eq 'svuotato')
	{
		$messaggio="Ordine effettuato con successo, ora il tuo carrello &egrave; vuoto";
	}
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => $amministratore,
		'messaggio' => $messaggio,
	};
}
else
{
	if ($key eq 'modificato')
	{
		$messaggio="modifica effettuata con successo";
	}
	my $tot;
	my @lista_prodotti=$doc->findnodes("Carrelli/Carrello[Utente='$email']/Elemento/Prodotto/text()");
	my @lista_quantita=$doc->findnodes("Carrelli/Carrello[Utente='$email']/Elemento/Quantita/text()");
	
	my $k=0;
	my $x='<li><h2>'."Il tuo carrello</h2></li>";
	$tot=$tot.$x;
	foreach my$i (@lista_prodotti)
	{
		my $x='<li><label class="carrello-prodottoLabel">Prodotto: </label>'."$i".'</li>';
		$tot=$tot.$x;
		my $x='<li><label class="carrello-quantitaLabel">Quantit&agrave: </label>'." @lista_quantita[$k]".'</li>';
		$tot=$tot.$x;
		my $x='<li><label class="carrello-quantitaTogliLabel">Diminuisci quantit&agrave:</label><div class="inputLeft"></div><div class="inputMiddle"><input class="input" type="text" name="togli_quantita-'."$k".'"/></div><div class="inputRight"></div></li>';
		$tot=$tot.$x;
		my $x='<li><label class="carrello-prodottoTogliLabel">Togli il prodotto interamente:</label><input type="checkbox" name="elimina_prodotto-'."$k".'" value="1"/></li>';
		$tot=$tot.$x;
		$k++;
		
	}
	
	my $lista_carrello='<div class="form-container2"><form action="carrello_togli_quantita_prodotto.cgi" method="post"><ul class="form-Block">'."$tot".'</ul><button class="button" type="submit" value="togli">Togli</button></form><form action="stampa-acquisto.cgi" method="post"><button class="button" type="submit" value="accquista">Acquista</button></form></div>';
	
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => $amministratore,
		'lista_carrello' => $lista_carrello,
		'messaggio'=> $messaggio,
	};
}

my $file='carrello_temp.html';
$template->process($file,$vars) || die $template->error();

	




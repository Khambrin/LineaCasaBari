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
		$messaggio='Il tuo carrello &egrave; vuoto, visita la pagina <a href="check_session.cgi?prodotti">Prodotti</a> per comporne uno';
	}
	elsif ($key eq 'modificato')
	{
		$messaggio='Modifica effettuata con successo, ora il tuo carrello &egrave; vuoto. Torna alla pagina <a href="check_session.cgi?prodotti">Prodotti</a>';
	}
	elsif ($key eq 'svuotato')
	{
		$messaggio='Ordine effettuato con successo, ora il tuo carrello &egrave; vuoto. Torna alla pagina <a href="check_session.cgi?prodotti">Prodotti</a>';
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
		$messaggio="Modifica effettuata con successo";
	}
	if ($key eq 'non-modificato')
	{
		$messaggio="Nessuna modifica effettuata";
	}
	my $tot;
	my @lista_prodotti=$doc->findnodes("Carrelli/Carrello[Utente='$email']/Elemento/Prodotto/text()");
	my @lista_quantita=$doc->findnodes("Carrelli/Carrello[Utente='$email']/Elemento/Quantita/text()");
	
	my $k=0;
	my $parser=XML::LibXML->new;
	my $doc=$parser->parse_file("../data/Prodotti.xml");
	
	foreach my$i (@lista_prodotti)
	{
		my $prodotto_immagine=$doc->findnodes("Prodotti/Prodotto[Codice='$i']/Immagine/text()");
		my $alt= substr $prodotto_immagine, 19, -4;
		my $stampa_immagine='<img src="'."$prodotto_immagine".'" alt="'."$alt".'"/>';
		my $x='<div class="carrello_left_col">'."$stampa_immagine".'</div>';
		$tot=$tot.$x;
		my $x='<div class="carrello_right_col">
            <fieldset>
                <legend>Prodotto '."$i".'</legend>
                <ul class="form-Block">
                    <li>
                        <h3 class="carrello-prodottoh3">Prodotto: '."$i".'</h3>
                    </li>';
		$tot=$tot.$x;
		my $x='<li><p>Quantit&agrave;: '." @lista_quantita[$k]".'</p></li>';
		$tot=$tot.$x;
		my $x='<li>
                <p>Diminuisci quantit&agrave;:</p>
                <div class="inputLeft"></div><div class="input-carrello"><input class="input" title="Diminuisci quantit&agrave;" type="text" name="togli_quantita-'."$k".'"/></div><div class="inputRight"></div>
            </li>';
		$tot=$tot.$x;
		my $x='<li>
                        <p>Togli il prodotto interamente:</p>
                        <input title="Togli il prodotto interamente" type="checkbox" name="elimina_prodotto-'."$k".'" value="1"/>
                    </li>
                    </ul>
                </fieldset>
            </div>';
		$tot=$tot.$x;
		
		$k++;
		
	}
	my $x='<div class="side-element">
                <button class="button" type="submit" value="togli">Togli</button>
            </div>
            </form>
            <form class="side-element" action="stampa-acquisto.cgi" method="post">
                <div class="side-element">
                    <button class="button" type="submit" value="acquista">Acquista</button>
                </div>
            </form>';
	$tot=$tot.$x;

	my $lista_carrello='<div class="generic-container"><div class="form-container2">
                <h2>Il tuo carrello</h2>
                <form class="side-element" action="carrello-edit.cgi" method="post">'."$tot".'</div>
            </div>';
	
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

	




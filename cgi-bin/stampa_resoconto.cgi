#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use Switch;
use XML::LibXML;

my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
my $cgi=new CGI;
my $session = CGI::Session->load();

my $email=$session->param("email");
my $amministratore=$session->param("amministratore");
my $email=$session->param("email");
my $pagamento=param("mpagamento-select");

my $parser=XML::LibXML->new;
my $carrello_doc=$parser->parse_file("../data/Carrelli.xml");
my $prodotto_doc=$parser->parse_file("../data/Prodotti.xml");

my $num_prodotti=$carrello_doc->findvalue("count(Carrelli/Carrello[Utente='$email']/Elemento)");
my $tot_prodotto=0;
for(my $i=0; $i<$num_prodotti; $i++)
{
	my @cod=$carrello_doc->findnodes("Carrelli/Carrello[Utente='$email']/Elemento[$i]/Prodotto/text()");
	my $codice=@cod[0]->string_value;
	my @prz=$prodotto_doc->findnodes("Prodotti/Prodotto[Codice='$codice']/Prezzo/text()");
	my $prezzo=@prz[0]->string_value;
	$tot_prodotto=$tot_prodotto+$prezzo;
}

my $tot;

my $x='<li><h2>Resoconto</h2></li>';
$tot=$tot.$x;

my $x='<li><label id="resoconto-costoLabel">Prezzo totale: </label>'."$tot_prodotto".'</li>';
$tot=$tot.$x;

my $x='<li><label id="resoconto-mpagLabel">Metodo scelto: ';
$tot=$tot.$x;

my $indi=param('indirizzo');
my $x='<li><p>Hai scelto l&#180;indirizzo numero: '."$indi".'</p><div class="inputLeft"></div><div class="inputMiddle"><input class="input" type="text" name="codCcredito"/></div><div class="inputRight"></div></li>';
$tot=$tot.$x;

if($pagamento eq 'carta_credito')
{
	my $x='Carta di credito</label><li>';
	$tot=$tot.$x;
	my $x='<li><label id="resoconto-ccreditoLabel">Inserire codice: </label><div class="inputLeft"></div><div class="inputMiddle"><input class="input" type="text" name="codCcredito"/></div><div class="inputRight"></div></li>';
	$tot=$tot.$x;
}
elsif($pagamento eq 'bonifico')
{
	my $x='Bonifico</label><li>';
	$tot=$tot.$x;
	my $x='<li><p>Le nostre coordinate bancarie sono: IT	11	X	03268	10001	100000000000</p></li>';
	$tot=$tot.$x;
}
elsif($pagamento eq 'contrassegno')
{
	my $x='Contrassegno</label><li>';
	$tot=$tot.$x;
	my $x='<li><p>Le invieremo una mail con data e ora di arrivo previsto della merce</p></li>';
	$tot=$tot.$x;
}
elsif($pagamento eq 'pay_pal')
{
	my $x='Pay pal</label><li>';
	$tot=$tot.$x;
	my $x='<li><label id="resoconto-paypalLabel">Inserire codice: </label><div class="inputLeft"></div><div class="inputMiddle"><input class="input" type="text" name="codPaypal"/></div><div class="inputRight"></div></li>';
	$tot=$tot.$x;
}
elsif($pagamento eq 'carta_prepagata')
{
	my $x='Carta prepagata</label><li>';
	$tot=$tot.$x;
	my $x='<li><label id="resoconto-prepagataLabel">Inserire codice: </label><div class="inputLeft"></div><div class="inputMiddle"><input class="input" type="text" name="codPaypal"/></div><div class="inputRight"></div></li>';
	$tot=$tot.$x;
}
my $x='<li><button class="button" type="submit" value="conferma">Conferma</button><li>';
$tot=$tot.$x;

my $lista_acquisto='<div class="form-container2"><form action="aggiungi-ordine.cgi" method="post"><ul>'."$tot".'</ul></form></div>';
my $vars={
	'sessione' => "true",
	'email' => $email,
	'lista_acquisto' => $lista_acquisto,
	'amministratore'=>$amministratore,
};

my $file='resoconto_temp.html';
$template->process($file,$vars) || die $template->error();

#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use XML::LibXML;
use File::Basename;
use Switch;



my $cgi=new CGI;

my $session = CGI::Session->load();
my $email=$session->param("email");
my $mpagamento=param("mpagamento");
my $indirizzo=param("indirizzo");indirizzo
my $parser=XML::LibXML->new;
my $carrello_doc=$parser->parse_file("../data/Carrelli.xml");
my $num_prodotti=$carrello_doc->findvalue("count(Carrelli/Carrello[Utente='$email']/Elemento)");

my $new=0;
if (-e "../data/Ordini.xml")
{
	my $parser=XML::LibXML->new();
	$doc=$parser->parse_file("../data/Ordini.xml");
	$root=$doc->documentElement();
}
else
{
	$doc=XML::LibXML::Document->new("1.0","UTF-8");
	$root=$doc->createElement("Ordini");
	$doc->setDocumentElement($root);
	$new=1;	
}

my $ordine_tag=$doc->createElement("Ordine");	
$root->appendChild($ordine_tag);

if($new==0)
{
	my $last_id=$doc->findvalue("Ordini/Ordine[last()]/Codice");
	$id=$last_id+1;
	my $id_tag=$doc->createElement("Codice");
	$id_tag->appendTextNode($id);
	$ordine_tag->appendChild($id_tag);
}
else
{
	$id=1;
	my $id_tag=$doc->createElement("Codice");
	$id_tag->appendTextNode($id);
	$ordine_tag->appendChild($id_tag);
}

my $utente_tag=$doc->createElement("Utente");
$utente_tag->appendTextNode($email);
$ordine_tag->appendChild($utente_tag);

my ($sec,$min,$hour,$mday,$mon,$yr19,$wday,$yday,$isdst) = localtime(time);
my $year=$yr19+1900;
my $date="$mday/$mon/$year";
my $date_tag=$doc->createElement("Data");
$date_tag->appendTextNode($date);
$ordine_tag->appendChild($date_tag);
	
my $pagamento_tag=$doc->createElement("Mpagamento");
$pagamento_tag->appendTextNode($mpagamento);
$ordine_tag->appendChild($pagamento_tag);
	
my $indirizzo_tag=$doc->createElement("Indirizzo");
$ordine_tag->appendChild($indirizzo_tag);
$indirizzo_tag->appendTextNode($indirizzo);

for(my$i=1;$i<=num_prodotti;$i++)	
{
	my $cod=param('prodotto'."$i".'');
	prodotto_tag=$doc->createElement("Prodotto");
	$ordine_tag->appendChild($indirizzo_tag);
	$prodotto_tag->appendTextNode($cod);
}

open (XML,">","../data/Ordini.xml");
print XML $doc->toString();
close(XML);
#manca svuotare carrello e redirect su check session con svuotato
my $messaggio="Prodotto aggiunto correttamente al carrello";
print $cgi->redirect('prodotto.cgi?Codice='."$codice".'&Filter='."$filter".'&Page='."$page".'&Messaggio='."$messaggio");


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
my $mpagamento=param('mpagamento');
if($mpagamento eq 'carta_credito')
{
	$mpagamento='carta di credito';
}
elsif($mpagamento eq 'pay_pal')
{
	$mpagamento='PayPal';
}
elsif($mpagamento eq 'carta_prepagata')
{
	$mpagamento='Carta prepagata';
}

my $indirizzo=param("indirizzo");
my $parser=XML::LibXML->new;
my $carrello_doc=$parser->parse_file("../data/Carrelli.xml");
my $num_prodotti=$carrello_doc->findvalue("count(Carrelli/Carrello[Utente='$email']/Elemento)");

my $new=0;
my $ordini_doc;
my $root;
if (-e "../data/Ordini.xml")
{
	my $parser=XML::LibXML->new();
	$ordini_doc=$parser->parse_file("../data/Ordini.xml");
	$root=$ordini_doc->documentElement();
}
else
{
	$ordini_doc=XML::LibXML::Document->new("1.0","UTF-8");
	$root=$ordini_doc->createElement("Ordini");
	$ordini_doc->setDocumentElement($root);
	$new=1;	
}

my $ordine_tag=$ordini_doc->createElement("Ordine");	
$root->appendChild($ordine_tag);

if($new==0)
{
	my $last_id=$ordini_doc->findvalue("Ordini/Ordine[last()]/Codice");
	my $id=$last_id+1;
	my $id_tag=$ordini_doc->createElement("Codice");
	$id_tag->appendTextNode($id);
	$ordine_tag->appendChild($id_tag);
}
else
{
	my $id=1;
	my $id_tag=$ordini_doc->createElement("Codice");
	$id_tag->appendTextNode($id);
	$ordine_tag->appendChild($id_tag);
}

my $utente_tag=$ordini_doc->createElement("Utente");
$utente_tag->appendTextNode($email);
$ordine_tag->appendChild($utente_tag);

my ($sec,$min,$hour,$mday,$mon,$yr19,$wday,$yday,$isdst) = localtime(time);
my $year=$yr19+1900;
my $date="$mday/$mon/$year";
my $date_tag=$ordini_doc->createElement("Data");
$date_tag->appendTextNode($date);
$ordine_tag->appendChild($date_tag);
	
my $pagamento_tag=$ordini_doc->createElement("Mpagamento");
$pagamento_tag->appendTextNode($mpagamento);
$ordine_tag->appendChild($pagamento_tag);
	
my $indirizzo_tag=$ordini_doc->createElement("Indirizzo");
$ordine_tag->appendChild($indirizzo_tag);
$indirizzo_tag->appendTextNode($indirizzo);

for(my$i=1;$i<=$num_prodotti;$i++)	
{
	my $cod=param('prodotto'."$i".'');
	my $prodotto_tag=$ordini_doc->createElement("Prodotto_ordinato");
	$ordine_tag->appendChild($indirizzo_tag);
	$prodotto_tag->appendTextNode($cod);
}

open (XML,">","../data/Ordini.xml");
print XML $ordini_doc->toString();
close(XML);

my $carrello = $carrello_doc->findnodes("Carrelli/Carrello[Utente='$email']");
$carrello->[0]->parentNode->removeChild($carrello->[0]);

open (XML,">","../data/Carrelli.xml");
print XML $carrello_doc->toString();
close(XML);
print $cgi->redirect('check_session.cgi?carrello-svuotato');



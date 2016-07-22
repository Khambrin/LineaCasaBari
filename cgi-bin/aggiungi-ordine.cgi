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
my $doc=$parser->parse_file("../data/Carrelli.xml");
my $num_prodotti=$doc->findvalue("count(Carrelli/Carrello[Utente='$email']/Elemento)");

my $doc;
my $root;
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
}

my $ordine_tag=$doc->createElement("Ordine");	
$root->appendChild($ordine_tag);

my $last_id=$doc->findvalue("Ordini/Ordine[last()]/Codice");
my $id=$last_id+1;
my $id_tag=$doc->createElement("Codice");
$ordine_tag->appendChild($id_tag);
$id_tag->appendTextNode($id);

my $utente_tag=$doc->createElement("Utente");
$ordine_tag->appendChild($utente_tag);
$utente_tag->appendTextNode($email);

my ($sec,$min,$hour,$mday,$mon,$yr19,$wday,$yday,$isdst) = localtime(time);
my $year=$yr19+1900;
my $date="$mday/$mon/$year";
my $date_tag=$doc->createElement("Data");
$ordine_tag->appendChild($date_tag);
$date_tag->appendTextNode($date);
	
my $pagamento_tag=$doc->createElement("Mpagamento");
$ordine_tag->appendChild($pagamento_tag);
$pagamento_tag->appendTextNode($mpagamento);
	
my $indirizzo_tag=$doc->createElement("Indirizzo");
$ordine_tag->appendChild($indirizzo_tag);
$indirizzo_tag->appendTextNode($indirizzo);

for(my$i=1;$i<=$num_prodotti;$i++)	
{
	my $cod=param('$i');
	my $prodotto_tag=$doc->createElement("Prodotto_ordinato");
	$ordine_tag->appendChild($indirizzo_tag);
	$prodotto_tag->appendTextNode($cod);
}

open (XML,">","../data/Ordini.xml");
print XML $doc->toString();
close(XML);

my $parser=XML::LibXML->new();
$doc=$parser->parse_file("../data/Carrelli.xml");
my $carrello = $doc->findnodes("Carrelli/Carrello[Utente='$email']");
$carrello->[0]->parentNode->removeChild($carrello->[0]);

open (XML,">","../data/Carrelli.xml");
print XML $doc->toString();
close(XML);
print $cgi->redirect('check_session.cgi?carrello-svuotato');



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
my $quantita=param("quantita");
my $prodotto=param("codice_prodotto");
my %in;

if (length ($ENV{'QUERY_STRING'}) > 0){
    my $buffer = $ENV{'QUERY_STRING'};
    my @pairs = split(/&/, $buffer);
	my $name;
	my $value;
    foreach my $pair (@pairs){
        ($name, $value) = split(/=/, $pair);
        $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$in{$name} = $value; 
    }
}

#memorizzo tutti i valori necessari a ritornare alla pagina del prodotto correttamente

my $filter;
if ($in{'Filter'}) {
	$filter=$in{'Filter'};
	}
else {
	$filter='Tutte';
}

my $page;
if ($in{'Page'}) {
	$page=$in{'Page'};
	}
else {
	$page=0;
}

my $codice=$in{'Codice'};
if(!$codice){$codice=$prodotto;}

my $query;
if ($in{'Query'}) {
	$query=$in{'Query'};
}

my $order;
if ($in{'Order'}) {
	$order=$in{'Order'};
}

my $query_string;
if($query) {
	$query_string='?Codice='."$codice".'&amp;Filter='."$filter".'&amp;Page='."$page".'&amp;Query='."$query".'&amp;Order='."$order";
} else {
	$query_string='?Codice='."$codice".'&amp;Filter='."$filter".'&amp;Page='."$page".'&amp;Order='."$order";
}

if ($session->is_empty) {
	print $cgi->redirect('check_session.cgi'."$query_string");
}



my $doc,my $root;
	my $id=0, my $valutazione="";
if (-e "../data/Carrelli.xml")
{
	my $parser=XML::LibXML->new();
	$doc=$parser->parse_file("../data/Carrelli.xml");
	$root=$doc->documentElement();
}
else
{
	$doc=XML::LibXML::Document->new("1.0","UTF-8");
	$root=$doc->createElement("Carrelli");
	$doc->setDocumentElement($root);	
}
my @carrello_esistente=$doc->findnodes("Carrelli/Carrello[Utente='$email']");
if(!@carrello_esistente[0])
{
	my $carrello_tag=$doc->createElement("Carrello");	
	$root->appendChild($carrello_tag);
	my $id_tag=$doc->createElement("Utente");
	$id_tag->appendTextNode($email);
	$carrello_tag->appendChild($id_tag);
	
	my $element_tag=$doc->createElement("Elemento");
	$carrello_tag->appendChild($element_tag);	
	
	my $prodotto_tag=$doc->createElement("Prodotto");
	$element_tag->appendChild($prodotto_tag);
	$prodotto_tag->appendTextNode($prodotto);
	
	my $quantita_tag=$doc->createElement("Quantita");
	$element_tag->appendChild($quantita_tag);
	$quantita_tag->appendTextNode($quantita);
}
else
{
	my @prodotto_esistente=$doc->findnodes("Carrelli/Carrello[Utente='$email']/Elemento[Prodotto='$prodotto']");
	if(!@prodotto_esistente[0])
	{
		my $element_tag=$doc->createElement("Elemento");
		@carrello_esistente[0]->appendChild($element_tag);
		
		my $prodotto_tag=$doc->createElement("Prodotto");
		$element_tag->appendChild($prodotto_tag);
		$prodotto_tag->appendTextNode($prodotto);
	
		my $quantita_tag=$doc->createElement("Quantita");
		$element_tag->appendChild($quantita_tag);
		$quantita_tag->appendTextNode($quantita);
	}
	else
	{
		my @quantita_esistente=$doc->findnodes("Carrelli/Carrello[Utente='$email']/Elemento[Prodotto='$prodotto']/Quantita");
		my $somma=@quantita_esistente[0]->string_value;
		$somma=$somma+$quantita;
		
		my @element_node=$doc->findnodes("Carrelli/Carrello[Utente='$email']/Elemento[Prodotto='$prodotto']");
		
		@quantita_esistente[0]->parentNode->removeChild(@quantita_esistente[0]);
		
		my $quantita_tag=$doc->createElement("Quantita");
		@element_node[0]->appendChild($quantita_tag);
		$quantita_tag->appendTextNode($somma);

	}
}
open (XML,">","../data/Carrelli.xml");
print XML $doc->toString();
close(XML);

my $messaggio='Prodotto aggiunto correttamente al carrello. Per effettuare l'."'".'acquisto procedi al';
print $cgi->redirect('prodotto.cgi'."$query_string".'&amp;Messaggio='."$messaggio");


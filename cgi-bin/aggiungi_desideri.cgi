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
my $prodotto=param("codice_prodotto");
my $codice=$prodotto;


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
if (-e "../data/Desideri.xml")
{
	my $parser=XML::LibXML->new();
	$doc=$parser->parse_file("../data/Desideri.xml");
	$root=$doc->documentElement();
}
else
{
	$doc=XML::LibXML::Document->new("1.0","UTF-8");
	$root=$doc->createElement("Liste");
	$doc->setDocumentElement($root);	
}
my @lista_esistente=$doc->findnodes("Liste/Lista[Utente='$email']");
if(!@lista_esistente[0])
{
	my $lista_tag=$doc->createElement("Lista");	
	$root->appendChild($lista_tag);
	my $id_tag=$doc->createElement("Utente");
	$id_tag->appendTextNode($email);
	$lista_tag->appendChild($id_tag);
	
	my $prodotto_tag=$doc->createElement("Prodotto");
	$lista_tag->appendChild($prodotto_tag);
	$prodotto_tag->appendTextNode($prodotto);	

}
else
{
my $lista_tag=@lista_esistente[0];
	my $prodotto_esistente=$doc->findnodes("Liste/Lista[Utente='$email' and Prodotto='$prodotto']");
	if(!$prodotto_esistente)
	{
		my $prodotto_tag=$doc->createElement("Prodotto");
		$lista_tag->appendChild($prodotto_tag);
		$prodotto_tag->appendTextNode($prodotto);
	}
}
open (XML,">","../data/Desideri.xml");
print XML $doc->toString();
close(XML);

my $messaggio="Prodotto aggiunto correttamente alla lista dei desideri";
print $cgi->redirect('prodotto.cgi'."$query_string".'&amp;MessaggioDesideri='."$messaggio");


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

if (-e "../data/Prodotti.xml")
{



}
else
{
	my $doc=XML::LibXML::Document->new("1.0","UTF-8");
	my $root=$doc->createElement("Prodotti");
	$doc->setDocumentElement($root);
	my $prodotto_tag=$doc->createElement("Prodotto");
	$root->appendChild($prodotto_tag);
	my @tags=("Codice","Nome","Descrizione","Prezzo","Data_aggiunta","Valutazione","Immagine");
		foreach my $k (@value_tags)
		{
			my $value_tag=$doc->createElement($k);
			$value_tag->appendTextNode($values{lc $k});
			$utente_tag->appendChild($value_tag);
		}
	
}

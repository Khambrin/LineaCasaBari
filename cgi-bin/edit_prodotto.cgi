#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use Switch;
use XML::LibXML;
use File::Basename;

my $cgi=new CGI;

my $session = CGI::Session->load();
my $email=$session->param("email");
my $pagina=param("pagina");
my @errors=();
my %values;


my $parser=XML::LibXML->new;


foreach my $p (param())
{
	$values{$p}=param($p);
}

my $doc,my $root;

my $parser=XML::LibXML->new();
$doc=$parser->parse_file("../data/Prodotti.xml");
$root=$doc->documentElement();


my $old_prodotto=$values{"old_cod"};

my $prodotto_node=$doc->findnodes("Prodotti/Prodotto[Codice='$old_prodotto']");
$prodotto_node->[0]->parentNode->removeChild($prodotto_node->[0]);

my $prodotto_tag=$doc->createElement("Prodotto");	
$root->appendChild($prodotto_tag);

my $codice_tag=$doc->createElement("Codice");
$codice_tag->appendTextNode($values{'Codice'});
$prodotto_tag->appendChild($codice_tag);

my $nome_tag=$doc->createElement("Nome");
$nome_tag->appendTextNode($values{'Nome'});
$prodotto_tag->appendChild($nome_tag);

my $descrizione_tag=$doc->createElement("Descrizione");
$descrizione_tag->appendTextNode($values{'Descrizione'});
$prodotto_tag->appendChild($descrizione_tag);

my $categoria_tag=$doc->createElement("Categoria");
$categoria_tag->appendTextNode($values{'Categoria'});
$prodotto_tag->appendChild($categoria_tag);

my $prezzo_tag=$doc->createElement("Prezzo");
$prezzo_tag->appendTextNode($values{'Prezzo'});
$prodotto_tag->appendChild($prezzo_tag);

my $data_tag=$doc->createElement("Data_aggiunta");
$data_tag->appendTextNode($values{'Data'});
$prodotto_tag->appendChild($data_tag);

my $immagine_tag=$doc->createElement("Immagine");
my $immagine;
my $upload_directory="../public_html/images/prodotti";
my $read_directory="../images/prodotti";
if ($values{'Immagine'})
{
	
	my $upload_filehandle=$cgi->upload("Immagine");
	open (UPLOADFILE,">$upload_directory/$values{'Immagine'}") or die "$!";
	binmode UPLOADFILE;
	while (<$upload_filehandle>)
	{
		print UPLOADFILE;
	}
	close UPLOADFILE;
	$immagine="$read_directory/$values{'Immagine'}";
}
else
{
	$immagine="$upload_directory/$values{'old_image'}";
}
$immagine_tag->appendTextNode($immagine);
$prodotto_tag->appendChild($immagine_tag);

my $tag_tag=$doc->createElement("Tag");
$tag_tag->appendTextNode($values{'Tag1'});
$prodotto_tag->appendChild($tag_tag);

my $tag_tag=$doc->createElement("Tag");
$tag_tag->appendTextNode($values{'Tag2'});
$prodotto_tag->appendChild($tag_tag);

my $tag_tag=$doc->createElement("Tag");
$tag_tag->appendTextNode($values{'Tag3'});
$prodotto_tag->appendChild($tag_tag);

my $tag_tag=$doc->createElement("Tag");
$tag_tag->appendTextNode($values{'Tag4'});
$prodotto_tag->appendChild($tag_tag);


open (XML,">","../data/Prodotti.xml");
print XML $doc->toString();
close(XML);
print $cgi->redirect("ricerca_prodotto.cgi?modified");


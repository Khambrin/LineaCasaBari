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



my $parser=XML::LibXML->new;
my $email_recensione=$cgi->param("email_recensione");
my $doc=$parser->parse_file("../data/Prodotti.xml");

#calcolo il voto del prodotto
my $valutazione=0;
my $num_voti=0;
my @recensione_votop=$doc->findnodes("Prodotti/Prodotto[Codice='$codice']/Recensione/Voto/text()");
foreach my $i (@recensione_votop) {
	$valutazione="$valutazione"+"$i";
	$num_voti++;
}
my $voto_recensione_eliminata=$doc->findnodes("Prodotti/Prodotto[Codice='$codice']/Recensione[Email='$email_recensione']/Voto/text()");
$valutazione="$valutazione"-"$voto_recensione_eliminata";
$num_voti--;
$valutazione=$valutazione/$num_voti;

my $prodotto_valutazione=$doc->findnodes("Prodotti/Prodotto[Codice='$codice']/Valutazione");

my $valutazione_tag=$doc->createElement("Valutazione");
$valutazione_tag->appendTextNode($valutazione);
$prodotto_valutazione->[0]->replaceNode($valutazione_tag);	


my $prodotto_node=$doc->findnodes("Prodotti/Prodotto[Codice='$codice']/Recensione[Email='$email_recensione']");
$prodotto_node->[0]->parentNode->removeChild($prodotto_node->[0]);


open(XML,">","../data/Prodotti.xml");
print XML $doc->toString();
close(XML);

print $cgi->redirect('prodotto.cgi?Codice='."$codice".'&Filter='."$filter".'&Page='."$page");



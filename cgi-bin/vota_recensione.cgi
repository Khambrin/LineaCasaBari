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
my %values;
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

foreach my $p (param())
{
	$values{$p}=param($p);
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

my $query;
if ($in{'Query'}) {
	$query=$in{'Query'};
}

my $order;
if ($in{'Order'}) {
	$order=$in{'Order'};
}

my $codice=$in{'Codice'};

my $query_string;
if($query) {
	$query_string='?Codice='."$codice".'&Filter='."$filter".'&Page='."$page".'&Query='."$query".'&Order='."$order";
} else {
	$query_string='?Codice='."$codice".'&Filter='."$filter".'&Page='."$page".'&Order='."$order";
}




my $parser=XML::LibXML->new;
my $email_recensione=$cgi->param("email_recensione");
my $doc=$parser->parse_file("../data/Prodotti.xml");

#calcolo il voto della recensione
my $valutazione=0;
my $num_voti=0;
my $recensione_votor=$doc->findnodes("Prodotti/Prodotto[Codice='$codice']/Recensione[Email='$email_recensione']/Voto_recensione/text()");
my @recensione_emailvoto=$doc->findnodes("Prodotti/Prodotto[Codice='$codice']/Recensione[Email='$email_recensione']/Email_voto/text()");
$num_voti=@recensione_emailvoto;
$valutazione="$recensione_votor"+$values{"voto"};
$num_voti++;
$valutazione=$valutazione/$num_voti;

my $recensione_node=$doc->findnodes("Prodotti/Prodotto[Codice='$codice']/Recensione[Email='$email_recensione']/Voto_recensione");

my $valutazione_tag=$doc->createElement("Voto_recensione");
$valutazione_tag->appendTextNode($valutazione);
$recensione_node->[0]->replaceNode($valutazione_tag);

#inserisco l'email di chi vota nella lista
my $recensione_node=$doc->findnodes("Prodotti/Prodotto[Codice='$codice']/Recensione[Email='$email_recensione']");

my $email_tag=$doc->createElement("Email_voto");
$email_tag->appendTextNode($email);
$recensione_node->[0]->appendChild($email_tag);

open(XML,">","../data/Prodotti.xml");
print XML $doc->toString();
close(XML);

print $cgi->redirect('prodotto.cgi'."$query_string");


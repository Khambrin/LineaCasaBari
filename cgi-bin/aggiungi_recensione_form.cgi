#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use XML::LibXML;
use File::Basename;

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
	$query_string='?Codice='."$codice".'&amp;Filter='."$filter".'&amp;Page='."$page".'&amp;Query='."$query".'&amp;Order='."$order";
} else {
	$query_string='?Codice='."$codice".'&amp;Filter='."$filter".'&amp;Page='."$page".'&amp;Order='."$order";
}

foreach my $p (param())
{
	$values{$p}=param($p);
}

#gestione degli errori

my $errors;
my $default;

if (!$values{"titolo"})
{
	my $x="&amp;Errtitle=1";
	$errors=$errors.$x;
} else {
	my $title=$values{"titolo"};
	my $x='&amp;Title='."$title"; 
	$default=$default.$x;
}

if (!$values{"nome"})
{
	my $x="&amp;Errname=1";
	$errors=$errors.$x;
} else {
	my $nome=$values{"nome"};
	my $x='&amp;Nome='."$nome";
	$default=$default.$x;
}

if (!$values{"testo"})
{
	my $x="&amp;Errtext=1";
	$errors=$errors.$x;
} else {
	my $testo=$values{"testo"};
	my $x='&amp;Testo='."$testo";
	$default=$default.$x;
}

if ($errors)
{
	print $cgi->redirect('prodotto.cgi'."$query_string"."$errors"."$default");
}
else
{
	my $doc,my $root;
	my $parser=XML::LibXML->new();
	$doc=$parser->parse_file("../data/Prodotti.xml");
	$root=$doc->documentElement();
		
	#calcolo il voto del prodotto
	my $valutazione=0;
	my $num_voti=0;
	my @recensione_votop=$doc->findnodes("Prodotti/Prodotto[Codice='$codice']/Recensione/Voto/text()");
	foreach my $i (@recensione_votop) {
		$valutazione="$valutazione"+"$i";
		$num_voti++;
	}
	$valutazione=$valutazione+$values{"voto"};
	$num_voti++;
	$valutazione=$valutazione/$num_voti;

	my $prodotto_node=$doc->findnodes("Prodotti/Prodotto[Codice='$codice']");

	my $prodotto_valutazione=$doc->findnodes("Prodotti/Prodotto[Codice='$codice']/Valutazione");
	my $valutazione_tag=$doc->createElement("Valutazione");
	$valutazione_tag->appendTextNode($valutazione);
	$prodotto_valutazione->[0]->replaceNode($valutazione_tag);	

	my $recensione_tag=$doc->createElement("Recensione");	
	$prodotto_node->[0]->appendChild($recensione_tag);

	my $email_tag=$doc->createElement("Email");
	$email_tag->appendTextNode($email);
	$recensione_tag->appendChild($email_tag);
	
	my $titolo_tag=$doc->createElement("Titolo");
	$titolo_tag->appendTextNode($values{'titolo'});
	$recensione_tag->appendChild($titolo_tag);
	
	my $nome_tag=$doc->createElement("Nome");
	$nome_tag->appendTextNode($values{'nome'});
	$recensione_tag->appendChild($nome_tag);

	my ($sec,$min,$hour,$mday,$mon,$yr19,$wday,$yday,$isdst) = localtime(time);
	my $year=$yr19+1900;
	my $date="$mday/$mon/$year";
	my $data_tag=$doc->createElement("Data_pubblicazione");
	$data_tag->appendTextNode($date);
	$recensione_tag->appendChild($data_tag);
	
	my $testo_tag=$doc->createElement("Testo");
	$testo_tag->appendTextNode($values{'testo'});
	$recensione_tag->appendChild($testo_tag);

	my $votop_tag=$doc->createElement("Voto");
	$votop_tag->appendTextNode($values{'voto'});
	$recensione_tag->appendChild($votop_tag);

	my $votor_tag=$doc->createElement("Voto_recensione");
	$votor_tag->appendTextNode('');
	$recensione_tag->appendChild($votor_tag);

	open (XML,">","../data/Prodotti.xml");
	print XML $doc->toString();
	close(XML);
	print $cgi->redirect('prodotto.cgi'."$query_string");
}

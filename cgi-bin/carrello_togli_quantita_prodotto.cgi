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

my $doc=$parser->parse_file("../data/Carrelli.xml");
my $num_prodotti=$doc->findvalue("count(Carrelli/Carrello[Utente='$email']/Elemento)");

my @param
my $counter=0;
for (my $i=1; $i<=$num_prodotti;$i++)
{
	$counter++;
	
}


my $alt= substr $prodotto_immagine, 19, -4;

print $cgi->header('text/html');
print $cod_prodotto;

=pod
my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Ordini.xml");
my $num_prodotti=$doc->findvalue("count(Ordini/Ordine[Codice='$cod_ordine']/Prodotto)");
my $counter=0;
for (my $i=1; $i<=$num_prodotti;$i++)
{
	$counter++;
	if(param($i))
	{
		my $ordine = $doc->findnodes("Ordini/Ordine[Codice='$cod_ordine']/Prodotto[$counter]");
		$ordine->[0]->parentNode->removeChild($ordine->[0]);
		$counter--;
	}		
}
open(XML,">","../data/Ordini.xml");
print XML $doc->toString();
close(XML);

$parser=XML::LibXML->new;
$doc=$parser->parse_file("../data/Ordini.xml");
$num_prodotti=$doc->findvalue("count(Ordini/Ordine[Codice='$cod_ordine']/Prodotto)");

if($num_prodotti)
{
	print $cgi->redirect("ricerca_ordini.cgi?$cod_ordine");
}
else
{
	print $cgi->redirect("togli_ordine.cgi?$cod_ordine");
}





=cut

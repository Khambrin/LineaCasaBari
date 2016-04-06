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

my $parser=XML::LibXML->new;
my $prodotto=param("prodotto");

my $doc=$parser->parse_file("../data/Prodotti.xml");
my $prodotto_node=$doc->findnodes("Prodotti/Prodotto[Codice='$prodotto']");
$prodotto_node->[0]->parentNode->removeChild($prodotto_node->[0]);

open(XML,">","../data/Prodotti.xml");
print XML $doc->toString();
close(XML);

print $cgi->redirect('ricerca_prodotto.cgi?deleted');

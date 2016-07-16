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

my $parser=XML::LibXML->new;
my $codice=$cgi->param("cod_desiderio");
my $index=$cgi->param("indice_desiderio");




my $doc=$parser->parse_file("../data/Desideri.xml");
my $desiderio_node=$doc->findnodes("Liste/Lista[Utente='$email']/Prodotto");
$desiderio_node->[$index]->parentNode->removeChild($desiderio_node->[$index]);





open(XML,">","../data/Desideri.xml");
print XML $doc->toString();
close(XML);

print $cgi->redirect('stampa_desideri.cgi');










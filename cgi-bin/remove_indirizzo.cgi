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
my $index=$cgi->param("indice_indirizzo");
$index=$index-1;


my $doc=$parser->parse_file("../data/Indirizzi.xml");
my $indirizzi_node=$doc->findnodes("Indirizzi/Utente[Email='$email']/Indirizzo");
$indirizzi_node->[$index]->parentNode->removeChild($indirizzi_node->[$index]);



open(XML,">","../data/Indirizzi.xml");
print XML $doc->toString();
close(XML);

print $cgi->redirect('check_session.cgi?stampa_indirizzi_rimosso');










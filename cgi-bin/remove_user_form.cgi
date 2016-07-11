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
my $utente=param("emailuser");

my $doc=$parser->parse_file("../data/Utenti.xml");
my $utente_node=$doc->findnodes("Utenti/Utente[Email='$utente']");
$utente_node->[0]->parentNode->removeChild($utente_node->[0]);

open(XML,">","../data/Utenti.xml");
print XML $doc->toString();
close(XML);

print $cgi->redirect('remove_user.cgi');

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
if ($session->is_empty) {
	print $cgi->redirect('check_session.cgi?rimosso_annuncio');
}
my $parser=XML::LibXML->new;
my $codice=param("codice");

my $doc=$parser->parse_file("../data/Annunci.xml");
my $annuncio_node=$doc->findnodes("Annunci/Annuncio[Codice='$codice']");
$annuncio_node->[0]->parentNode->removeChild($annuncio_node->[0]);

open(XML,">","../data/Annunci.xml");
print XML $doc->toString();
close(XML);

print $cgi->redirect('check_session.cgi?rimosso_annuncio');










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

my $parser=XML::LibXML->new;
my $titolo_edit=param("titolo_edit");

my $doc=$parser->parse_file("../data/Annunci.xml");

my @annuncio_node=$doc->findnodes("Annunci/Annuncio[Titolo='$titolo_edit']");

@annuncio_node->[0]->removeChild("Titolo");
@annuncio_node->[0]->appendTextChild("Titolo", "Nuovo titolo");


open(XML,">","../data/Annunci.xml");
print XML $doc->toString();
close(XML);





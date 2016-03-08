#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use XML::LibXML;

my $cgi=new CGI;

my $session = CGI::Session->load();
my $email=$session->param("email");
my $codice=$session->param("Codice");

my $doc=$parser->parse_file("../data/Ordini.xml");
my @lista=$doc->findnodes("Ordini//Ordine[Codice=$Codice])");

my $file='gestione_prodotti_temp.html';
my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'error' => $error_message,
		'lista' => @lista,
	};





		
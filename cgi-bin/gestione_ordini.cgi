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
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my $lista_ordini;

if (-e "../data/Ordini.xml")
{
	my $parser=XML::LibXML->new;
	my $doc=$parser->parse_file("../data/Ordini.xml");
	my @orders=$doc->findnodes("Utenti/Utente/Email/text()");	
}
else
{
	$lista_ordini="";
}


my $file='gestione_ordini_temp.html';
my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'lista_ordini' => $lista_ordini,
	};
print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

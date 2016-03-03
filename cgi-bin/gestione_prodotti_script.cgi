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

my $lista_prodotti;
if (-e "../data/Prodotti.xml")
{
	my $parser=XML::LibXML->new;
	my $doc=$parser->parse_file("../data/Prodotti.xml");
	my @products=$doc->findnodes("Utenti/Utente/Email/text()");
}
else
{
	$lista_prodotti="";
}



my $file='gestione_prodotti_temp.html';
my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'lista_prodotti' => $lista_prodotti,
	};
print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use XML::LibXML;

my $cgi=new CGI;
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
	
my $session = CGI::Session->load();
my $email=$session->param("email");
my @errors=();

my $cod=param("cod");

if (!$cod)
{
	push @errors, "inserire un codice";
}


my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Ordini.xml");


my @lista=$doc->findnodes("Ordini//Ordine[Codice='$cod']");

my $file='gestione_ordini_temp.html';
my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'errors' => @errors,
		'lista' => @lista,
	};
print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

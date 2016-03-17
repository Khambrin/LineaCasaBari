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
print $cgi->header('text/html');
my $session = CGI::Session->load();
my $email=$session->param("email");

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Ordini.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
	
my $parser=XML::LibXML->new;
my $ordine;
if ($ENV{'REQUEST_METHOD'} eq 'POST')
{
	$ordine=param("ordine");
	
}
else
{
	$ordine=$ENV{'QUERY_STRING'};
}

my $doc=$parser->parse_file("../data/Ordini.xml");
my $ordine_node=$doc->findnodes("Ordini/Ordine[Codice='$ordine']");
$ordine_node->[0]->parentNode->removeChild($ordine_node->[0]);

open(XML,">","../data/Ordini.xml");
print XML $doc->toString();
close(XML);

my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'list' => "false",
	};

my $file='gestione_ordini_temp.html';
$template->process($file,$vars) || die $template->error();

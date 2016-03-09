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
	
my $cod=param("codice");
my $error="false";
my @cod_ordini=$doc->findnodes("Ordini/Ordine/Codice/text()");

if($cod)
{
	my $i;
	foreach $i (@cod_ordini)
	{
		if($i ne $cod)
		{
			$error="il codice inserito non corrisponde a nessun ordine esistente";
		}
		else
		{
			$error="false";
			last;
		}
	}
}
else
{
	$error="inserisci un codice per la ricerca";
}


my $file='gestione_ordini_temp.html';
my $tot;
my @ordine=$doc->findnodes("Ordini/Ordine[Codice='$cod']/text()");
foreach my $i (@ordine)
{
	my $x='<li><form action="gestione_ordini.cgi" method="post">'."$i".'<div><input type="submit" value="modifica"/></div></form></li>';
	$tot=$tot.$x;
}

my $lista_ordine="<ul>"."$tot"."</ul>";

my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'list' => "true",
		'error' => $error,
		'lista_ordini' => $lista_ordine,
	};

$template->process($file,$vars) || die $template->error();

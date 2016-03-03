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

my @codice;
my @data;
my @utente;
my @prodotti;
my $lista_ordini;

if (-e "../data/Ordini.xml")
{
	my $parser=XML::LibXML->new;
	my $doc=$parser->parse_file("../data/Ordini.xml");
	@codice=$doc->findnodes("Ordini//Ordine/Codice/text()");	
	@data=$doc->findnodes("Ordini//Ordine/Data/text()");	
	@utente=$doc->findnodes("Ordini//Ordine/Utente/text()");	
	@prodotti=$doc->findnodes("Ordini//Ordine/Prodotto/text()");	
}
else
{
	$lista_ordini_aux="";
}


my $file='gestione_ordini_temp.html';
my $tot;
foreach my $i (@lista_ordini_aux)
{
	my $x="<li>$i.</li>";
	$tot=$tot.$x;
}

 $lista_ordini="<ul>"."$tot"."</ul>";

my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'lista_utenti' => $lista_ordini,
	};
print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

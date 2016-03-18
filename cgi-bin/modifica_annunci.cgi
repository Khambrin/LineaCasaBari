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
my $email=$session->param("email");

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Annunci.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my @annuncio_titolo=$doc->findnodes("Annunci/Annuncio/Titolo/text()");

my $file='gestione_annunci_temp.html';
my $tot;
foreach my $i (@annuncio_titolo)
{
	my $x="<li>$i".'<form class="togli_annuncio-pulsante" action="remove_annuncio.cgi" method="post"><div><input type="submit" value="Rimuovi"/><input type="hidden" name="titolo" value="'."$i".'"/></div></form>
<form class="modifica_annuncio-pulsante" action="modifica_annunci_script.cgi" method="post"><div><input type="submit" value="Modifica"/><input type="hidden" name="titolo_edit" value="'."$i".'"/></div></form>
</li>';
	$tot=$tot.$x;
}

my $lista_annunci="<ul>"."$tot"."</ul>";

my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'pagina' => "modifica_annunci",
		'lista_annunci' => $lista_annunci,
	};

print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

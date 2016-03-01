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
my $doc=$parser->parse_file("../data/Utenti.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my @users=$doc->findnodes("Utenti/Utente/Email/text()");

my $file='togli_utenti_temp.html';
my $tot;
foreach my $i (@users)
{
	my $asd="<li>$i".'<form class="togli_utenti-pulsante"><div><input type="submit" value="Rimuovi"/></div></form></li>';
	$tot=$tot.$asd;
}

my $lista_utenti="<ul>"."$tot"."</ul>";

my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'lista_utenti' => $lista_utenti,
	};
$template->process($file,$vars) || die $template->error();

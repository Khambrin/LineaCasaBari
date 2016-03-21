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
	my $x='<li class="gestione-block">'."$i".'<form class="togli_utenti-pulsante" action="remove_user_form.cgi" method="post"><div class="gestione-button_block"><button class="button" type="submit">Rimuovi</button><input type="hidden" name="email" value="'."$i".'"/></div></form></li>';
	$tot=$tot.$x;
}

my $lista_utenti='<ul class="gestione-aggiungi_form" >'."$tot"."</ul>";

my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'lista_utenti' => $lista_utenti,
	};
$template->process($file,$vars) || die $template->error();

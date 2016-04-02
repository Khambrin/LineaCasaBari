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
my $mex=$cgi->param("messaggio_newsletter");
my $ias=$cgi->param("iscrizione_avvenuta");

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Utenti.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my @users=$doc->findnodes("Utenti/Utente/Email/text()");
my $file='togli_utenti_temp.html';
my $tot='<form action="remove_user_form.cgi" method="post">';
foreach my $i (@users)
{
	my $x='<li class="gestione-block"><div class="gestione-button_block"><label class="gestione-labels">'."$i".'</label><button class="button" type="submit"> Rimuovi </button></div><input type="hidden" name="email" value="'."$i".'"/></li>';
	$tot=$tot.$x;
}

my $lista_utenti='<ul class="gestione-aggiungi_form" >'."$tot"."</form></ul>";

my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'lista_utenti' => $lista_utenti,
		'messaggio_newsletter'=>$mex,
		'iscrizione_avvenuta'=>$ias,
	};
print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

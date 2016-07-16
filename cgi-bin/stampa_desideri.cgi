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

my $amministratore=$session->param("amministratore");
my $mex=$cgi->param("messaggio_newsletter");
my $ias=$cgi->param("iscrizione_avvenuta");

my $vars;

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Desideri.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my @prodotti=$doc->findnodes("Liste/Lista[Utente='$email']/Prodotto/text()");


my $file='lista_desideri_temp.html';
my $tot;


for (my $index=0; $index <=$#prodotti; $index++)
{	
	my $x='<li>Prodotto: '."@prodotti[$index]".'</li>';
	$tot=$tot.$x;
	my $x='<li><form action="remove_desiderio.cgi" method="post"><div><button class="button" type="submit">Rimuovi Prodotto</button><input type="hidden" name="indice_desiderio" value="'."$index".'"/></div></form></li>';
	$tot=$tot.$x;
	my $x='<li><form action="aggiungi_carrello.cgi" method="post"><div><button class="button" type="submit">Aggiungi al Carrello</button><input type="hidden" name="codice_prodotto" value="'."@prodotti[$index]".'"/></div></form></li>';
	$tot=$tot.$x;
}




my $lista_desideri="<ul>"."$tot"."</ul>";

if ($session->is_empty)
{
	$vars={
		'sessione' => "false",
		'lista_desideri' => $lista_desideri,
		'messaggio_newsletter'=>$mex,
		'iscrizione_avvenuta'=>$ias,
	};
}

else
{
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => $amministratore,
		'lista_desideri' => $lista_desideri,
		'messaggio_newsletter'=>$mex,
		'iscrizione_avvenuta'=>$ias,
	};
}
print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

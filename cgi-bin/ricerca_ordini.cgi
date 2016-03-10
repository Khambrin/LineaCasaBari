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
push my @ordine, $doc->findnodes("Ordini/Ordine[Codice='$cod']/Codice/text()");
push @ordine, $doc->findnodes("Ordini/Ordine[Codice='$cod']/Utente/text()");
push @ordine, $doc->findnodes("Ordini/Ordine[Codice='$cod']/Data/text()");
my $num_prodotto=$doc->findvalue("count(Ordini/Ordine[Codice=1]/Prodotto)");
for(my $x=0; $x<$num_prodotto;$x++)
{
	push @ordine, $doc->findnodes("Ordini/Ordine[Codice='$cod']/Prodotto/text()");
}

my @label = ('Codice','Utente','Data' );
for(my $x=0; $x<$num_prodotto;$x++)
{
	push @label, "Prodotto";
}

my $y=0;
for(my $i=0; $i<3;$i++)
{
	my $x='<li><form action="gestione_ordini.cgi" method="post">'."<label>@label[$i]: </label>". '<input type="text" name="'."@label[$i]".'" value="'."@ordine[$y]".'"/>';
	$y++;
	$tot=$tot.$x;
}
my $counter=1;
for(my $i=0; $i<$num_prodotto;$i++)
{
	my $x='<li><form action="gestione_ordini.cgi" method="post">'."<label>@label[$y] $counter: </label>". '<input type="text" name="'."@label[$y]$counter".'" value="'."@ordine[$y]".'"/>';
	$y++;
	$counter++;
	$tot=$tot.$x;
}

$tot=$tot.'<div><input type="submit" value="modifica"/></div></form></li>';

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

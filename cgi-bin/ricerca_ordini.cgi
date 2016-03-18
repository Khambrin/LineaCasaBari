#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
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
my $cod;
if ($ENV{'REQUEST_METHOD'} eq 'POST')
{
	$cod=param("codice");
	
}
else
{
	$cod=$ENV{'QUERY_STRING'};
}

my $error="false";
my @cod_ordini=$doc->findnodes("Ordini/Ordine/Codice/text()");

if(@cod_ordini)
{
	if($cod)
	{
		my $i;
		foreach $i (@cod_ordini)
		{
			if($i ne $cod)
			{
				print "non uguale";
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
}
else
{
	$error="non ci sono ordini";
}
my $vars;
if($error eq "false")
{
	my $tot;
	push my @ordine, $doc->findnodes("Ordini/Ordine[Codice='$cod']/Codice/text()");
	push @ordine, $doc->findnodes("Ordini/Ordine[Codice='$cod']/Utente/text()");
	push @ordine, $doc->findnodes("Ordini/Ordine[Codice='$cod']/Data/text()");
	my $num_prodotto=$doc->findvalue("count(Ordini/Ordine[Codice='$cod']/Prodotto)");
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
		my $x='<li class="gestione-block">'.'<form>'.'<label class="gestione-labels">'."@label[$i]: @ordine[$y]</label></form></li>";
		$y++;
		$tot=$tot.$x;
	}
	my $counter=1;
	$tot=$tot.'<form action="elimina_prodotti_ordini.cgi" method="post">';
	for(my $i=0; $i<$num_prodotto;$i++)
	{
		my $x='<li class="gestione-block">'.'<div><label class="gestione-labels">'."@label[$y] $counter: @ordine[$y]</label>".'<input type="checkbox" name="'."$counter".'" value="on"/></div></li>';
		$y++;
		$counter++;
		$tot=$tot.$x;
	}

	$y=0;
	$tot=$tot.'<li class="gestione-block"><div class="gestione-button_block"><button class="button" type="submit">elimina selezionati</button></div><input type="hidden" name="ordine" value="'."$cod".'"/></form><form action="togli_ordine.cgi" method="post"><input type="hidden" name="ordine" value="'."$cod".'"/><div><button class="button" type="submit">togli ordine</button></div></form></li>';
	my $lista_ordine='<ul class="gestione-aggiungi_form">'."$tot"."</ul>";
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'list' => "true",
		'lista_ordini' => $lista_ordine,
	};
}
else
{
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'list' => "false",
		'error' => $error,
	};
}
my $file='gestione_ordini_temp.html';
$template->process($file,$vars) || die $template->error();

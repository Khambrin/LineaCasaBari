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
		my $x="<li>"."<label>@label[$i]: @ordine[$y]</label></li>";
		$y++;
		$tot=$tot.$x;
	}
	my $counter=1;
	for(my $i=0; $i<$num_prodotto;$i++)
	{
		my $x="<li>"."<label>@label[$y] $counter: @ordine[$y]</label>".'<div><input type="checkbox" value="'."$counter".'/></div></li>';
		$y++;
		$counter++;
		$tot=$tot.$x;
	}

	$y=0;
	$tot=$tot.'<li><div><input type="submit" value="elimina selezionati"/></div><div><input type="submit" value="aggiungi prodotto"/></div>'.'<input type="hidden" name="ordine" value="'."$cod".'"/><input type="hidden" name="numero_prodotti" value="'."$num_prodotto".'"/></li>';
	my $lista_ordine='<div><form action=gestione_ordini.cgi" method="post">'."<ul>"."$tot"."</ul></form></div>";
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

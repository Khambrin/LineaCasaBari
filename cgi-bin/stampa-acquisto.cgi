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
my $doc=$parser->parse_file("../data/Indirizzi.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
=pod
my $messaggio="false";
my @utente_ordini=$doc->findnodes("Ordini/Ordine/Utente/text()");

if(@utente_ordini)
{
	my $i;
	foreach $i (@utente_ordini)
	{
		if($i ne $email)
		{
			$messaggio="non hai eseguito alcun ordine";
		}
		else
		{
			$messaggio="false";
			last;
		}
	}
}
else
{
	$messaggio="non ci sono ordini";
}

my $vars;


if($messaggio eq "false")
{
	my $tot;
	my @lista_ordini=$doc->findnodes("Ordini/Ordine[Utente='$email']/Codice/text()");
	foreach my$i (@lista_ordini)
	{
		my $x='<li><h2>'."Codice: $i</h2></li>";
		$tot=$tot.$x;
		my $x='<li><label>'."Utente: $email</label></li>";
		$tot=$tot.$x;
		my $data=$doc->findnodes("Ordini/Ordine[Codice=$i]/Data/text()");
		my $x='<li><label>'."Data: $data</label></li>";
		$tot=$tot.$x;
		my $num_prodotto=$doc->findvalue("count(Ordini/Ordine[Codice='$i']/Prodotto)");
		for(my $y=1; $y<=$num_prodotto;$y++)
		{
			my $prodotto=$doc->findnodes("Ordini/Ordine[Codice=$i]/Prodotto[$y]/text()");
			my $x='<li><label>'."Prodotto: $prodotto</label></li>";
			$tot=$tot.$x;
		}
	}
	
	my $lista_ordine='<div class="form-container2"><ul class="form-Block">'."$tot"."</ul></div>";
	$vars={
		'sessione' => "true",
		'email' => $email,
		'list' => "true",
		'amministratore' => $amministratore,
		'lista_ordini' => $lista_ordine,
	};
}
else
{
	$vars={
		'sessione' => "true",
		'email' => $email,
		'list' => "false",
		'amministratore' => $amministratore,
		'messaggio' => $messaggio,
	};
}
my $file='i_miei_ordini_temp.html';
$template->process($file,$vars) || die $template->error();

=cut

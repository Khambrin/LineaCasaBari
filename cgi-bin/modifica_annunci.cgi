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
if ($session->is_empty) {
	print $cgi->redirect('check_session.cgi?gestione_annunci');
}
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
	my $sess;
if ($session->is_empty) 
{
	$sess="false";
}
else
{
	$sess="true";
}
my $email=$session->param("email");
my $doc;
my $file='gestione_annunci_temp.html';
my $messaggio_vuota="false";
my $vars;
my $lista_annunci;
if (-e "../data/Annunci.xml") 
{
	my $parser=XML::LibXML->new;
	$doc=$parser->parse_file("../data/Annunci.xml");

	my @annuncio_codice=$doc->findnodes("Annunci/Annuncio/Codice/text()");
		
	my $counter=$doc->findvalue("count(Annunci/Annuncio)");
	if($counter!=0)
	{
		my $tot;
		foreach my $i (@annuncio_codice)
		{
			my $annuncio_titolo=$doc->findnodes("Annunci/Annuncio[Codice='$i']/Titolo/text()");
			my $x='<li>'."$annuncio_titolo".'<form action="remove_annuncio.cgi" method="post"><div><button class="button" type="submit" value="Rimuovi">Rimuovi</button><input type="hidden" name="codice" value="'."$i".'"/></div></form>
	<form action="modifica_annunci_script.cgi" method="post"><div><button class="button" type="submit" value="Modifica">Modifica</button><input type="hidden" name="codice_edit" value="'."$i".'"/></div></form>
	</li>';
			$tot=$tot.$x;
		}
		 $lista_annunci='<div class="form-container2"><h2>Modifica annunci</h2><ul class="form-Block">'."$tot</ul></div>";
	}
	else
	{
		 $lista_annunci='false';
		 $messaggio_vuota="Lista annunci vuota";
	}

	
	my $messaggio_confirm=0;

	if ($ENV{'QUERY_STRING'} eq 'rimosso')
	{
		$messaggio_confirm="Annuncio rimosso con successo";
		my $counter=$doc->findvalue("count(Annunci/Annuncio)");
		if($counter==0)
		{
			$messaggio_confirm="Annuncio rimosso con successo, lista annunci vuota";
		}
		$messaggio_vuota="false";

		$vars={
			'sessione' => $sess,
			'email' => $email,
			'amministratore' => "true",
			'messaggio_confirm' => $messaggio_confirm,
			'pagina' => "modifica_annunci",
			'lista_annunci' => $lista_annunci,
			'messaggio_vuota'=> $messaggio_vuota,
			
		};
	}
	elsif ($ENV{'QUERY_STRING'} eq 'modificato')
	{
		$messaggio_confirm="Annuncio modificato con successo";
	  $vars={
			'sessione' => $sess,
			'email' => $email,
			'amministratore' => "true",
			'messaggio_confirm' => $messaggio_confirm,
			'pagina' => "modifica_annunci",
			'lista_annunci' => $lista_annunci,
			'messaggio_vuota'=> $messaggio_vuota,
		};
	}
	else
	{
	  $vars={
			'sessione' => $sess,
			'email' => $email,
			'amministratore' => "true",
			'pagina' => "modifica_annunci",
			'lista_annunci' => $lista_annunci,
			'messaggio_vuota'=> $messaggio_vuota,
		};
	}
}
else
{
	$messaggio_vuota="Lista annunci vuota";
	$lista_annunci='false';
	$vars={
			'sessione' => $sess,
			'email' => $email,
			'amministratore' => "true",
			'pagina' => "modifica_annunci",
			'messaggio_vuota'=> $messaggio_vuota,
			'lista_annunci' => $lista_annunci,
		};
}
print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();


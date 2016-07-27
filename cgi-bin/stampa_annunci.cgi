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
my $doc;
my $root;
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
my $ sess;
if ($session->is_empty) 
{
	$sess="false";
}
else
{
	$sess="true";
}
	
my $file='annunci_temp.html';
if ((-e "../data/Annunci.xml") or (my $counter=$doc->findvalue("count(Annunci/Annuncio)")) )
{
	my $parser=XML::LibXML->new();
	$doc=$parser->parse_file("../data/Annunci.xml");
	$root=$doc->documentElement();
	
	my @annuncio_titolo=$doc->findnodes("Annunci/Annuncio/Titolo/text()");
	my @annuncio_codice=$doc->findnodes("Annunci/Annuncio/Codice/text()");
	my @annuncio_data=$doc->findnodes("Annunci/Annuncio/Data/text()");
	my @annuncio_testo=$doc->findnodes("Annunci/Annuncio/Testo/text()");
	my @annuncio_immagine=$doc->findnodes("Annunci/Annuncio/Immagine/text()");

	my $lista_annunci;
	for (my $index=0; $index <=$#annuncio_titolo; $index++)
	{	
		my $x='<div class="info-container"><h3>'."@annuncio_titolo[$index]".'</h3>';
		$lista_annunci=$lista_annunci.$x;
		my $x='<div class="info-text"><p>'."@annuncio_data[$index]".'</p>';
		$lista_annunci=$lista_annunci.$x;
		my $x="<p>@annuncio_testo[$index]".'</p>';
		$lista_annunci=$lista_annunci.$x;
		my $alt= substr @annuncio_immagine[$index], 18, -4;
		my $x='<div class="immagine_annuncio"><img src="'."@annuncio_immagine[$index]".'" alt="'."$alt".'"/></div></div></div>';
		$lista_annunci=$lista_annunci.$x;
	}
	
		$vars={
			'sessione' => $sess,
			'email' => $email,
			'amministratore' => $amministratore,
			'lista_annunci' => $lista_annunci,
		};
}
else
{
	$vars={
			'sessione' => $sess,
			'email' => $email,
			'amministratore' => $amministratore,
			'messaggio_confirm' => "Non ci sono annunci"
		};
	
}

	


print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

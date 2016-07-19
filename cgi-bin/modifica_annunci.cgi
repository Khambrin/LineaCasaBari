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
my $email=$session->param("email");

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Annunci.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my @annuncio_titolo=$doc->findnodes("Annunci/Annuncio/Titolo/text()");

my $file='gestione_annunci_temp.html';
my $tot;
foreach my $i (@annuncio_titolo)
{
	my $x='<li>'."$i".'<form action="remove_annuncio.cgi" method="post"><div><button class="button" type="submit" value="Rimuovi">Rimuovi</button><input type="hidden" name="titolo" value="'."$i".'"/></div></form>
<form action="modifica_annunci_script.cgi" method="post"><div><button class="button" type="submit" value="Modifica">Modifica</button><input type="hidden" name="titolo_edit" value="'."$i".'"/></div></form>
</li>';
	$tot=$tot.$x;
}

my $lista_annunci='<div class="form-container2"><h2>Modifica annunci</h2><ul class="form-Block">'."$tot</ul></div>";

my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'pagina' => "modifica_annunci",
		'lista_annunci' => $lista_annunci,
	};

print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

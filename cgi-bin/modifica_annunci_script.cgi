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

my $codice=param("codice_edit");



my $annuncio_node=$doc->findnodes("Annunci/Annuncio[Codice='$codice']/Codice/text()");
my $titolo=$doc->findnodes("Annunci/Annuncio[Codice='$codice']/Titolo/text()");
my $fcontenuto=$doc->findnodes("Annunci/Annuncio[Codice='$codice']/Testo/text()");

my $vcontenuto='<textarea id="testo" class="gestione_textarea" name="testo" rows="" cols="">'."$fcontenuto".'</textarea>';

my $vt_form='<input id="titolo_annuncio" class="input" type="text" name="titolo" value="'."$titolo".'"/>';

my $hiddencodice='<input id="codice" class="input" type="hidden" name="oldcodice" value="'."$codice".'"/>';


my $file='gestione_annunci_temp.html';
my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'pagina' => "edit",
		'vtitolo'=>$vt_form,
		'vcontenuto'=>$vcontenuto,
		'oldcodice'=>$hiddencodice,
	};

print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

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

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Annunci.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my $titolo=param("titolo_edit");
my $annuncio_node=$doc->findnodes("Annunci/Annuncio[Titolo='$titolo']");
my $contenuto=$annuncio_node->[0]->parentNode->findvalue('Testo');

my $vt_form='<input class= "input" type="text" name="titolo" value="'."$titolo".'"/>';

# 


#




my $file='gestione_annunci_temp.html';
my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'pagina' => "edit",
		'prova'=>"salveeeeeeee",
		'vtitolo'=>$vt_form,
	};

print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

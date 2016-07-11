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

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Utenti.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});




my $old_name=$doc->findnodes("Utenti/Utente[Email='$email']/Nome/text()");
my $old_surname=$doc->findnodes("Utenti/Utente[Email='$email']/Cognome/text()");
my $old_tel=$doc->findnodes("Utenti/Utente[Email='$email']/Telefono/text()");




my $old_em_form='<input class= "input" type="text" name="nuova_email" value="'."$email".'"/>';
my $old_name_form='<input class= "input" type="text" name="nuovo_nome" value="'."$old_name".'"/>';
my $old_surname_form='<input class= "input" type="text" name="nuovo_cognome" value="'."$old_surname".'"/>';
my $old_tel_form='<input class= "input" type="text" name="nuovo_telefono" value="'."$old_tel".'"/>';




my $file='impostazioni_account_temp.html';
my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => $amministratore,
		'vemail'=>$old_em_form,
		'vnome'=>$old_name_form,
		'vcognome'=>$old_surname_form,
		'vtelefono'=>$old_tel_form,
		
	};

print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

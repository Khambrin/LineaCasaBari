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
if ($session->is_empty) {
	print $cgi->redirect('check_session.cgi?gestione_indirizzi');
}
my $email=$session->param("email");

my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my $hidden;
my $file='indirizzi_temp.html';
my $vars;
my $messaggio_confirm="false";
if($ENV{'QUERY_STRING'} eq 'aggiunto')
{
	$hidden='<input type="hidden" name="pagina" value="aggiungi"/>';
	$messaggio_confirm="Indirizzo aggiunto correttamente";
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'pagina' => "aggiungi",
		'hidden' => $hidden,
		'messaggio_confirm'=> $messaggio_confirm,
	};
}
elsif ($ENV{'QUERY_STRING'} eq 'nonaggiunto')
{
	$hidden='<input type="hidden" name="pagina" value="aggiungi"/>';
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'pagina' => "aggiungi",
		'hidden' => $hidden,
		'messaggio_confirm'=> $messaggio_confirm,
	};
}
print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

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

my $file, my $vars;

my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

switch($ENV{'QUERY_STRING'})
{
	case 'index' { $file='index_temp.html'; }
	case 'annunci' { $file='annunci_temp.html'; }
	case 'contattaci' { $file='contattaci_temp.html'; }
	case 'registrazione' { $file='registrazione_temp.html'; }
	case 'login' { $file='login_temp.html'; }
	case 'la_nostra_storia' { $file='la_nostra_storia_temp.html'; }
	case 'prodotti' { $file='prodotti_temp.html'; }
	case 'resi_rimborsi' { $file='resi_rimborsi_temp.html'; }
	case 'termini_spedizione' { $file='termini_spedizione_temp.html'; }
	case 'i_miei_ordini' { $file='i_miei_ordini_temp.html'; }
	case 'impostazioni_account' { $file='impostazioni_account_temp.html' }
	case 'indirizzi' { $file='indirizzi_temp.html' }
	case 'pagamenti' { $file='pagamenti_temp.html' }
	case 'gestione_annunci' { $file='gestione_annunci_temp.html' }
	case 'gestione_ordini' {$file='gestione_ordini_temp.html' }
}

if ($session->is_empty)
{
	$vars={
		'sessione' => "false",
	};
	if ($ENV{'QUERY_STRING'} eq 'i_miei_ordini' or $ENV{'QUERY_STRING'} eq 'pagamenti' or $ENV{'QUERY_STRING'} eq 'impostazioni_account' 
		or $ENV{'QUERY_STRING'} eq 'indirizzi' or $ENV{'QUERY_STRING'} eq 'togli_utenti' or $ENV{'QUERY_STRING'} eq 'gestione_prodotti' 
		or $ENV{'QUERY_STRING'} eq 'gestione_ordini' or $ENV{'QUERY_STRING'} eq 'gestione_annunci')
	{
		$file='login_temp.html';
	}
}
else
{	
	my $email=$session->param("email");
	my $amministratore=$session->param("amministratore");
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => $amministratore,
		'error'=> "false",
	};
	if ($ENV{'QUERY_STRING'} eq 'login' or $ENV{'QUERY_STRING'} eq 'registrazione')
	{
		$file='index_temp.html';
	}
	if ($ENV{'QUERY_STRING'} eq 'togli_utenti')
	{
		print $cgi->redirect("remove_user.cgi");
	}
	if ($ENV{'QUERY_STRING'} eq 'gestione_prodotti')
	{
		print $cgi->redirect("gestione_prodotti_script.cgi?aggiungi");
	}
	if($ENV{'QUERY_STRING'} eq 'gestione_annunci')
	{
		print $cgi->redirect("gestione_annunci_script.cgi?aggiungi");
	}
}
	print $cgi->header('text/html');
	$template->process($file,$vars) || die $template->error();

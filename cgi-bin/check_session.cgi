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
	case 'registrazione' { $file='registrazione_temp.html'; }
	case 'login' { $file='login_temp.html'; }
	case 'la_nostra_storia' { $file='la_nostra_storia_temp.html'; }
	case 'prodotti' { print $cgi->redirect("prodotti.cgi"); }
	case 'resi_rimborsi' { $file='resi_rimborsi_temp.html'; }
	case 'termini_spedizione' { $file='termini_spedizione_temp.html'; }
	case 'impostazioni_account' { $file='impostazioni_account_temp.html' }
	case 'gestione_ordini' {$file='gestione_ordini_temp.html' }
	case 'lista_desideri' {$file='lista_desideri_temp.html' }
	case 'mappa_sito' { $file='mappa_sito_temp.html' }
	case 'iscrizione_newsletter' { $file='newsletter_temp.html' }
}

if ($session->is_empty)
{
	$vars={
		'sessione' => "false",
	};
	if ($ENV{'QUERY_STRING'} eq 'i_miei_ordini' or $ENV{'QUERY_STRING'} eq 'impostazioni_account' 
		or $ENV{'QUERY_STRING'} eq 'indirizzi' or $ENV{'QUERY_STRING'} eq 'togli_utenti' 
		or $ENV{'QUERY_STRING'} eq 'gestione_prodotti' or $ENV{'QUERY_STRING'} eq 'gestione_ordini' 
		or $ENV{'QUERY_STRING'} eq 'gestione_annunci' or $ENV{'QUERY_STRING'} eq 'carrello' 
		or $ENV{'QUERY_STRING'} eq 'gestione_account_normal' or $ENV{'QUERY_STRING'} eq 'gestione_indirizzi' 
		or $ENV{'QUERY_STRING'} eq 'carrello-svuotato' or $ENV{'QUERY_STRING'} eq 'carrello-modificato'
		or $ENV{'QUERY_STRING'} eq 'stampa_indirizzi'	or $ENV{'QUERY_STRING'} eq 'edit_indirizzo'
		or $ENV{'QUERY_STRING'} eq 'stampa_desideri' or $ENV{'QUERY_STRING'} eq 'desiderio-rimosso'
		or $ENV{'QUERY_STRING'} eq 'aggiungi-indirizzo' or $ENV{'QUERY_STRING'} eq 'stampa_indirizzi'
		or $ENV{'QUERY_STRING'} eq 'stampa_indirizzi_rimosso'or $ENV{'QUERY_STRING'} eq 'stampa_indirizzi_modifica'
		or $ENV{'QUERY_STRING'} eq 'stampa_acquisto' or $ENV{'QUERY_STRING'} eq 'gestione_account_mod')
	{
		$file='login_temp.html';
		$vars={
				'log' => "Accedi prima di continuare",
				'query_string' => "$ENV{'QUERY_STRING'}",
			}
	}
	elsif ($ENV{'QUERY_STRING'} eq 'logout')
	{
		print $cgi->redirect("gestione_account.cgi?exit");
	}
	elsif ($ENV{'QUERY_STRING'} eq 'registrato')
	{
		$file='login_temp.html';
		$vars={
			'log'=> "Registrazione avvenuta con successo ora puoi accedere",
		};
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
		'messaggio'=> "false",
	};
	if ($ENV{'QUERY_STRING'} eq 'gestione_account_normal')
	{
		print $cgi->redirect("gestione_account.cgi");
	}

	if ($ENV{'QUERY_STRING'} eq 'login' or  $ENV{'QUERY_STRING'} eq 'registrazione' or $ENV{'QUERY_STRING'} eq 'gestione_account')
	{
		print $cgi->redirect("gestione_account.cgi?ok");
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
	if($ENV{'QUERY_STRING'} eq 'i_miei_ordini')
	{
		print $cgi->redirect("stampa_ordini.cgi");
	}
	if($ENV{'QUERY_STRING'} eq 'carrello')
	{
		print $cgi->redirect("stampa_carrello.cgi?false");
	}
	if($ENV{'QUERY_STRING'} eq 'carrello-modificato')
	{
		print $cgi->redirect("stampa_carrello.cgi?modificato");
	}
	if($ENV{'QUERY_STRING'} eq 'carrello-svuotato')
	{
		print $cgi->redirect("stampa_carrello.cgi?svuotato");
	}
	if ($ENV{'QUERY_STRING'} eq 'stampa_indirizzi' or  $ENV{'QUERY_STRING'} eq 'edit_indirizzo')
	{
		print $cgi->redirect("stampa_indirizzi.cgi");
	}
	if($ENV{'QUERY_STRING'} eq 'stampa_desideri')
	{
		print $cgi->redirect("stampa_desideri.cgi");
	}
	if ($ENV{'QUERY_STRING'} eq 'desiderio-rimosso')
	{
		print $cgi->redirect("stampa_desideri.cgi?rimosso");
	}
	if($ENV{'QUERY_STRING'} eq 'aggiungi-indirizzo' or $ENV{'QUERY_STRING'} eq 'gestione_indirizzi' )
	{
		print $cgi->redirect("gestione_indirizzi_script.cgi?nonaggiunto");
	}
	if($ENV{'QUERY_STRING'} eq 'aggiungi-indirizzo-ok')
	{
		print $cgi->redirect("gestione_indirizzi_script.cgi?aggiunto");
	}
	if($ENV{'QUERY_STRING'} eq 'stampa_indirizzi')
	{
		print $cgi->redirect("stampa_indirizzi.cgi")
	}
	if($ENV{'QUERY_STRING'} eq 'stampa_indirizzi_rimosso')
	{
		print $cgi->redirect("stampa_indirizzi.cgi?rimosso")
	}
	if($ENV{'QUERY_STRING'} eq 'stampa_indirizzi_modifica')
	{
		print $cgi->redirect("stampa_indirizzi.cgi?modificato")
	}
	if( $ENV{'QUERY_STRING'} eq 'stampa_acquisto')
	{
		print $cgi->redirect("stampa-acquisto.cgi")
	}
	if( $ENV{'QUERY_STRING'} eq 'gestione_account_mod')
	{
		print $cgi->redirect("gestione_account.cgi?mod")
	}
}
	print $cgi->header('text/html');
	$template->process($file,$vars) || die $template->error();

#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use Switch;

my $cgi=new CGI;
print $cgi->header('text/html');
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
	case 'la_nostra_storia' { $file='la_nostra_storia_temp.html'; }
	case 'prodotti' { $file='prodotti_temp.html'; }
	case 'resi_rimborsi' { $file='resi_rimborsi_temp.html'; }
	case 'termini_spedizione' { $file='termini_spedizione_temp.html'; }
	case 'i_miei_ordini' { $file='i_miei_ordini_temp'; }
	case 'impostazioni_account' { $file='impostazioni_account_temp' }
	case 'indirizzi' { $file='indirizzi_temp' }
	case 'pagamenti' { $file='pagamenti_temp' }
}

if ($session->is_empty)
{
	$vars={
		'sessione' => "false",
	};
	if ($ENV{'QUERY_STRING'} eq 'login' or $ENV{'QUERY_STRING'} eq 'account')
	{
		$file='login_temp.html';
	}
	if ($ENV{'QUERY_STRING'} eq 'registrazione')
	{
		$file='registrazione_temp.html';
	}
}
else
{	
	$vars={
		'sessione' => "true",
		'email' => $session->param("email"),
	};
	if ($ENV{'QUERY_STRING'} eq 'login' or $ENV{'QUERY_STRING'} eq 'registrazione')
	{
		$file='index_temp.html';
	}
	if ($ENV{'QUERY_STRING'} eq 'account')
	{
		$file='account_temp.html';
	}
}
	$template->process($file,$vars) || die $template->error();

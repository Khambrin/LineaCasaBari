#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use XML::LibXML;
use Template;
use CGI::Session;

my $cgi=new CGI;

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Utenti.xml");
my @messaggi=();
my %values;
foreach my $p (param())
{
	$values{$p}=param($p);
}

$values{email}=lc $values{email};

if ($doc->findnodes("Utenti/Utente/Email[text()='$values{email}']"))
{
	if (!$doc->findnodes("Utenti/Utente[Email[text()='$values{email}']]/Password[text()='$values{password}']"))
	{
		push @messaggi, "La password inserita &egrave errata";
	}
}
else
{
	push @messaggi, "L'email inserita &egrave errata";
}

if (@messaggi)
{
	print $cgi->header('text/html');
	my $file='login_temp.html';
	my $vars={
		'messaggio' => "<ul>"."<li>@messaggi</li>"."</ul>",
		'query_string' => "$values{query_string}",
		};
	my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
	$template->process($file,$vars) || die $template->error();
}
else
{
	my $amministratore=$doc->findvalue("Utenti/Utente[Email[text()='$values{email}']]/Amministratore");
	my $session=new CGI::Session("driver:File",undef,{Directory=>File::Spec->tmpdir});
	my $cookie=$cgi->cookie(CGISESSID => $session->id);
	$session->param("email", $values{email});
	$session->param("amministratore", $amministratore);
	if ($values{query_string} && $values{query_string} ne "impostazioni_account") {
	print $cgi->redirect(-uri => 'check_session.cgi?'."$values{query_string}", -cookie => $cookie);
	} else {
	print $cgi->redirect(-uri => 'check_session.cgi?login', -cookie => $cookie);
	}
}

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
my @errors=();
my %values;
foreach my $p (param())
{
	$values{$p}=param($p);
}

if ($doc->findnodes("Utenti/Utente/Email[text()='$values{email}']"))
{
	if (!$doc->findnodes("Utenti/Utente[Email[text()='$values{email}']]/Password[text()='$values{password}']"))
	{
		push @errors, "La password inserita è errata.";
	}
}
else
{
	push @errors, "L'email inserita è errata.";
}

if (@errors)
{
	print $cgi->header('text/html');
	my $file='login_temp.html';
	my $vars={
		'error' => "<ul>"."<li>[@errors]</li>"."</ul>"
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
	print $cgi->redirect(-uri => 'check_session.cgi?login', -cookie => $cookie);
}

#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use XML::LibXML;
use Template;
use CGI::Session;

my $cgi=new CGI;

print $cgi->header('text/html');

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
=pod
	open(FORM,'../public_html/login.html') or die $!;
	my $form=join('',<FORM>);
	close(FORM);
	my $error_message="<ul>"."<li>[@errors]</li>"."</ul>";
	$form=~ s/<!--error_message-->/$error_message/;
	my $original_css='<link href="LineaCasaBari.css" rel="stylesheet" type="text/css" media="screen"/>';
	my $correct_css='<link href="../LineaCasaBari.css" rel="stylesheet" type="text/css" media="screen"/>';
	$form=~ s/$original_css/$correct_css/;
	my $original_jquery='<script type="text/javascript" src="jquery-1.12.0.js"></script>';
	my $correct_jquery='<script type="text/javascript" src="../jquery-1.12.0.js"></script>';
	$form=~ s/$original_jquery/$correct_jquery/;
	my $original_linkskipper='<script type="text/javascript" src="link_skipper.js"></script>';
	my $correct_linkskipper='<script type="text/javascript" src="../link_skipper.js"></script>';
	$form=~ s/$original_linkskipper/$correct_linkskipper/;
	print $form;
=cut
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
	my $session=new CGI::Session("driver:File",undef,{Directory=>File::Spec->tmpdir});
	my $cookie=$cgi->cookie(CGISESSID => $session->id);
	$session->param('email', $values{email});
	print $cgi->redirect(-uri => 'home_script.cgi', -cookie => $cookie);
}

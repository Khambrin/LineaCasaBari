#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;

my $cgi=new CGI;

my $session = CGI::Session->load();
if ($session->is_empty)
{
	print $cgi->header('text/html');

	my $file='home_temp.html';
	my $vars={
		'check' => "false",
		'test' => "false",
	};
	my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
	$template->process($file,$vars) || die $template->error();
}
else
{
	print $cgi->header('text/html');
	my $file='home_temp.html';
	my $vars={
		'check' => "false",
		'test' => "true",
		'email' => $session->param("email"),
	};
	my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
	$template->process($file,$vars) || die $template->error();
}

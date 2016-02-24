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


my $session = CGI::Session->load();
if (!$session->is_empty)
{
	my $file='home_temp.html';
	my $vars={
		
	};
	my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
	$template->process($file,$vars) || die $template->error();
}
else
{
	print $cgi->redirect('../public_html/home.html');
}



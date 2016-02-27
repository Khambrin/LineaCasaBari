#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use XML::LibXML;
use Template;
use CGI::Session;
use Switch;

my $cgi=new CGI;

my $session = CGI::Session->load();

if ($session->is_empty)
{
	print $cgi->redirect("check_session.cgi?$ENV{'QUERY_STRING'}");
}
else
{	
	print $cgi->redirect("check_session.cgi?$ENV{'QUERY_STRING'}");
}

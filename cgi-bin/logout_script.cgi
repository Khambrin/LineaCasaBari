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
$session->delete();
$session->flush();

print $cgi->redirect('../public_html/home.html');


#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use CGI::Session;


my $cgi=new CGI;

my $session = CGI::Session->load();
$session->delete();
$session->flush();

print $cgi->redirect('check_session.cgi?index');


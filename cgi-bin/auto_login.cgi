#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use CGI::Session;

my $cgi=new CGI;

my $session=new CGI::Session("driver:File",undef,{Directory=>File::Spec->tmpdir});
my $cookie=$cgi->cookie(CGISESSID => $session->id);
$session->param("email", $ENV{'QUERY_STRING'});
print $cgi->redirect(-uri => 'check_session.cgi?login', -cookie => $cookie);

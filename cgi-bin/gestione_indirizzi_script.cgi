#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use XML::LibXML;

my $cgi=new CGI;

my $session = CGI::Session->load();
if ($session->is_empty) {
	print $cgi->redirect('check_session.cgi?indirizzi');
}
my $email=$session->param("email");

my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my $hidden='<input type="hidden" name="pagina" value="'."$ENV{'QUERY_STRING'}".'"/>';
my $file='indirizzi_temp.html';
my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'pagina' => $ENV{'QUERY_STRING'},
		'hidden' => $hidden,
	};
print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

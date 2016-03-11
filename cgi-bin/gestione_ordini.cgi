#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use XML::Twig;

my $cgi=new CGI;
print $cgi->header('text/html');
my $session = CGI::Session->load();
my $email=$session->param("email");

my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my $vecchio_ordine= param("vecchio_ordine");

my $twig=XML::Twig->new(
    pretty_print  => 'indented',
    twig_handlers => { 
        name => sub { 
            $_->set_text( 'culo' )->flush  if $_->text eq 'abari@gmail.com' 
        },
    },
    );
$twig->parsefile_inplace( '../data/Ordini.xml');





my $file='gestione_ordini_temp.html';
my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'list' => "false",
		'messaggio' => "modifica effettuata",
		};
$template->process($file,$vars) || die $template->error();


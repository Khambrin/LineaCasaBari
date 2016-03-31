#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use XML::LibXML;
use File::Basename;

my $cgi=new CGI;

my $session = CGI::Session->load();
my $email=$session->param("email");
my $amministratore=$session->param("amministratore");

my $vars;
my $void_address;


my $mail_iscrizione =$cgi->param('iscrizione');
my $page_nl =$cgi->param('pagina_nl');

if (!$mail_iscrizione)
{
	$void_address="Inserire un indirizzo email";
}


if ($void_address)
{
	print $cgi->header('text/html');
	my $file=$page_nl;
	if ($session->is_empty)
	{
		$vars={
			'sessione' => "false",
			'messaggio' => $void_address,
		};
	}

	else
	{
		$vars={
			'sessione' => "true",
			'email' => $email,
			'amministratore' => $amministratore,
			'messaggio' => $void_address,
		};
	}
	
	
	my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
	$template->process($file,$vars) || die $template->error();
}
else
{
	my $doc,my $root; my $greetings="Iscrizione alla newsletter avvenuta con successo";
	if (-e "../data/Newsletter.xml")
	{
		my $parser=XML::LibXML->new();
		$doc=$parser->parse_file("../data/Newsletter.xml");
		$root=$doc->documentElement();
	}
	else
	{
		$doc=XML::LibXML::Document->new("1.0","UTF-8");
		$root=$doc->createElement("Newsletter");
		$doc->setDocumentElement($root);
	}

	my $mail_tag=$doc->createElement("mail");
	$mail_tag->appendTextNode($mail_iscrizione);
	$root->appendChild($mail_tag);
	
	print $cgi->header('text/html');
	my $file=$page_nl;
	if ($session->is_empty)
	{
		$vars={
			'sessione' => "false",
			'iscrizione_avvenuta' => $greetings,
		};
	}

	else
	{
		$vars={
			'sessione' => "true",
			'email' => $email,
			'amministratore' => $amministratore,
			'iscrizione_avvenuta' => $greetings,
		};
	}
	
	
	my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
	$template->process($file,$vars) || die $template->error();

	open (XML,">","../data/Newsletter.xml");
	print XML $doc->toString();
	close(XML);
	



}


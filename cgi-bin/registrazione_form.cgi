#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use XML::LibXML;
use Template;

my $cgi=new CGI;

my @messaggi=();
my %values;

foreach my $p (param())
{
	$values{$p}=param($p);
}

my $pwd=$values{"password"};
foreach my $chiave (keys %values)
{
	if (!$values{$chiave})
	{
		push @messaggi, "Devi completare il campo '$chiave'.";
	}
	if ($chiave eq "email")
	{
		#controlli sul campo email
		if (!$values{$chiave}=~ /^[^ ,@]+\@([a-z0-9-]+\.)+[a-z]+$/)
		{
			push @messaggi, "Indirizzo email inserito non valido.";
		}
	}
	if ($chiave eq "password")
	{
		#controlli sul campo password
		
	}
	if ($chiave eq "conf_password")
	{
		if ($values{$chiave} ne $pwd)
		{
			push @messaggi, "La conferma della password non corrisponde.";
		}
	}
}

if (@messaggi)
{
	print $cgi->header('text/html');
	my $file='registrazione_temp.html';
	my $vars={
		'messaggio' => "<ul>"."<li>[@messaggi]</li>"."</ul>"
	};
	my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
	$template->process($file,$vars) || die $template->error();
}
else
{
	my $doc,my $root;
	if (-e "../data/Utenti.xml")
	{
		my $parser=XML::LibXML->new();
		$doc=$parser->parse_file("../data/Utenti.xml");
		$root=$doc->documentElement();
	}
	else
	{
		my $doc=XML::LibXML::Document->new("1.0","UTF-8");
		my $root=$doc->createElement("Utenti");
		$doc->setDocumentElement($root);
	}
	my $utente_tag=$doc->createElement("Utente");
		$root->appendChild($utente_tag);
		my @value_tags=("Nome","Cognome","Email","Password");
		foreach my $k (@value_tags)
		{
			my $value_tag=$doc->createElement($k);
			$value_tag->appendTextNode($values{lc $k});
			$utente_tag->appendChild($value_tag);
		}
		
		my @novalue_tags=("Telefono","Amministratore");
		foreach my $i (@novalue_tags)
		{
			my $novalue_tag=$doc->createElement($i);
			if ($i eq "Amministratore")
			{
				$novalue_tag->appendTextNode("false");
			}
			$utente_tag->appendChild($novalue_tag);
		}
		open (XML,">","../data/Utenti.xml");
		print XML $doc->toString();
		close(XML);
		print $cgi->redirect("auto_login.cgi?$values{'email'}");
}


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

my $doc;
my $parser=XML::LibXML->new();
$doc=$parser->parse_file("../data/Utenti.xml");
my @lista_email=$doc->findnodes("Utenti/Utente/Email/text()");

my $pwd=$values{"password"};
my $email_value=$values{'email'};
foreach my $chiave (keys %values)
{
	if (!$values{$chiave})
	{
		if($chiave eq "conf_password")
		{
			push @messaggi, "Devi confermare la password";
		}
		else
		{
			push @messaggi, "Devi completare il campo '$chiave'";
		}
	}
	elsif ($chiave eq "email")
	{
		#controlli sul campo email
		my $email=$values{$chiave};
		my $regex=$email=~ /^[a-z0-9.]+\@[a-z0-9.-]+$/;
		if (not $regex)
		{
			push @messaggi, "Indirizzo email inserito non valido";
			$email_value="";
		}
		if (grep( /^$email_value$/, @lista_email )) {
			push @messaggi, "Indirizzo email gi&aacute; utilizzato"
		}
	}
	elsif ($chiave eq "password")
	{
		
		if (length($pwd)>20)
		{
			push @messaggi, "La password inserita &egrave troppo lunga, massimo 20 caratteri";
		}
		if (length($pwd)<8)
		{
			push @messaggi, "La password inserita &egrave troppo corta, minimo 8 caratteri";
		}
		if ($values{$chiave} =~ m/[^a-zA-Z0-9]/)
		{
			push @messaggi, "La password inserita contiene caratteri non consentiti, caratteti permessi lettere minuscole maiuscole e numeri";
		}
	}
	elsif ($chiave eq "conf_password")
	{
		if ($values{$chiave} ne $pwd)
		{
			push @messaggi, "Le password non corrispondono";
		}
	}
}

if (@messaggi)
{
	print $cgi->header('text/html');
	my $file='registrazione_temp.html';
	my $tot;
	my $x;
	my $i=0;
	foreach my $k (@messaggi)
	{
		my $aux=@messaggi[$i];
		$i=$i+1;
		$x="<li>"."$aux".'</li>'; 
		$tot=$tot.$x;
	}
	$tot="<ul>"."$tot"."</ul>";
	my $vars={
		'messaggio_registrazione'=> $tot,
		'nomeValue'=> 'value="'."$values{'nome'}".'"',
		'cognomeValue'=> 'value="'."$values{'cognome'}".'"',
		'emailValue'=> 'value="'."$email_value".'"',
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
		print $cgi->redirect("check_session.cgi?registrato");
}



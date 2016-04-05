#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use Switch;
use XML::LibXML;
use File::Basename;

my $cgi=new CGI;

my $session = CGI::Session->load();
my $email=$session->param("email");
my $amministratore=$session->param("amministratore");
my @errors=();
my %values;


my $parser=XML::LibXML->new;


foreach my $p (param())
{
	$values{$p}=param($p);
}

if (!$values{"nuova_email"})
{
	push @errors, "Devi completare il campo email.";
}
if (!$values{"vecchia_password"})
{
	push @errors, "Devi inserire la password corrente.";
}
if (!$values{"nuova_password"})
{
	push @errors, "Devi inserire la nuova password.";
}

if (@errors)
{
	print $cgi->header('text/html');
	my $file='impostazioni_account_temp.html';
	my $error_message_aux;
	foreach my $i (@errors)
	{
		my $x="<li>$i".'</li>';
		$error_message_aux=$error_message_aux.$x;
	}
	my $error_message="<ul>"."$error_message_aux"."</ul>";
	my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => $amministratore,
		'error' => $error_message,
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
		$doc=XML::LibXML::Document->new("1.0","UTF-8");
		$root=$doc->createElement("Annunci");
		$doc->setDocumentElement($root);
	}
	####
	$old_pw=$doc->findnodes("Utenti/Utente[Email='$email']/Password/text()");
	if ($values{"vacchia_password"}!=$old_pw)
	{
		push @errors, "Password corrente errata. Inserire la password corrente per apportare modifiche all'account.";
	}
	if (@errors)
	{
		print $cgi->header('text/html');
		my $file='impostazioni_account_temp.html';
		my $error_message_aux;
		foreach my $i (@errors)
		{
			my $x="<li>$i".'</li>';
			$error_message_aux=$error_message_aux.$x;
		}
		my $error_message="<ul>"."$error_message_aux"."</ul>";
		my $vars={
			'sessione' => "true",
			'email' => $email,
			'amministratore' => $amministratore,
			'error' => $error_message,
		};
		my $template=Template->new({
			INCLUDE_PATH => '../public_html/temp',
		});
		$template->process($file,$vars) || die $template->error();
	}
	
	
	####
	
	my $utente_node=$doc->findnodes("Utenti/Utente[Email='$email']");
	my $via=$doc->findnodes("Utenti/Utente[Email='$email']/Indirizzo/Via/Text()");
	my $ncivico=$doc->findnodes("Utenti/Utente[Email='$email']/Indirizzo/Numero_civico/Text()");
	my $citta=$doc->findnodes("Utenti/Utente[Email='$email']/Indirizzo/Città/Text()");
	my $prov=$doc->findnodes("Utenti/Utente[Email='$email']/Indirizzo/Provincia/Text()");
	my $cap=$doc->findnodes("Utenti/Utente[Email='$email']/Indirizzo/CAP/Text()");
	my $admin=$doc->findnodes("Utenti/Utente[Email='$email']/Amministratore/Text()");

	$utente_node->[0]->parentNode->removeChild($annuncio_node->[0]);

	my $utente_tag=$doc->createElement("Utente");	
	$root->appendChild($utente_tag);
	
	
	my $nome_tag=$doc->createElement("Nome");
	$nome_tag->appendTextNode($values{'nuovo_nome'});
	$utente_tag->appendChild($nome_tag);
	
	my $cognome_tag=$doc->createElement("Cognome");
	$cognome_tag->appendTextNode($values{'nuovo_cognome'});
	$utente_tag->appendChild($nome_tag);

	my $telefono_tag=$doc->createElement("Telefono");
	$telefono_tag->appendTextNode($values{'nuovo_telefono'});
	$utente_tag->appendChild($telefono_tag);
	
	my $email_tag=$doc->createElement("Email");
	$email_tag->appendTextNode($values{'nuova_email'});
	$utente_tag->appendChild($email_tag);

	my $password_tag=$doc->createElement("Password");
	$password_tag->appendTextNode($values{'nuova_password'});
	$utente_tag->appendChild($password_tag);
	#
	my $admin_tag=$doc->createElement("Amministratore");
	$admin_tag->appendTextNode($admin);
	$utente_tag->appendChild($password_tag);
	#creare indirizzo tag
	my $indirizzo_tag=$doc->createElement("Indirizzo");	
	$utente_tag->appendChild($indirizzo_tag);
	#
	my $admin_tag=$doc->createElement("Via");
	$admin_tag->appendTextNode($admin);
	$indirizzo_tag->appendChild($admin_tag);

	my $ncivico_tag=$doc->createElement("Numero_civico");
	$ncivico_tag->appendTextNode($ncivico);
	$indirizzo_tag->appendChild($ncivico_tag);

	my $citta_tag=$doc->createElement("Città");
	$citta_tag->appendTextNode($citta);
	$indirizzo_tag->appendChild($citta_tag);

	my $prov_tag=$doc->createElement("Provincia");
	$prov_tag->appendTextNode($prov);
	$indirizzo_tag->appendChild($prov_tag);

	my $cap_tag=$doc->createElement("CAP");
	$cap_tag->appendTextNode($cap);
	$indirizzo_tag->appendChild($cap_tag);
	#
	open (XML,">","../data/Utenti.xml");
	print XML $doc->toString();
	close(XML);
	print $cgi->redirect("gestione_account.cgi");

}

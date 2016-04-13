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
	push @errors, "Devi inserire l'indirizzo email.";
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

	my $parser=XML::LibXML->new();
	my $doc=$parser->parse_file("../data/Utenti.xml");
	my $root=$doc->documentElement();
	
	
	my $old_name=$doc->findnodes("Utenti/Utente[Email='$email']/Nome/text()");
	my $old_surname=$doc->findnodes("Utenti/Utente[Email='$email']/Cognome/text()");
	my $old_tel=$doc->findnodes("Utenti/Utente[Email='$email']/Telefono/text()");

	my $old_em_form='<input class= "input" type="text" name="nuova_email" value="'."$email".'"/>';
	my $old_name_form='<input class= "input" type="text" name="nuovo_nome" value="'."$old_name".'"/>';
	my $old_surname_form='<input class= "input" type="text" name="nuovo_cognome" value="'."$old_surname".'"/>';
	my $old_tel_form='<input class= "input" type="text" name="nuovo_telefono" value="'."$old_tel".'"/>';
	
	my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => $amministratore,
		'messaggio' => $error_message,
		'vemail'=>$old_em_form,
		'vnome'=>$old_name_form,
		'vcognome'=>$old_surname_form,
		'vtelefono'=>$old_tel_form,
	};
	my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
	$template->process($file,$vars) || die $template->error();
}
else
{
	
	my $doc,my $root;
	
	my $parser=XML::LibXML->new();
	$doc=$parser->parse_file("../data/Utenti.xml");
	$root=$doc->documentElement();
	
	my $old_pw=$doc->findnodes("Utenti/Utente[Email='$email']/Password/text()");
	if ($values{"vecchia_password"} ne $old_pw)
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

		my $old_name=$doc->findnodes("Utenti/Utente[Email='$email']/Nome/text()");
		my $old_surname=$doc->findnodes("Utenti/Utente[Email='$email']/Cognome/text()");
		my $old_tel=$doc->findnodes("Utenti/Utente[Email='$email']/Telefono/text()");

		my $old_em_form='<input class= "input" type="text" name="nuova_email" value="'."$email".'"/>';
		my $old_name_form='<input class= "input" type="text" name="nuovo_nome" value="'."$old_name".'"/>';
		my $old_surname_form='<input class= "input" type="text" name="nuovo_cognome" value="'."$old_surname".'"/>';
		my $old_tel_form='<input class= "input" type="text" name="nuovo_telefono" value="'."$old_tel".'"/>';

		my $vars={
			'sessione' => "true",
			'email' => $email,
			'amministratore' => $amministratore,
			'messaggio' => $error_message,
			'vemail'=>$old_em_form,
			'vnome'=>$old_name_form,
			'vcognome'=>$old_surname_form,
			'vtelefono'=>$old_tel_form,
		};
		my $template=Template->new({
			INCLUDE_PATH => '../public_html/temp',
		});
		$template->process($file,$vars) || die $template->error();
	}
	
	my $utente_node=$doc->findnodes("Utenti/Utente[Email='$email']");

	my $admin=$doc->findnodes("Utenti/Utente[Email='$email']/Amministratore");

	$utente_node->[0]->parentNode->removeChild($utente_node->[0]);

	my $utente_tag=$doc->createElement("Utente");	
	$root->appendChild($utente_tag);
	
	
	my $nome_tag=$doc->createElement("Nome");
	$nome_tag->appendTextNode($values{'nuovo_nome'});
	$utente_tag->appendChild($nome_tag);
	
	my $cognome_tag=$doc->createElement("Cognome");
	$cognome_tag->appendTextNode($values{'nuovo_cognome'});
	$utente_tag->appendChild($cognome_tag);

	my $telefono_tag=$doc->createElement("Telefono");
	$telefono_tag->appendTextNode($values{'nuovo_telefono'});
	$utente_tag->appendChild($telefono_tag);
	
	my $email_tag=$doc->createElement("Email");
	$email_tag->appendTextNode($values{'nuova_email'});
	$utente_tag->appendChild($email_tag);

	my $password_tag=$doc->createElement("Password");
	$password_tag->appendTextNode($values{'nuova_password'});
	$utente_tag->appendChild($password_tag);
	
	my $admin_tag=$doc->createElement("Amministratore");
	$admin_tag->appendTextNode($admin);
	$utente_tag->appendChild($admin_tag);
	
	$session->param("email", $values{nuova_email});

	open (XML,">","../data/Utenti.xml");
	print XML $doc->toString();
	close(XML);

	use XML::LibXML;
	$parser=XML::LibXML->new();
	$doc=$parser->parse_file("../data/Indirizzi.xml");
	$root=$doc->documentElement();
	
	my $ric_canc=$doc->findnodes("Indirizzi/Utente[Email='$email']/Email/text()");
	if($ric_canc eq $email)
	{
		my $utente_canc=$doc->findnodes("Indirizzi/Utente[Email='$email']");
		my $email_canc=$doc->findnodes("Indirizzi/Utente[Email='$email']/Email");
	
		my $newemail_tag=$doc->createElement("Email");
		$newemail_tag->appendTextNode($values{'nuova_email'});
		$utente_canc->[0]->appendChild($newemail_tag); 
	
		$email_canc->[0]->parentNode->removeChild($email_canc->[0]);
	}
		
	open (XML,">","../data/Indirizzi.xml");
	print XML $doc->toString();
	close(XML);

	print $cgi->redirect("gestione_account.cgi");

}

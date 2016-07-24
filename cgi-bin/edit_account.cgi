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

my $doc;
my $parser=XML::LibXML->new();
$doc=$parser->parse_file("../data/Utenti.xml");
my $root=$doc->documentElement();
my @lista_email=$doc->findnodes("Utenti/Utente/Email/text()");


foreach my $p (param())
{
	$values{$p}=param($p);
}

if ($values{"nuova_password"} and !$values{"vecchia_password"})
{
	push @errors, "Devi inserire la vecchia password per poterla cambiare.";
}

if($values{"nuova_email"} ne $email)
{
	my $regex=$values{"nuova_email"}=~ /^[a-z0-9.]+\@[a-z0-9.-]+$/;
	if (not $regex)
	{
		push @errors, "Indirizzo email inserito non valido";
	}
	if (grep( /^$values{"nuova_email"}$/, @lista_email ))
	{
		push @errors, "Indirizzo email gi&agrave; utilizzato"
	}
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
	
	my $old_no=$doc->findnodes("Utenti/Utente[Email='$email']/Nome/text()");
	my $old_co=$doc->findnodes("Utenti/Utente[Email='$email']/Cognome/text()");
	my $old_em=$email;
	my $old_psw=$doc->findnodes("Utenti/Utente[Email='$email']/Password/text()");
	my $old_tel=$doc->findnodes("Utenti/Utente[Email='$email']/Telefono/text()");
	my $old_amm=$doc->findnodes("Utenti/Utente[Email='$email']/Amministratore/text()");

	my $utente_node=$doc->findnodes("Utenti/Utente[Email='$email']");
	$utente_node->[0]->parentNode->removeChild($utente_node->[0]);

	my $utente_tag=$doc->createElement("Utente");	
	$root->appendChild($utente_tag);
	
	my $nome_tag=$doc->createElement("Nome");
	if($values{'nuovo_nome'})
	{
		$nome_tag->appendTextNode($values{'nuovo_nome'});
	}
	else
	{
		$nome_tag->appendTextNode($old_no);
	}
	$utente_tag->appendChild($nome_tag);
	
	my $cognome_tag=$doc->createElement("Cognome");
	if($values{'nuovo_cognome'})
	{
		$cognome_tag->appendTextNode($values{'nuovo_cognome'});
	}
	else
	{
		$cognome_tag->appendTextNode($old_co);
	}
	$utente_tag->appendChild($cognome_tag);

	my $telefono_tag=$doc->createElement("Telefono");
	if($values{'nuovo_telefono'})
	{
		$telefono_tag->appendTextNode($values{'nuovo_telefono'});
	}
	else
	{
		$telefono_tag->appendTextNode($old_tel);
	}	
	$utente_tag->appendChild($telefono_tag);
	
	my $email_tag=$doc->createElement("Email");
	if($values{'nuova_email'})
	{
		$email_tag->appendTextNode($values{'nuova_email'});
		$session->param("email", $values{'nuova_email'});
	}
	else
	{
		$email_tag->appendTextNode($old_em);
	}
	$utente_tag->appendChild($email_tag);

	my $password_tag=$doc->createElement("Password");
	if($values{'nuova_password'})
	{
		$password_tag->appendTextNode($values{'nuova_password'});
	}
	else
	{
		$password_tag->appendTextNode($old_psw);
	}
	$utente_tag->appendChild($password_tag);
	
	my $admin_tag=$doc->createElement("Amministratore");
	$admin_tag->appendTextNode($old_amm);
	$utente_tag->appendChild($admin_tag);
		
	

	open (XML,">","../data/Utenti.xml");
	print XML $doc->toString();
	close(XML);

	$parser=XML::LibXML->new();
	$doc=$parser->parse_file("../data/Indirizzi.xml");
	$root=$doc->documentElement();
		
	my $utente_canc=$doc->findnodes("Indirizzi/Utente[Email='$email']");
	
	my $email_canc=$doc->findnodes("Indirizzi/Utente[Email='$email']/Email");
	my $newemail_tag=$doc->createElement("Email");
	$newemail_tag->appendTextNode($values{'nuova_email'});
	$utente_canc->[0]->appendChild($newemail_tag); 
	$email_canc->[0]->parentNode->removeChild($email_canc->[0]);
		
	open (XML,">","../data/Indirizzi.xml");
	print XML $doc->toString();
	close(XML);

	$parser=XML::LibXML->new();
	$doc=$parser->parse_file("../data/Ordini.xml");
	$root=$doc->documentElement();
	
	my $utente_canc=$doc->findnodes("Ordini/Ordine[Utente='$email']");
	
	my $email_canc=$doc->findnodes("Ordini/Ordine[Utente='$email']/Utente");
	my $newemail_tag=$doc->createElement("Utente");
	$newemail_tag->appendTextNode($values{'nuova_email'});
	$utente_canc->[0]->appendChild($newemail_tag); 
	$email_canc->[0]->parentNode->removeChild($email_canc->[0]);
	
			
	open (XML,">","../data/Ordini.xml");
	print XML $doc->toString();
	close(XML);

	print $cgi->redirect("check_session.cgi?gestione_account_mod");
}



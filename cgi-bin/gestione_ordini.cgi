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

my vecchio_ordine= param("vecchio_ordine");
my $twig = XML::Twig -> parse_file ("../data/Ordini.xml" ); 

if ($twig -> get_xpath("Ordini/Ordine[Codice='$vecchio_ordine']")) 
{
	my $add_to = $twig -> get_xpath ( "Ordini/Ordine/Codice", param("Codice") ); 
	$add_to = $twig -> get_xpath ( "Ordini/Ordine/Utente", param("Utente") );
	$add_to = $twig -> get_xpath ( "Ordini/Ordine/Data", param("Data") );
	for(my $i=1;$i<=param("numero_prodotti");$i++)
	{
		$add_to = $twig -> get_xpath ( "Ordini/Ordine/Prodotto[$i]", param("Prodotto[$i]") );
	}
	$add_to -> insert_new_elt ( 'last_child', 'param', { name => "another_setting" }, "Content here" );

	$twig -> set_pretty_print("indented_a");
	$twig -> print;
    
}






my $file='gestione_ordini_temp.html';
my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'list' => "false",
		'messaggio' => "modifica effettuata",
		};
$template->process($file,$vars) || die $template->error();


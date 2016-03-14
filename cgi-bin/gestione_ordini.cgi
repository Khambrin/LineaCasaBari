#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use XML::LibXML;

my $cgi=new CGI;
print $cgi->header('text/html');
my $session = CGI::Session->load();
my $email=$session->param("email");
my @error;

my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my $prodotto=param("Prodotto"),my $parser,my $doc;
print $prodotto;
=pod
if($vecchio_ordine eq $new_codice)
{
	push @error, "codice ordine gi&agrave esistente";
	print $cgi->redirect("ricerca_ordini.cgi?lista_ordine");
}
else
{
	$parser = XML::LibXML->new();
    $doc=$parser->parse_file("../data/Ordini.xml");
    my $ordine_node=$doc->findnodes("Oridini/Ordine[Codice='$vecchio_ordine']");
	$ordine_node->[0]->parentNode->removeChild($ordine_node->[0]);
	open(XML,">","../data/Ordini.xml");
	print XML $doc->toString();
	close(XML);
}


my $file='gestione_ordini_temp.html';
my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'list' => "true",
		'error' =>@error,
		};
$template->process($file,$vars) || die $template->error();


=cut

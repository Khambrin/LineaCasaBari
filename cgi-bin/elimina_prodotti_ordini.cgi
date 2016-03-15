#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use Switch;
use XML::LibXML;

my $cgi=new CGI;
print $cgi->header('text/html');
my $session = CGI::Session->load();
my $email=$session->param("email");
print $cgi->header('text/html');
my $parser,my $doc;
my $num_prodotti=param("num_prodotti");
my $cod_ordine=param("ordine");
print $cod_ordine;
print $cgi->header('text/html');
print $num_prodotti;
for (my $i=1; $i<=$num_prodotti;$i++)
{
	if($cgi->param($i) == 'on')
	{
		
		$parser=XML::LibXML->new;
		$doc=$parser->parse_file("../data/Ordini.xml");
		my $ordine = $doc->findnodes("Ordini/Ordine[Codice='$cod_ordine']/Prodotto[$i]");
		$ordine->[0]->parentNode->removeChild($ordine->[0]);
		
	}	
}
open(XML,">","../data/Ordini.xml");
print XML $doc->toString();
close(XML);






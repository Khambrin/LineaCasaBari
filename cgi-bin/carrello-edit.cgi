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
my $session = CGI::Session->load();
my $email=$session->param("email");

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Carrelli.xml");
my $num_prodotti=$doc->findvalue("count(Carrelli/Carrello[Utente='$email']/Elemento)");
my @all_quantita;
my @all_prodotti;

for(my $i=0; $i<$num_prodotti;$i++)
{
	if(param("togli_quantita-"."$i"))
	{
		@all_quantita[$i]=param("togli_quantita-"."$i");
	}
	else
	{
		@all_quantita[$i]=0;
	}
	
	if(param("elimina_prodotto-"."$i"))
	{
		@all_prodotti[$i]=1;
	}
	else
	{
		@all_prodotti[$i]=0;
	}
}

my $elimina_prodotto=0;
my $counterp=1;
for (my $i=0; $i< $num_prodotti; $i++)
{
	if (@all_quantita[$i] > 0) 
	{
		my @quantita_esistente=$doc->findnodes("Carrelli/Carrello[Utente='$email']/Elemento[$counterp]/Quantita/text()");
		my $aux=@quantita_esistente[0]->string_value;
		my $aux1=@all_quantita[$i];
		my $diff=$aux-$aux1;
		if($diff>0)
		{
			my @quantita_node=$doc->findnodes("Carrelli/Carrello[Utente='$email']/Elemento[$counterp]/Quantita");
			@quantita_node[0]->parentNode->removeChild(@quantita_node[0]);
			my $quantita_tag=$doc->createElement("Quantita");
			my @element_node=$doc->findnodes("Carrelli/Carrello[Utente='$email']/Elemento[$counterp]");
			@element_node[0]->appendChild($quantita_tag);
			$quantita_tag->appendTextNode($diff);
		}
		else
		{
			$elimina_prodotto=1;
		}
	}			
	if (@all_prodotti[$i]==1 or ($elimina_prodotto==1))
	{
		my @prodotto = $doc->findnodes("Carrelli/Carrello[Utente='$email']/Elemento[$counterp]/Prodotto");
		@prodotto->[0]->parentNode->removeChild(@prodotto->[0]);
		
		my @quantita = $doc->findnodes("Carrelli/Carrello[Utente='$email']/Elemento[$counterp]/Quantita");
		@quantita->[0]->parentNode->removeChild(@quantita->[0]);
		
		my @elemento = $doc->findnodes("Carrelli/Carrello[Utente='$email']/Elemento[$counterp]");
		@elemento->[0]->parentNode->removeChild(@elemento->[0]);
		$elimina_prodotto=0;
		
		my $num_elementi=$doc->findvalue("count(Carrelli/Carrello[Utente='$email']/Elemento)");

		if($num_elementi ==0)
		{
			
			my @carrello = $doc->findnodes("Carrelli/Carrello[Utente='$email']");
			@carrello->[0]->parentNode->removeChild(@carrello->[0]);
		}
	}
	else
	{
		$counterp++;
	}
}

open(XML,">","../data/Carrelli.xml");
print XML $doc->toString();
close(XML);
print $cgi->redirect("check_session.cgi?carrello-modificato");




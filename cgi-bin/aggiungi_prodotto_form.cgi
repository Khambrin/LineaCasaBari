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
my $pagina=param("pagina");
my @messaggi=();
my %values;

foreach my $p (param())
{
	$values{$p}=param($p);
}

if (!$values{"nome"})
{
	push @messaggi, "Devi completare il campo nome.";
}
if (!$values{"prezzo"})
{
	push @messaggi, "Devi completare il campo prezzo.";
}
if (!$values{"descrizione"})
{
	push @messaggi, "Devi completare il campo descrizione.";
}


my $regex=$values{"prezzo"}=~ /^[0-9]+\,[0-9]{2}$/;
{
	if(!$regex){push @messaggi, "Inserisci un prezzo valido";}
}

if ($values{"immagine"}) {
	my $image_size = -s $values{"immagine"};
	if($image_size > 200000) {push @messaggi, "Immagine troppo grande";}
}

if (@messaggi)
{
	print $cgi->header('text/html');
	my $file='gestione_prodotti_temp.html';
	my $error_message_aux;
	foreach my $i (@messaggi)
	{
		my $x="<li>$i".'</li>';
		$error_message_aux=$error_message_aux.$x;
	}
	my $error_message="<ul>"."$error_message_aux"."</ul>";
	my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'messaggio' => $error_message,
		'pagina' => $pagina,
	};
	my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
	$template->process($file,$vars) || die $template->error();
}
else
{
	my $doc,my $root;
	my $id=0, my $valutazione="";
	if (-e "../data/Prodotti.xml")
	{
		my $parser=XML::LibXML->new();
		$doc=$parser->parse_file("../data/Prodotti.xml");
		$root=$doc->documentElement();
		my $last_id=$doc->findvalue("Prodotti/Prodotto[last()]/Codice");
		$id=$last_id+1;
	}
	else
	{
		$doc=XML::LibXML::Document->new("1.0","UTF-8");
		$root=$doc->createElement("Prodotti");
		$doc->setDocumentElement($root);
		
	}
		my $prodotto_tag=$doc->createElement("Prodotto");	
		$root->appendChild($prodotto_tag);
		
		my $id_tag=$doc->createElement("Codice");
		$id_tag->appendTextNode($id);
		$prodotto_tag->appendChild($id_tag);
		
		my @value_tags=("Nome","Descrizione","Categoria","Prezzo");
		foreach my $k (@value_tags)
		{
			my $value_tag=$doc->createElement($k);
			$value_tag->appendTextNode($values{lc $k});
			$prodotto_tag->appendChild($value_tag);
		}
		my ($sec,$min,$hour,$mday,$mon,$yr19,$wday,$yday,$isdst) = localtime(time);
		my $year=$yr19+1900;
		my $date="$mday/$mon/$year";
		my $date_tag=$doc->createElement("Data_aggiunta");
		$date_tag->appendTextNode($date);
		$prodotto_tag->appendChild($date_tag);

		my $valutazione_tag=$doc->createElement("Valutazione");
		$valutazione_tag->appendTextNode($valutazione);
		$prodotto_tag->appendChild($valutazione_tag);

		my $immagine_tag=$doc->createElement("Immagine");
		my $immagine;
		if ($values{'immagine'})
		{
			my $upload_directory="../public_html/images/prodotti";
			my $load_directory="../images/prodotti";
			my $upload_filehandle=$cgi->upload("immagine");
			open (UPLOADFILE,">$upload_directory/$values{'immagine'}") or die "$!";
			binmode UPLOADFILE;
			while (<$upload_filehandle>)
			{
				print UPLOADFILE;
			}
			close UPLOADFILE;
			$immagine="$load_directory/$values{'immagine'}";
		}
		else
		{
			$immagine="";
		}
		$immagine_tag->appendTextNode($immagine);
		$prodotto_tag->appendChild($immagine_tag);
		if ($values{"tag1"})
		{
			my $tag1_tag=$doc->createElement("Tag");
			$tag1_tag->appendTextNode($values{lc"tag1"});
			$prodotto_tag->appendChild($tag1_tag);
		}
		if ($values{"tag2"})
		{
			my $tag2_tag=$doc->createElement("Tag");
			$tag2_tag->appendTextNode($values{lc"tag2"});
			$prodotto_tag->appendChild($tag2_tag);
		}
		if ($values{"tag3"})
		{
			my $tag3_tag=$doc->createElement("Tag");
			$tag3_tag->appendTextNode($values{lc"tag3"});
			$prodotto_tag->appendChild($tag3_tag);
		}
		if ($values{"tag4"})
		{
			my $tag4_tag=$doc->createElement("Tag");
			$tag4_tag->appendTextNode($values{lc"tag4"});
			$prodotto_tag->appendChild($tag4_tag);
		}
		open (XML,">","../data/Prodotti.xml");
		print XML $doc->toString();
		close(XML);
		print $cgi->redirect("gestione_prodotti_script.cgi?aggiungi");
}
		

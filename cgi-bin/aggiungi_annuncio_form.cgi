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
my $titolo_value="";
my $testo_value="";

foreach my $p (param())
{
	$values{$p}=param($p);
}

if (!$values{"titolo"})
{
	push @messaggi, "Devi completare il campo titolo";
}
else
{
	$titolo_value=$values{"titolo"};
}
if (!$values{"testo"})
{
	push @messaggi, "Devi completare il campo testo";
}
else
{
	$testo_value=$values{"testo"};	
}

if (@messaggi)
{
	print $cgi->header('text/html');
	my $file='gestione_annunci_temp.html';
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
		'titolo_value' => 'value="'."$titolo_value".'"',
		'testo_value' => $testo_value,
		'messaggio' => $error_message,
		'pagina' => "aggiungi",
	};
	my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
	$template->process($file,$vars) || die $template->error();
}
else
{
	my $doc,my $root;
	if (-e "../data/Annunci.xml")
	{
		my $parser=XML::LibXML->new();
		$doc=$parser->parse_file("../data/Annunci.xml");
		$root=$doc->documentElement();
	}
	else
	{
		$doc=XML::LibXML::Document->new("1.0","UTF-8");
		$root=$doc->createElement("Annunci");
		$doc->setDocumentElement($root);
	}
	my $find_title=$values{'titolo'};
	my $only=$doc->findnodes("Annunci/Annuncio[Titolo='$find_title']/Titolo/text()");
	if ($find_title eq $only)
	{
		push @messaggi, "Titolo gi&agrave utilizzato.";
		print $cgi->header('text/html');
		my $file='gestione_annunci_temp.html';
		my $error_message_aux;
		foreach my $i (@messaggi)
		{
			my $x="<li>$i".'</li>';
			$error_message_aux=$error_message_aux.$x;
		}
		my $error_message="<ul>"."$error_message_aux"."</ul>";
	
		my $parser=XML::LibXML->new;
		my $doc=$parser->parse_file("../data/Annunci.xml");
		my $template=Template->new({
			INCLUDE_PATH => '../public_html/temp',
		});
	
		my $titolo=$values{"oldtitolo"};
		my $annuncio_node=$doc->findnodes("Annunci/Annuncio[Titolo='$titolo']");
		my $fcontenuto=$doc->findnodes("Annunci/Annuncio[Titolo='$titolo']/Testo/text()");
	
		my $vcontenuto='<textarea id="gestione_annunci-textarea" rows="100" cols="100" name="testo">'."$fcontenuto".'</textarea>';
		my $vt_form='<input class= "input" type="text" name="titolo" value="'."$titolo".'"/>';
		my $hiddentitle='<input class= "input" type="hidden" name="oldtitolo" value="'."$titolo".'"/>';
	
		my $vars={
			'sessione' => "true",
			'email' => $email,
			'amministratore' => "true",
			'messaggio' => $error_message,
			'pagina' => "aggiungi",
			'vtitolo'=>$vt_form,
			'vcontenuto'=>$vcontenuto,
			'oldtitolo'=>$hiddentitle,
		};
		my $template=Template->new({
			INCLUDE_PATH => '../public_html/temp',
		});
		$template->process($file,$vars) || die $template->error();
	}
	else
	{
		my $annuncio_tag=$doc->createElement("Annuncio");	
		$root->appendChild($annuncio_tag);

		my $titolo_tag=$doc->createElement("Titolo");
		$titolo_tag->appendTextNode($values{'titolo'});
		$annuncio_tag->appendChild($titolo_tag);
	
		my ($sec,$min,$hour,$mday,$mon,$yr19,$wday,$yday,$isdst) = localtime(time);
		my $year=$yr19+1900;
		my $date="$mday/$mon/$year";
		my $date_tag=$doc->createElement("Data");
		$date_tag->appendTextNode($date);
		$annuncio_tag->appendChild($date_tag);

		my $testo_tag=$doc->createElement("Testo");
		$testo_tag->appendTextNode($values{'testo'});
		$annuncio_tag->appendChild($testo_tag);

		my $immagine_tag=$doc->createElement("Immagine");
		my $immagine;
		if ($values{'immagine'})
		{
			my $upload_directory="../public_html/images/annunci";
			my $read_directory="../images/annunci";
			my $upload_filehandle=$cgi->upload("immagine");
			open (UPLOADFILE,">$upload_directory/$values{'immagine'}") or die "$!";
			binmode UPLOADFILE;
			while (<$upload_filehandle>)
			{
				print UPLOADFILE;
			}
			close UPLOADFILE;
			$immagine="$read_directory/$values{'immagine'}";
		}
		else
		{
			$immagine=" ";
		}
		$immagine_tag->appendTextNode($immagine);
		$annuncio_tag->appendChild($immagine_tag);
	
		open (XML,">","../data/Annunci.xml");
		print XML $doc->toString();
		close(XML);
		print $cgi->redirect("gestione_annunci_script.cgi?aggiungi");
	}
}

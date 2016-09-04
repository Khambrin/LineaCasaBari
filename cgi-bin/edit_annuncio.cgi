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
if ($session->is_empty) {
	print $cgi->redirect('check_session.cgi?modifica_annunci');
}

my $email=$session->param("email");
my $pagina=param("pagina");
my @errors=();
my %values;

#
my $parser=XML::LibXML->new;
#

foreach my $p (param())
{
	$values{$p}=param($p);
}

if (!$values{"titolo"})
{
	push @errors, "Devi completare il campo titolo.";
}
if (!$values{"testo"})
{
	push @errors, "Devi completare il campo testo.";
}

if ($values{"immagine"}) {
	my $image_size = -s $values{"immagine"};
	if($image_size > 200000) {push @errors, "Immagine troppo grande";}
}


if (@errors)
{
	print $cgi->header('text/html');
	my $file='gestione_annunci_temp.html';
	my $error_message_aux;
	foreach my $i (@errors)
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

	my $codice=$values{"oldcodice"};
	my $annuncio_node=$doc->findnodes("Annunci/Annuncio[Codice='$codice']");
	
	my $titolo=$values{"titolo"};
	my $fcontenuto=$values{"testo"};

	my $vcontenuto='<textarea class="gestione_annunci-textarea" rows="9" cols="40" name="testo">'."$fcontenuto".'</textarea>';
	my $vt_form='<input class= "input" title="Inserisci titolo" type="text" name="titolo" value="'."$titolo".'"/>';
	my $hiddencodice='<input class= "input" title="Codice nascosto" type="hidden" name="oldcodice" value="'."$codice".'"/>';

	my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'error' => $error_message,
		'pagina' => "edit",
		'vtitolo'=>$vt_form,
		'vcontenuto'=>$vcontenuto,
		'oldcodice'=>$hiddencodice,
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

	my $codice=$values{"oldcodice"};
	my $vecchio_codice=$doc->findnodes("Annunci/Annuncio[Codice='$codice']/Titolo/text()");
	my $annuncio_node=$doc->findnodes("Annunci/Annuncio[Codice='$codice']");
	my $old_testo=$doc->findnodes("Annunci/Annuncio[Codice='$codice']/Testo/text()");
	my $old_immagine=$doc->findnodes("Annunci/Annuncio[Codice='$codice']/Immagine");
	$annuncio_node->[0]->parentNode->removeChild($annuncio_node->[0]);
	
		
		my $annuncio_tag=$doc->createElement("Annuncio");	
		$root->appendChild($annuncio_tag);

		my $titolo_tag=$doc->createElement("Titolo");
		$titolo_tag->appendTextNode($values{'titolo'});
		$annuncio_tag->appendChild($titolo_tag);
	
		my $last_codice=$doc->findvalue("Annunci/Annuncio[last()]/Codice");
		my $codice_annuncio=$last_codice+1;
		
		my $codice_tag=$doc->createElement("Codice");
		$codice_tag->appendTextNode($codice_annuncio);
		$annuncio_tag->appendChild($codice_tag);
		
		
		
	
	
	
		my ($sec,$min,$hour,$mday,$mon,$yr19,$wday,$yday,$isdst) = localtime(time);
		my $year=$yr19+1900;
		my $regex=$mon=~ /^[0-9]$/;
		if($regex)
		{
			$mon="0".$mon;
		}
		my $date="$year-$mon-$mday";

		$regex=$mday=~ /^[0-9]$/;
		if($regex)
		{
			$mday="0".$mday;
		}
		my $date="$year-$mon-$mday";
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
			my $upload_directory="../public_html/images/annunci";
			$immagine="$upload_directory/$old_immagine";
		}
		$immagine_tag->appendTextNode($immagine);
		$annuncio_tag->appendChild($immagine_tag);
	
		open (XML,">","../data/Annunci.xml");
		print XML $doc->toString();
		close(XML);
		print $cgi->redirect("check_session.cgi?modifica_annunci");
	
}

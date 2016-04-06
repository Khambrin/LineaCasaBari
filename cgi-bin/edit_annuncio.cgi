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
	my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'error' => $error_message,
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

	my $vecchiotitolo=$values{"oldtitolo"};
	my $annuncio_node=$doc->findnodes("Annunci/Annuncio[Titolo='$vecchiotitolo']");
	my $old_immagine=$doc->findnodes("Annunci/Annuncio[Titolo='$vecchiotitolo']/Immagine");
	$annuncio_node->[0]->parentNode->removeChild($annuncio_node->[0]);

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
			my $upload_directory="../public_html/images/annunci";
			$immagine="$upload_directory/$old_immagine";
		}
		$immagine_tag->appendTextNode($immagine);
		$annuncio_tag->appendChild($immagine_tag);

		open (XML,">","../data/Annunci.xml");
		print XML $doc->toString();
		close(XML);
		print $cgi->redirect("modifica_annunci.cgi");

}

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
my $messaggio_error="false";
my %values;

my $doc,my $root;

my $parser=XML::LibXML->new();
$doc=$parser->parse_file("../data/Prodotti.xml");
$root=$doc->documentElement();

my $nome_value="";
my $descrizione_value="";
my $prezzo_value="";
my $data_value="";
my $tag1_value="";
my $tag2_value="";
my $tag3_value="";
my $tag4_value="";
foreach my $p (param())
{
	$values{$p}=lc param($p);
}

if ($values{"Nome"})
{
	$nome_value=$values{"Nome"};
}
if ($values{"Descrizione"})
{
	$descrizione_value=$values{"Descrizione"};
}
if ($values{"Prezzo"})
{
	$prezzo_value=$values{"Prezzo"};
	my $regex=$values{"Prezzo"}=~ /^[0-9]+(\,[0-9]{2})?$/;
	if(!$regex)
	{
		$messaggio_error="Inserisci un prezzo valido";
		$prezzo_value="";
	}
}
if ($values{"Data"})
{
	$data_value=$values{"Data"};
}
if ($values{"Tag1"})
{
	$tag1_value=$values{"Tag1"};
}
if ($values{"Tag2"})
{
	$tag2_value=$values{"Tag2"};
}
if ($values{"Tag3"})
{
	$tag3_value=$values{"Tag3"};
}
if ($values{"Tag4"})
{
	$tag4_value=$values{"Tag4"};
}
if($messaggio_error eq "false")
{
	
	my $old_prodotto=$values{"old_cod"};
	my $prodotto_node=$doc->findnodes("Prodotti/Prodotto[Codice='$old_prodotto']");
	$prodotto_node->[0]->parentNode->removeChild($prodotto_node->[0]);
	my $prodotto_tag=$doc->createElement("Prodotto");	
	$root->appendChild($prodotto_tag);
	my $codice_tag=$doc->createElement("Codice");
	$codice_tag->appendTextNode($old_prodotto);
	$prodotto_tag->appendChild($codice_tag);
	my $nome_tag=$doc->createElement("Nome");
	$nome_tag->appendTextNode($values{'Nome'});
	$prodotto_tag->appendChild($nome_tag);
	my $descrizione_tag=$doc->createElement("Descrizione");
	$descrizione_tag->appendTextNode($values{'Descrizione'});
	$prodotto_tag->appendChild($descrizione_tag);
	my $categoria_tag=$doc->createElement("Categoria");
	$categoria_tag->appendTextNode($values{'Categoria'});
	$prodotto_tag->appendChild($categoria_tag);
	my $prezzo_tag=$doc->createElement("Prezzo");
	$prezzo_tag->appendTextNode($values{'Prezzo'});
	$prodotto_tag->appendChild($prezzo_tag);
	my $data_tag=$doc->createElement("Data_aggiunta");
	$data_tag->appendTextNode($values{'Data'});
	$prodotto_tag->appendChild($data_tag);
	my $immagine_tag=$doc->createElement("Immagine");
	my $immagine;
	my $upload_directory="../public_html/images/prodotti";
	my $read_directory="../images/prodotti";
	if ($values{'Immagine'})
	{
		my $upload_filehandle=$cgi->upload("Immagine");
		open (UPLOADFILE,">$upload_directory/$values{'Immagine'}") or die "$!";
		binmode UPLOADFILE;
		while (<$upload_filehandle>)
		{
			print UPLOADFILE;
		}
		close UPLOADFILE;
		$immagine="$read_directory/$values{'Immagine'}";
	}
	else
	{
		$immagine="$upload_directory/$values{'old_image'}";
	}
	$immagine_tag->appendTextNode($immagine);
	$prodotto_tag->appendChild($immagine_tag);
	my $tag_tag=$doc->createElement("Tag");
	$tag_tag->appendTextNode($values{'Tag1'});
	$prodotto_tag->appendChild($tag_tag);
	my $tag_tag=$doc->createElement("Tag");
	$tag_tag->appendTextNode($values{'Tag2'});
	$prodotto_tag->appendChild($tag_tag);
	my $tag_tag=$doc->createElement("Tag");
	$tag_tag->appendTextNode($values{'Tag3'});
	$prodotto_tag->appendChild($tag_tag);
	my $tag_tag=$doc->createElement("Tag");
	$tag_tag->appendTextNode($values{'Tag4'});
	$prodotto_tag->appendChild($tag_tag);



	open (XML,">","../data/Prodotti.xml");
	print XML $doc->toString();
	close(XML);
	print $cgi->redirect("ricerca_prodotto.cgi?modified");
}
else
{
	my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
	my $cod=param("old_cod");
	if($nome_value eq "")
	{
		$nome_value=$doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Nome/text()");
	}
	if($descrizione_value eq"")
	{
		$descrizione_value=$doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Descrizione/text()");
	}
	my $categoria_value=$doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Categoria/text()");
	$prezzo_value=$doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Prezzo/text()");
	if($data_value eq "")
	{
		$data_value=$doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Data_aggiunta/text()");
	}
	my $valutazione_value=$doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Valutazione/text()");
	my $immagine_value=$doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Immagine/text()");
	if($tag1_value eq "")
	{
		$tag1_value=$doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Tag[1]/text()");
	}
	if($tag2_value eq "")
	{
		$tag2_value=$doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Tag[2]/text()");
	}
	if($tag3_value eq "")
	{
		$tag3_value=$doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Tag[3]/text()");
	}
	if($tag4_value eq"")
	{
		$tag4_value=$doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Tag[4]/text()");
	}
	
	my $tot='<form action="edit_prodotto.cgi" method="post" enctype="multipart/form-data">';
	my $i=0;
	
	my$x='<li><label>Nome:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name="Nome" type="text" value='."$nome_value".' /></div><div class="inputRight"></div></li>';
	$tot=$tot.$x;
	$i++;
	
	$x='<li><label>Descrizione:</label><textarea rows="50" cols="50" name="Descrizione">'."$descrizione_value".'</textarea></li>';
	$i++;
	$tot=$tot.$x;
	
	my @splitstring= (split (/_/, basename($categoria_value)));
	$x='<li><label>La categoria &egrave '."@splitstring".' scegli la nuova:</label><select name="Categoria"><option value="lista_nozze">Lista nozze</option><option value="porcellane">Porcellane</option><option value="paralumi">Paralumi</option><option value="pentole">Pentole</option><option value="per_la_tavola">Per la tavola</option><option value="tovaglie">Tovaglie</option></select></li>';
	$tot=$tot.$x;
	$i++;
	
	$x='<li><label>Prezzo:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name="Prezzo" type="text" value='."$prezzo_value".' /></div><div class="inputRight"></div>&#8364;</li>';
	$tot=$tot.$x;
	$i++;
	
	$x='<li><label>Data aggiunta:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name="Data" type="text" value='."$data_value".' /></div><div class="inputRight"></div></li>';
	$tot=$tot.$x;
	$i++;	
	
	my $filespec="$immagine_value";
	my $path= dirname $filespec;
	my $filename=basename $filespec;
	my $read_directory="../images/prodotti";
	my $immagine="$read_directory/$filename";
	$x='<li><label>Inserisci una nuova immagine:</label><img src='."$immagine".' alt="foto prodotto" height="100" width="100"><input type="file" name="Immagine"></li>';
	$tot=$tot.$x;
	$i++;
		
	$x='<li><label>Tag:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name="Tag1" type="text" value='."$tag1_value".' /></div><div class="inputRight"></div></li>';
	$i++;
	$tot=$tot.$x;
	
	$x='<li><label>Tag:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name="Tag2" type="text" value='."$tag2_value".' /></div><div class="inputRight"></div></li>';
	$i++;
	$tot=$tot.$x;
	
	$x='<li><label>Tag:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name="Tag3" type="text" value='."$tag3_value".' /></div><div class="inputRight"></div></li>';
	$i++;
	$tot=$tot.$x;
	
	$x='<li><label>Tag:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name="Tag4" type="text" value='."$tag4_value".' /></div><div class="inputRight"></div></li>';
	$i++;
	$tot=$tot.$x;
	
	$x='<li><div><button class="button" type="submit">Modifica</button><input type="hidden" name="old_cod" value="'."$cod".'"/><input type="hidden" name="old_image" value="'."$filename".'"/></form><form action="togli_prodotto.cgi" method="post"><input type="hidden" name="prodotto" value="'."$cod".'" /><button class="button" type="submit">togli prodotto</button></form></div></li>';
	$i++;
	$tot=$tot.$x;
	
	my $lista_prodotto='<div class="form-container2"><ul class="form-Block">'."$tot".'</ul></div>';
	my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'list' => "true",
		'lista_prodotti' => $lista_prodotto,
		'messaggio_error' => $messaggio_error,
		'pagina' => "rimuovi_modifica",
	};
	print $cgi->header('text/html');
	my $file='gestione_prodotti_temp.html';
	$template->process($file,$vars) || die $template->error();
}
	


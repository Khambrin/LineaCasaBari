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
print $cgi->header('text/html');
my $session = CGI::Session->load();
my $email=$session->param("email");

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Prodotti.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});
my $cod;
if ($ENV{'REQUEST_METHOD'} eq 'POST')
{
	$cod=param("codice");
	
}
else
{
	$cod=$ENV{'QUERY_STRING'};
}
my $messaggio="false";
my @cod_prodotti=$doc->findnodes("Prodotti/Prodotto/Codice/text()");

if($ENV{'QUERY_STRING'}eq "modified")
{
	$messaggio="modifica effettuata con successo";
}
elsif($ENV{'QUERY_STRING'}eq "deleted")
{
	$messaggio="eliminazione effettuata con successo";
}
else
{
	if(@cod_prodotti)
	{
		if($cod>=0)
		{
			my $i;
			foreach $i (@cod_prodotti)
			{
				if($i ne $cod)
				{
					$messaggio="il codice inserito non corrisponde a nessun prodotto esistente";
				}
				else
				{
					$messaggio="false";
					last;
				}
			}
		}
		else
		{
			$messaggio="inserisci un codice per la ricerca";
		}
	}
	else
	{
		$messaggio="non ci sono prodotti";
	}
}
my $vars;

if($messaggio eq "false")
{
	push my @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Codice/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Nome/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Descrizione/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Categoria/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Prezzo/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Data_aggiunta/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Valutazione/text()");
	push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Immagine/text()");
	my $num_tag=$doc->findvalue("count(Prodotti/Prodotto[Codice='$cod']/Tag)");
	for(my $x=1; $x<=$num_tag;$x++)
	{
		push @prodotto, $doc->findnodes("Prodotti/Prodotto[Codice='$cod']/Tag[$x]/text()");
	}
	
	
	my $tot='<form action="edit_prodotto.cgi" method="post" enctype="multipart/form-data">';
	my $i=0;
	
	my $x='<li><div id="prodotto-cod"><label id="prodotto-codiceLabel">Codice:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name="Codice" type="text" value='."@prodotto[$i]".' /></div><div class="inputRight"></div></div></li>';
	$tot=$tot.$x;
	$i++;
	
	$x='<li><label id="prodotto-nomeLabel">Nome:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name="Nome" type="text" value='."@prodotto[$i]".' /></div><div class="inputRight"></div></li>';
	$tot=$tot.$x;
	$i++;
	
	$x='<li><label id="prodotto-descrizioneLabel">Descrizione:</label><textarea id="gestione_prodotti-textarea rows="50" cols="50" name="Descrizione">'."@prodotto[$i]".' </textarea></li>';
	$i++;
	$tot=$tot.$x;
	
	my @splitstring= (split (/_/, basename(@prodotto[$i])));
	$x='<li"><div id="prodotto-cat"><label id="prodotto-categoriaricLabel">La categoria &egrave '."@splitstring".' scegli la nuova:</label><select name="Categoria"><option value="lista_nozze">Lista nozze</option><option value="porcellane">Porcellane</option><option value="paralumi">Paralumi</option><option value="pentole">Pentole</option><option value="per_la_tavola">Per la tavola</option><option value="tovaglie">Tovaglie</option></select></div></li>';
	$tot=$tot.$x;
	$i++;
	
	$x='<li><label id="prodotto-prezzoLabel">Prezzo:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name="Prezzo" type="text" value='."@prodotto[$i]".' /></div><div class="inputRight"></div></li>';
	$tot=$tot.$x;
	$i++;
	
	$x='<li><label id="prodotto-dataLabel">Data aggiunta:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name="Data" type="text" value='."@prodotto[$i]".' /></div><div class="inputRight"></div></li>';
	$tot=$tot.$x;
	$i++;	
	
	my $filespec="@prodotto[$i]";
	my $path= dirname $filespec;
	my $filename=basename $filespec;
	my $read_directory="../images/prodotti";
	my $immagine="$read_directory/$filename";
	$x='<li><label id="prodotto-immagineLabel">Inserisci una nuova immagine:</label><img src='."$immagine".' alt="foto prodotto" height="100" width="100"><input type="file" name="Immagine"></li>';
	$tot=$tot.$x;
	$i++;
		
	$x='<li><label class="prodotto-tagLabel">Tag:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name="Tag1" type="text" value='."@prodotto[$i]".' /></div><div class="inputRight"></div></li>';
	$i++;
	$tot=$tot.$x;
	
	$x='<li><label class="prodotto-tagLabel">Tag:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name="Tag2" type="text" value='."@prodotto[$i]".' /></div><div class="inputRight"></div></li>';
	$i++;
	$tot=$tot.$x;
	
	$x='<li><label class="prodotto-tagLabel">Tag:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name="Tag3" type="text" value='."@prodotto[$i]".' /></div><div class="inputRight"></div></li>';
	$i++;
	$tot=$tot.$x;
	
	$x='<li><label class="prodotto-tagLabel">Tag:</label><div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" name="Tag4" type="text" value='."@prodotto[$i]".' /></div><div class="inputRight"></div></li>';
	$i++;
	$tot=$tot.$x;
	
	
	$tot=$tot.'<li><div><button class="button" type="submit">Modifica</button><input type="hidden" name="old_cod" value="'."$cod".'"/><input type="hidden" name="old_image" value="'."$filename".'"/></form><form action="togli_prodotto.cgi" method="post"><input type="hidden" name="prodotto" value="'."$cod".'" /><button class="button" type="submit">togli prodotto</button></form></div></li>';
	my $lista_prodotto='<div id="form-containerprodotto"><ul class="gestione-aggiungi_form">'."$tot"."</ul></div>";
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'list' => "true",
		'lista_prodotti' => $lista_prodotto,
		'pagina' => "rimuovi_modifica",
	};
}
else
{
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'list' => "false",
		'messaggio' => $messaggio,
		'pagina' => "rimuovi_modifica",
		
		
	};
}
my $file='gestione_prodotti_temp.html';
$template->process($file,$vars) || die $template->error();

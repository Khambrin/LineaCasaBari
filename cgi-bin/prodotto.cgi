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

my $amministratore=$session->param("amministratore");
my $mex=$cgi->param("messaggio_newsletter");
my $ias=$cgi->param("iscrizione_avvenuta");

my $vars;

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Prodotti.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my %in;

if (length ($ENV{'QUERY_STRING'}) > 0){
      my $buffer = $ENV{'QUERY_STRING'};
      my @pairs = split(/&/, $buffer);
	  my $name;
	  my $value;
      foreach my $pair (@pairs){
            ($name, $value) = split(/=/, $pair);
            $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
			$in{$name} = $value; 
      }
 }
 
my $file='prodotto_temp.html';
my $Codice=$in{'Codice'};

my $prodotto_codice=$doc->findnodes("Prodotti/Prodotto[Codice='$Codice']/Codice/text()");
my $prodotto_nome=$doc->findnodes("Prodotti/Prodotto[Codice='$Codice']/Nome/text()");
my $prodotto_descrizione=$doc->findnodes("Prodotti/Prodotto[Codice='$Codice']/Descrizione/text()");
my $prodotto_categoria=$doc->findnodes("Prodotti/Prodotto[Codice='$Codice']/Categoria/text()");
my $prodotto_prezzo=$doc->findnodes("Prodotti/Prodotto[Codice='$Codice']/Prezzo/text()");
my $prodotto_data_aggiunta=$doc->findnodes("Prodotti/Prodotto[Codice='$Codice']/Data_aggiunta/text()");
my $prodotto_valutazione=$doc->findnodes("Prodotti/Prodotto[Codice='$Codice']/Valutazione/text()");
my $prodotto_immagine=$doc->findnodes("Prodotti/Prodotto[Codice='$Codice']/Immagine/text()");
my @recensione_email=$doc->findnodes("Prodotti/Prodotto[Codice='$Codice']/Recensione/Email/text()");
my @recensione_titolo=$doc->findnodes("Prodotti/Prodotto[Codice='$Codice']/Recensione/Titolo/text()");
my @recensione_nome=$doc->findnodes("Prodotti/Prodotto[Codice='$Codice']/Recensione/Nome/text()");
my @recensione_data=$doc->findnodes("Prodotti/Prodotto[Codice='$Codice']/Recensione/Data_pubblicazione/text()");
my @recensione_testo=$doc->findnodes("Prodotti/Prodotto[Codice='$Codice']/Recensione/Testo/text()");
my @recensione_votop=$doc->findnodes("Prodotti/Prodotto[Codice='$Codice']/Recensione/Voto/text()");
my @recensione_votor=$doc->findnodes("Prodotti/Prodotto[Codice='$Codice']/Recensione/Voto_recensione/text()");

my $alt= substr $prodotto_immagine, 19, -4;
my $stampa_immagine='<img src="'."$prodotto_immagine".'" alt="'."$alt".'"/>';


#gestione filtri ritorno alla ricerca
my $filter;
if ($in{'Filter'}) {
	$filter=$in{'Filter'};
	}
else {
	$filter='Tutte';
}

my $page;
if ($in{'Page'}) {
	$page=$in{'Page'};
	}
else {
	$page=0;
}

my $x='<a href="prodotti.cgi?Page='."$page".'&Filter='."$filter".'"> Torna ai risultati della ricerca per "'."$filter".'" </a>';
my $Pagina_precedente="$x";



#gestione form della recensione

my $tot;
my $already_reviewed;
if ((!$email) || grep(/^$email/, @recensione_email)) {
	$already_reviewed = 1;
} else {
	$already_reviewed = 0;
}

#my $hidden='<input type="hidden" name="" value="'."$ENV{'QUERY_STRING'}".'"/>';

my $recensione_form;
if(!$already_reviewed) {
	my $x='<form method="post" action="aggiungi_recensione_form.cgi?Codice='."$prodotto_codice".'&Page='."$page".'&Filter='."$filter".'" enctype="multipart/form-data">
			<ul class="aggiungi_recensione_form">
				<li class="gestione-block">
                    <label id="recensioneTitolo-label">Titolo:</label>
                    <div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" type="text" name="titolo"/></div><div class="inputRight"></div>
                </li>';
	my $tot=$tot.$x;
	if ($in{'Errtitle'}) {
		my $x='<li class="error"> Devi completare il campo titolo </li>';
		$tot=$tot.$x;
	}
	my $x='<li class="gestione-block">
                <label id="recensioneNome-label">Nome visualizzato:</label>
                <div class="inputLeft"></div><div class="gestione-inputMiddle"><input class="input" type="text" name="nome"/></div><div class="inputRight"></div>
            </li>';
	my $tot=$tot.$x;
	if ($in{'Errname'}) {
		my $x='<li class="error"> Devi completare il campo nome </li>';
		$tot=$tot.$x;
	}
	my $x='<li class="gestione-block">
                    <label id="recensioneTesto-label">Testo:</label>
                </li>
                <li class="gestione-block">
                    <textarea class="gestione_textarea" name="testo"></textarea>
                </li>';
	my $tot=$tot.$x;
	if ($in{'Errtext'}) {
		my $x='<li class="error"> Devi completare il campo testo	</li>';
		$tot=$tot.$x;
	}
	my $x='<li><label id="recensioneVoto-label"> Voto prodotto: <span>
				<select name="voto">
					<option value="1"> 1 </option>
					<option value="2"> 2 </option>
					<option value="3"> 3 </option>
					<option value="4"> 4 </option>
					<option value="5"> 5 </option>
				</select></span></label>
			</li>';
	my $tot=$tot.$x;
	if ($in{'Errvote'}) {
		my $x='<li class="error"> Devi selezionare un voto </li>';
		$tot=$tot.$x;
	}
	my $x='</ul>
            <div class="gestione-button_block">
                <button type="submit">Aggiungi recensione</button>
            </div>
           </form>';
	$tot=$tot.$x;
	$recensione_form="$tot";
}

#gestione numero commenti
my $Num_commenti;

if ($in{'Numcomm'}) {
	$Num_commenti=$in{'Numcomm'};
	}
else {
	$Num_commenti=3;
}

if($Num_commenti > $#recensione_titolo) {
	$Num_commenti=$#recensione_titolo;
}


for (my $index=0; $index <= $Num_commenti; $index++)
{
	my $x='<div class="recensione-prodotto"><ul><li><h2 id="Titolo_recensione">'."@recensione_titolo[$index]";
	$tot=$tot.$x;
	my $x='<span>'."@recensione_data[$index]".'</span>';
	$tot=$tot.$x;
	my $x='<span>'."@recensione_votor[$index]".'</span></h2></li>';
	$tot=$tot.$x;
	my $x='<li><h3 id="Nome_utente">'."@recensione_nome[$index]".'</h3></li>';
	$tot=$tot.$x;
	my $x='<li><p>'."@recensione_testo[$index]".'</p></li>';
	$tot=$tot.$x;
	if($email!=@recensione_email[$index]) {
		my $x='<li>
				<form action="vota_recensione" class="vota_recesione" method="post">
				<p> Voto: <span>
				<select name="voto">
					<option value="1"> 1 </option>
					<option value="1"> 2 </option>
					<option value="1"> 3 </option>
					<option value="1"> 4 </option>
					<option value="1"> 5 </option>
				</select></span></p>
				<p><input type="submit" value="Vota recensione"/></p>
				</form>
				</li>';
		$tot=$tot.$x;
	}
	if($amministratore | $email eq @recensione_email[$index]) {
		my $x='<li><form action="elimina_recensione" class="elimina_recensione" method="post">
				<p><input type="submit" value="Elimina recensione"/></p></form></li>';
		$tot=$tot.$x;
	}
	my $x='</ul></div>';
	my $tot=$tot.$x;
}	

my $stampa_recensioni="$tot";


if ($session->is_empty)
{
	$vars={
		'sessione' => "false",
		'messaggio_newsletter'=>$mex,
		'iscrizione_avvenuta'=>$ias,
		'prodotto_nome' =>$prodotto_nome,
		'prodotto_descrizione' =>$prodotto_descrizione,
		'prodotto_prezzo' =>$prodotto_prezzo,
		'prodotto_categoria' =>$prodotto_categoria,
		'prodotto_data' =>$prodotto_data_aggiunta,
		'prodotto_valutazione' =>$prodotto_valutazione,
		'prodotto_recensioni' =>$stampa_recensioni,
		'prodotto_immagine' =>$stampa_immagine,
		'recensione_form' =>$recensione_form,
		'pagina_precedente' =>$Pagina_precedente,
	};
}

else
{
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => $amministratore,
		'messaggio_newsletter'=>$mex,
		'iscrizione_avvenuta'=>$ias,
		'prodotto_nome' =>$prodotto_nome,
		'prodotto_descrizione' =>$prodotto_descrizione,
		'prodotto_prezzo' =>$prodotto_prezzo,
		'prodotto_categoria' =>$prodotto_categoria,
		'prodotto_data' =>$prodotto_data_aggiunta,
		'prodotto_valutazione' =>$prodotto_valutazione,
		'prodotto_recensioni' =>$stampa_recensioni,
		'prodotto_immagine' =>$stampa_immagine,
		'recensione_form' =>$recensione_form,
		'pagina_precedente' =>$Pagina_precedente,		
	};
}
print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

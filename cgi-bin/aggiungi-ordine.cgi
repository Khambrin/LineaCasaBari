#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use XML::LibXML;

use Switch;
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
		});
my $cgi=new CGI;

my $session = CGI::Session->load();
my $email=$session->param("email");
my $mpagamento=param('mpagamento');
my $indirizzo=param("indirizzo");
my $codice=0;
$codice=param('codice');
my $messaggio_errore='false';

if(($mpagamento eq 'carta_credito' or $mpagamento eq 'pay_pal' or $mpagamento eq 'carta_prepagata') and (!$codice ))#uso lo stesso cod di stampa_resoconto 
{		
		$messaggio_errore='Inserisci il codice della carta';
		my $amministratore=$session->param("amministratore");
		print $cgi->header('text/html');
		my $parser=XML::LibXML->new;
		my $carrello_doc=$parser->parse_file("../data/Carrelli.xml");
		my $parser2=XML::LibXML->new;
		my $prodotto_doc=$parser2->parse_file("../data/Prodotti.xml");
		my $template=Template->new({
			INCLUDE_PATH => '../public_html/temp',
		});
		my $num_prodotti=$carrello_doc->findvalue("count(Carrelli/Carrello[Utente='$email']/Elemento)");
		my $tot_prodotto=0;
		my $tot;
		for(my $i=1; $i<=$num_prodotti; $i++)
		{
			my @cod=$carrello_doc->findnodes("Carrelli/Carrello[Utente='$email']/Elemento[$i]/Prodotto/text()");
			my $codice=@cod[0]->string_value;
			my $x='<li><input type="hidden" name="prodotto'."$i".'" value="'."$codice".'"/></li>';
			$tot=$tot.$x;
			my @prz=$prodotto_doc->findnodes("Prodotti/Prodotto[Codice='$codice']/Prezzo/text()");
			my $prezzo=@prz[0]->string_value;
			$tot_prodotto=$tot_prodotto+$prezzo;
		}

		my $x='<li><h2>Resoconto</h2></li>';
		$tot=$tot.$x;

		my $x='<li class="resocontoLi"><p>Prezzo totale: '."$tot_prodotto ".'&#8364;</p></li>';
		$tot=$tot.$x;


		my $x='<li class="resocontoLi"><p>Hai scelto l&#180;indirizzo numero: '."$indirizzo".'</p></li>';
		$tot=$tot.$x;

		my $x='<li class="resocontoLi"><p>Metodo scelto: ';
		$tot=$tot.$x;

		if($mpagamento eq 'carta_credito')
		{
			my $x='Carta di credito</p></li>';
			$tot=$tot.$x;
			my $x='<li><label>Inserire codice: </label><div class="inputLeft"></div><div class="inputMiddle"><input class="input" type="text" name="codice"/></div><div class="inputRight"></div></li>';
			$tot=$tot.$x;
		}
		elsif($mpagamento eq 'bonifico')
		{
			my $x='Bonifico</p></li>';
			$tot=$tot.$x;
			my $x='<li><p>Le nostre coordinate bancarie sono: IT	11	X	03268	10001	100000000000</p></li>';
			$tot=$tot.$x;
		}
		elsif($mpagamento eq 'contrassegno')
		{
			my $x='Contrassegno</p></li>';
			$tot=$tot.$x;
			my $x='<li><p>Le invieremo una mail con data e ora di arrivo previsto della merce</p></li>';
			$tot=$tot.$x;
		}
		elsif($mpagamento eq 'pay_pal')
		{
			my $x='Pay pal</p></li>';
			$tot=$tot.$x;
			my $x='<li><label>Inserire codice: </label><div class="inputLeft"></div><div class="inputMiddle"><input class="input" type="text" name="codice"/></div><div class="inputRight"></div></li>';
			$tot=$tot.$x;
		}
		elsif($mpagamento eq 'carta_prepagata')
		{
			my $x='Carta prepagata</p></li>';
			$tot=$tot.$x;
			my $x='<li><label>Inserire codice: </label><div class="inputLeft"></div><div class="inputMiddle"><input class="input" type="text" name="codice"/></div><div class="inputRight"></div></li>';
			$tot=$tot.$x;
		}
		my $x='<li><button class="button" type="submit" value="conferma">Conferma</button></li>';
		$tot=$tot.$x;
		my $x='<li><input type="hidden" name="mpagamento" value="'."$mpagamento".'"/><input type="hidden" name="indirizzo" value="'."$indirizzo".'"/></li>';
		$tot=$tot.$x;

		my $lista_acquisto='<div class="form-container2"><form action="aggiungi-ordine.cgi" method="post"><ul>'."$tot".'</ul></form></div>';
		my $vars={
			'sessione' => "true",
			'email' => $email,
			'lista_acquisto' => $lista_acquisto,
			'amministratore'=>$amministratore,
			'messaggio_errore' => $messaggio_errore,
		};

		my $file='resoconto_temp.html';
		$template->process($file,$vars) || die $template->error();
	
	
}
else
{
	if($mpagamento eq 'carta_credito')
	{
		$mpagamento='carta di credito';
	}
	elsif($mpagamento eq 'pay_pal')
	{
		$mpagamento='PayPal';
	}
	elsif($mpagamento eq 'carta_prepagata')
	{
		$mpagamento='Carta prepagata';
	}


	my $parser=XML::LibXML->new;
	my $doc=$parser->parse_file("../data/Carrelli.xml");
	my $num_prodotti=$doc->findvalue("count(Carrelli/Carrello[Utente='$email']/Elemento)");
	my $parser2=XML::LibXML->new();
	my $doc2=$parser->parse_file("../data/Carrelli.xml");
	
	my $doc;
	my $root;
	my $id=1;
	if (-e "../data/Ordini.xml")
	{
		my $parser=XML::LibXML->new();
		$doc=$parser->parse_file("../data/Ordini.xml");
		$root=$doc->documentElement();
		my $last_id=$doc->findvalue("Ordini/Ordine[last()]/Codice");
		$id=$last_id+1;
	}
	else
	{
		$doc=XML::LibXML::Document->new("1.0","UTF-8");
		$root=$doc->createElement("Ordini");
		$doc->setDocumentElement($root);	
	}

	my $ordine_tag=$doc->createElement("Ordine");	
	$root->appendChild($ordine_tag);

	my $id_tag=$doc->createElement("Codice");
	$ordine_tag->appendChild($id_tag);
	$id_tag->appendTextNode($id);

	my $utente_tag=$doc->createElement("Utente");
	$ordine_tag->appendChild($utente_tag);
	$utente_tag->appendTextNode($email);

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
	$ordine_tag->appendChild($date_tag);
	$date_tag->appendTextNode($date);
		
	my $pagamento_tag=$doc->createElement("Mpagamento");
	$ordine_tag->appendChild($pagamento_tag);
	$pagamento_tag->appendTextNode($mpagamento);
		
	my $indirizzo_tag=$doc->createElement("Indirizzo");
	$ordine_tag->appendChild($indirizzo_tag);
	$indirizzo_tag->appendTextNode($indirizzo);
	
	for(my $i=1;$i<=$num_prodotti;$i++)	
	{
		my $cod=param('prodotto'."$i".'');
		my $prodotto_tag=$doc->createElement("Prodotto");
		$ordine_tag->appendChild($prodotto_tag);
		$prodotto_tag->appendTextNode($cod);
		
		my @quantita=$doc2->findnodes("Carrelli/Carrello[Utente='$email']/Elemento[$i]/Quantita/text()");
		my $quantita_tag=$doc->createElement("Quantita");
		$ordine_tag->appendChild($quantita_tag);
		$quantita_tag->appendTextNode(@quantita[0]);
		
	}

	open (XML,">","../data/Ordini.xml");
	print XML $doc->toString();
	close(XML);

	
	my @carrello = $doc2->findnodes("Carrelli/Carrello[Utente='$email']");
	@carrello[0]->parentNode->removeChild(@carrello[0]);

	open (XML,">","../data/Carrelli.xml");
	print XML $doc2->toString();
	close(XML);
	print $cgi->redirect('check_session.cgi?carrello-svuotato');


}


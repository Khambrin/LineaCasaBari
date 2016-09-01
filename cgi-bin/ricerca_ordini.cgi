#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use XML::LibXML;

my $cgi=new CGI;
print $cgi->header('text/html');
my $session = CGI::Session->load();
my $email=$session->param("email");

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Ordini.xml");
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
my @cod_ordini=$doc->findnodes("Ordini/Ordine/Codice/text()");

if(@cod_ordini)
{
	if($cod)
	{
		my $i;
		foreach $i (@cod_ordini)
		{
			if($i ne $cod)
			{
				$messaggio="il codice inserito non corrisponde a nessun ordine esistente";
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
	$messaggio="non ci sono ordini";
}
my $vars;
if($messaggio eq "false")
{
	push my @ordine, $doc->findnodes("Ordini/Ordine[Codice='$cod']/Codice/text()");
	push @ordine, $doc->findnodes("Ordini/Ordine[Codice='$cod']/Utente/text()");
	push @ordine, $doc->findnodes("Ordini/Ordine[Codice='$cod']/Data/text()");
	push @ordine, $doc->findnodes("Ordini/Ordine[Codice='$cod']/Mpagamento/text()");
	push @ordine, $doc->findnodes("Ordini/Ordine[Codice='$cod']/Indirizzo/text()");
	my $num_prodotto=$doc->findvalue("count(Ordini/Ordine[Codice='$cod']/Prodotto)");
	for(my $x=0; $x<$num_prodotto;$x++)
	{
		push @ordine, $doc->findnodes("Ordini/Ordine[Codice='$cod']/Prodotto/text()");
	}

	my @label = ('Codice','Utente','Data','Metodo di pagamento','Indirizzo' );
	my $y=0;
    my $block1; 
    my $block2;
    my $n_label=scalar @label;
	for(my $i=0; $i<$n_label;$i++)
	{
		my $x='<li class="ordini-block">'.
                '<p class="gestione-labels">'
                ."@label[$i]: @ordine[$y]</p>
            </li>";
		$y++;
		$block1=$block1.$x;
	}
	my $counter=1;
	for(my $i=0; $i<$num_prodotto;$i++)
	{
		my $x='<div class="ordini-block">
                    <label for="prodotto'."$counter".'" class="gestione-labels">'
                    ."Prodotto $counter: @ordine[$y]</label>"
                    .'<input id="prodotto'."$counter".'" type="checkbox" name="'
                    ."$counter"
                    .'" value="on"/>
                </div>';
		$y++;
		$counter++;
		$block2=$block2.$x;
	}

	$y=0;
	$block2=$block2.'<div class="side-element">
                    <button id="prodotto-eliminaSelezionati" class="button" type="submit">Elimina prodotti selezionati</button>
                    <input type="hidden" name="ordine" value="'
                    ."$cod".'"/>
                </div>';
	my $lista_ordine='<div class="form-container2">
                        <ul class="form-Block">'
                            ."$block1
                        </ul>"
                        .'<form class="side-element" action="elimina_prodotti_ordini.cgi" method="post">'
                                ."$block2"
                        .'</form>
                        <form class="side-element" action="togli_ordine.cgi" method="post">
                            <div class="side-element">
                                <input type="hidden" name="ordine" value="'."$cod".'"/>
                                <button class="button" type="submit">Rimuovi ordine</button>
                            </div>
                        </form>
                    </div>';
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'list' => "true",
		'lista_ordini' => $lista_ordine,
	};
}
else
{
	$vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'list' => "false",
		'messaggio_ordini' => $messaggio,
	};
}
my $file='gestione_ordini_temp.html';
$template->process($file,$vars) || die $template->error();

#!/usr/bin/perl -w

use CGI qw(:standard);
use CGI::Cookie;
use CGI::Carp qw(warningsToBrowser fatalsToBrowser);
use strict;
use Template;
use CGI::Session;
use XML::LibXML;

my $cgi=new CGI;
my $session = CGI::Session->load();
if ($session->is_empty) {
	print $cgi->redirect('check_session.cgi?togli_utenti');
}
my $email=$session->param("email");
my $mex=$cgi->param("messaggio_newsletter");
my $ias=$cgi->param("iscrizione_avvenuta");

my $parser=XML::LibXML->new;
my $doc=$parser->parse_file("../data/Utenti.xml");
my $template=Template->new({
		INCLUDE_PATH => '../public_html/temp',
	});

my @users=$doc->findnodes("Utenti/Utente/Email/text()");
my $file='togli_utenti_temp.html';
my $tot;
foreach my $i (@users)
{
	my $x='<li>
            <p>'."$i".'</p>
            <form class="side-element" action="remove_user_form.cgi" method="post">
                <div class="side-element">
                    <button class="button-utente" type="submit">Rimuovi</button>
                    <input type="hidden" name="emailuser" value="'."$i".'"/>
                </div>
            </form>
        </li>';
	$tot=$tot.$x;
}

my $lista_utenti='<div class="generic-container">
            <div class="form-container2">
                <h2>Rimuovi utente</h2>
                <ul class="form-Block" >
                    '."$tot"."
                </ul>
            </div>
        </div>";

my $vars={
		'sessione' => "true",
		'email' => $email,
		'amministratore' => "true",
		'lista_utenti' => $lista_utenti,
		'messaggio_newsletter'=>$mex,
		'iscrizione_avvenuta'=>$ias,
	};
print $cgi->header('text/html');
$template->process($file,$vars) || die $template->error();

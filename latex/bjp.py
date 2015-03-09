#! /usr/bin/python3

import calendar
import sys
import sqlite

argc = len ( sys.argv )
if argc != 2 :
    sys.exit ( 'Usage: bjp.py bjp_id' )

bjp = sys.argv[2]

connection = connect ('bjp.db')
cur = connection.cursor()
infos = cur.execute("select name, contact, address, intervenant, responsable, prestation, projet, nature from client inner join mission on client.bjp_id = mission.bjp_id inner join fournisseur on mission.bjp_id = fournisseur.bjp_id where client.bjp_id= '%s'" %bjp)
[ name, contact, address, intervenant, responsable, prestation, projet, nature ] = infos.fetchone()

with open ( 'latex/cartouche.tex' , 'w' ) as cartouche :

    print ( '\\begin{tabularx}{\\textwidth}{|X|X|}' , file = cartouche )
    print ( '\\hline' , file = cartouche )
    print ( '\\rowcolor[gray]{0.9} \\multicolumn{1}{|c|}{\\titre{CLIENT}} &' , file = cartouche )
    print ( '\\multicolumn{1}{c|}{\\titre{LINAGORA}} \\\\' , file = cartouche )
    print ( '\\hline' , file = cartouche )
    print ( '\\begin{tabular}{ll}' , file = cartouche )
    print ( 'Nom :\t\t&' , name , '\\\\[1ex]' , file = cartouche )

    print ( 'Contact :\t& ' , end = '' , file = cartouche )
    prems = True
    for l in contact.split ( '\n' ) :
        if l != '' :
            if prems :
                print ( l , '\\\\' , end = '' , file = cartouche )
                prems = False
            else :
                print ( '\n\t\t&' , l , '\\\\' , end = '' , file = cartouche )
        else :
            print ( '[1ex]' , file = cartouche )

    print ( 'Adresse :\t& ' , end = '' , file = cartouche )
    prems = True
    for l in address.split ( '\n' ) :
        if l != '' :
            if prems :
                print ( l , '\\\\' , file = cartouche )
                prems = False
            else :
                print ( '\t\t&' , l , '\\\\' , file = cartouche )

    print ( '\\end{tabular}' , file = cartouche )
    print ( '&' , file = cartouche )
    print ( '\\begin{tabular}{ll}' , file = cartouche )
    print ( 'Responsable :\t& ', responsable, '\\\\[1ex]' , file = cartouche )
    print ( 'Intervenant :\t& ', intervenant, file = cartouche )
    print ( '\\end{tabular}' , file = cartouche )
    print ( '\\\\' , file = cartouche )
    print ( '\\hline' , file = cartouche )
    print ( '\\end{tabularx}' , file = cartouche )
    print ( '' , file = cartouche )

    print ( '\\begin{tabularx}{\\textwidth}{|>{\\columncolor[gray]{0.9}}r|X|}' , file = cartouche )
    print ( '\\hline' , file = cartouche )
    print ( 'Intitulé de la prestation\t&' , prestation, '\\\\' , file = cartouche )
    print ( '\\hline' , file = cartouche )
    print ( 'Référence du projet\t\t&'     , projet    , '\\\\' , file = cartouche )
    print ( '\\hline' , file = cartouche )
    print ( 'Nature de la mission\t\t&'    , nature    , '\\\\' , file = cartouche )
    print ( '\\hline' , file = cartouche )
    print ( '\\end{tabularx}' , file = cartouche )
    print ( file = cartouche )

    annee = cur.execute("SELECT annee FROM calendrier WHERE bjp_id = '%s'" % bjp)
    mois = cur.execute("SELECT mois FROM calendrier WHERE bjp_id = '%s'" % bjp)
    nom_mois = ( '' , 'Janvier' , 'Février' , 'Mars' ,
		'Avril' , 'Mai' , 'Juin' ,
		'Juillet' , 'Août' , 'Septembre' ,
		'Octobre' , 'Novembre' , 'Décembre' )

    print ( '\\addsec{' , nom_mois[mois] , ' ' , annee , '}' ,
		sep = '' , file = cartouche )

with open ( 'latex/calendrier.tikz' , 'w' ) as tikz :

    print ( '\\begin{tikzpicture}' , file = tikz )

    calendrier = calendar.Calendar ( )

    nombre_semaines = calendrier.monthdays2calendar ( annee , mois )
    y = len ( nombre_semaines ) - 1

    print ( '\\draw ( 0 , 0 ) grid [ xstep = 2 , ystep = 1 ] ( 14 ,' ,
	y + 1 , ') ;' ,
	file = tikz )

    print ( '\\foreach \\x in { 0 , 1 , ... ,' , y , '}' , file = tikz )
    print ( '{' , file = tikz )
    print ( '\t% samedis' , file = tikz )
    print ( '\t\\filldraw [ fill = black!10 ]' , file = tikz )
    print ( '\t\t( 10 , \\x ) rectangle ( $ ( 12 , 1 ) + ( 0 , \\x ) $ ) ;' , file = tikz )
    print ( '\t% dimanches' , file = tikz )
    print ( '\t\\filldraw [ fill = black!10 ]' , file = tikz )
    print ( '\t\t( 12 , \\x ) rectangle ( $ ( 14 , 1 ) + ( 0 , \\x ) $ ) ;' , file = tikz )
    print ( '}' , file = tikz )

    nom_jour = ( 'lundi' , 'mardi' , 'mercredi' , 'jeudi' ,
		'vendredi' , 'samedi' , 'dimanche' )

    days = cur.execute("SELECT day, period from calendrier WHERE bjp_id= '%s'" %bjp)
    for j in calendrier.itermonthdays2 ( annee , mois ) :

        if j[0] != 0 :	# jour dans le mois

            x = j[1] * 2

            if j[0] in days.fetchall() :
                [day, period] = days.fetchone()
                if period == 'OK' :	# journée entière
                    print ( '\\filldraw [ fill = yellow!100!blue!30 ] (' ,
			x , ',' , y , ') rectangle (' ,
			x + 2 , ',' , y + 1 , ') ;' ,
			file = tikz )
                elif period == 'ma' :	# matin
                    print ( '\\filldraw [ fill = yellow!100!blue!30 ] (' ,
			x , ',' , y , ') -- (' ,
			x , ',' , y + 1 , ') -- (' ,
			x + 2 , ',' , y + 1 , ') -- cycle ;' ,
			file = tikz )
                elif period == 'am' :	# après-midi
                    print ( '\\filldraw [ fill = yellow!100!blue!30 ] (' ,
			x , ',' , y , ') -- (' ,
			x + 2 , ',' , y , ') -- (' ,
			x + 2 , ',' , y + 1 , ') -- cycle ;' ,
			file = tikz )

            print ( '\\node at ( ' , x + 1 , ' , ' , y + 0.8 , ' ) {' ,
		nom_jour[j[1]] , ' ' , j[0] , '} ;' ,
		sep = '' , file = tikz )

        if j[1] == 6 :
            y -= 1

    print ( '\\end{tikzpicture}' , file = tikz )

#! /usr/bin/python3

import calendar
import sys
import yaml

argc = len ( sys.argv )
if argc != 2 :
    sys.exit ( 'Usage: bjp.py fichier.yaml' )

with open ( sys.argv[1] , 'r' ) as f :
    bjp = yaml.load ( f )

with open ( 'cartouche.tex' , 'w' ) as cartouche :

    print ( '\\begin{tabularx}{\\textwidth}{|X|X|}' , file = cartouche )
    print ( '\\hline' , file = cartouche )
    print ( '\\rowcolor[gray]{0.9} \\multicolumn{1}{|c|}{\\titre{CLIENT}} &' , file = cartouche )
    print ( '\\multicolumn{1}{c|}{\\titre{LINAGORA}} \\\\' , file = cartouche )
    print ( '\\hline' , file = cartouche )
    print ( '\\begin{tabular}{ll}' , file = cartouche )
    print ( 'Nom :\t\t&' , bjp['client']['nom']  , '\\\\[1ex]' , file = cartouche )

    print ( 'Contact :\t& ' , end = '' , file = cartouche )
    prems = True
    for l in bjp['client']['contact'].split ( '\n' ) :
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
    for l in bjp['client']['adresse'].split ( '\n' ) :
        if l != '' :
            if prems :
                print ( l , '\\\\' , file = cartouche )
                prems = False
            else :
                print ( '\t\t&' , l , '\\\\' , file = cartouche )

    print ( '\\end{tabular}' , file = cartouche )
    print ( '&' , file = cartouche )
    print ( '\\begin{tabular}{ll}' , file = cartouche )
    print ( 'Responsable :\t& MANAGER \\\\[1ex]' , file = cartouche )
    print ( 'Intervenant :\t& MOI' , file = cartouche )
    print ( '\\end{tabular}' , file = cartouche )
    print ( '\\\\' , file = cartouche )
    print ( '\\hline' , file = cartouche )
    print ( '\\end{tabularx}' , file = cartouche )
    print ( '' , file = cartouche )

    print ( '\\begin{tabularx}{\\textwidth}{|>{\\columncolor[gray]{0.9}}r|X|}' , file = cartouche )
    print ( '\\hline' , file = cartouche )
    print ( 'Intitulé de la prestation\t&' , bjp['mission']['prestation'] , '\\\\' , file = cartouche )
    print ( '\\hline' , file = cartouche )
    print ( 'Référence du projet\t\t&'     , bjp['mission']['projet']     , '\\\\' , file = cartouche )
    print ( '\\hline' , file = cartouche )
    print ( 'Nature de la mission\t\t&'    , bjp['mission']['nature']     , '\\\\' , file = cartouche )
    print ( '\\hline' , file = cartouche )
    print ( '\\end{tabularx}' , file = cartouche )
    print ( file = cartouche )

    annee = bjp['annee']
    mois  = bjp['mois']
    nom_mois = ( '' , 'Janvier' , 'Février' , 'Mars' ,
		'Avril' , 'Mai' , 'Juin' ,
		'Juillet' , 'Août' , 'Septembre' ,
		'Octobre' , 'Novembre' , 'Décembre' )

    print ( '\\addsec{' , nom_mois[mois] , ' ' , annee , '}' ,
		sep = '' , file = cartouche )

with open ( 'calendrier.tikz' , 'w' ) as tikz :

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

    for j in calendrier.itermonthdays2 ( annee , mois ) :

        if j[0] != 0 :	# jour dans le mois

            x = j[1] * 2

            if j[0] in bjp['calendrier'] :
                if bjp['calendrier'][j[0]] == 'OK' :	# journée entière
                    print ( '\\filldraw [ fill = yellow!100!blue!30 ] (' ,
			x , ',' , y , ') rectangle (' ,
			x + 2 , ',' , y + 1 , ') ;' ,
			file = tikz )
                elif bjp['calendrier'][j[0]] == 'ma' :	# matin
                    print ( '\\filldraw [ fill = yellow!100!blue!30 ] (' ,
			x , ',' , y , ') -- (' ,
			x , ',' , y + 1 , ') -- (' ,
			x + 2 , ',' , y + 1 , ') -- cycle ;' ,
			file = tikz )
                elif bjp['calendrier'][j[0]] == 'am' :	# après-midi
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

MOVE 'ALC00003'                TO Z004-COTABC
           MOVE QT47-CORRCO               TO Z004-COIDTC
           IF W-QT47-YCOSRV NOT = SPACE OR Z004-YCOSRV = SPACE
             MOVE '1'                     TO Z004-YCOSRV
           END-IF
           IF Z004-YCOSRV = '1' OR 'A' OR 'D'
      *****SERVICE INDISPONIBLE******
             IF W-QT47-COETBI NOT = QT47-COETBI
             OR W-QT47-COEXSE NOT = QT47-COEXSE
             OR W-QT47-COTYPI NOT = QT47-COTYPI
      *- - - - - - - - - - - - - - - -
      *CHANGEMENT GROUPE UTILISATEUR
      *- - - - - - - - - - - - - - - -
               MOVE ZERO                  TO QT47-COINTE
               MOVE QT47-COETBI           TO W-QT47-COETBI
               MOVE QT47-COEXSE           TO W-QT47-COEXSE
               MOVE QT47-COTYPI           TO W-QT47-COTYPI
             END-IF
      *- - - - - - - - - - - - - - - -.
             MOVE QT47-COINTE             TO Z004-COINTE
             MOVE QT47-COHORO             TO Z004-COHORO
             MOVE QT47-CEACTF             TO Z004-CEACTF
             MOVE QT47-COETBI             TO Z004-COETBI
             MOVE QT47-COEXSE             TO Z004-COEXSE
             MOVE QT47-COTYPI             TO Z004-COTYPI
             MOVE W-QT00-DAVAG1           TO Z004-DAVAG1
             MOVE '0'                     TO IK
             PERFORM F92RC
             IF Z004-YCORET = '0'
               MOVE Z004-ZD600            TO W-QT47-ZD600
               MOVE W-QT47                TO QT47
               MOVE Z004-COIDTC           TO QT47-CORRCO
               MOVE Z004-COINTE           TO QT47-COINTE
               MOVE Z004-COHORO           TO QT47-COHORO
               MOVE Z004-CEACTF           TO QT47-CEACTF
               MOVE Z004-DAVAG1           TO W-QT00-DAVAG1
             ELSE
               MOVE '1'                   TO IK
               MOVE Z004-YCORET           TO W-QT00-YCORET
             END-IF
             IF QTER1-U914
               DISPLAY 'F96QT TABLE ' Z004-COTABC
                       ' ERREUR DE PARAMETRAGE   CODE '
                       'RETOUR : ' Z004-YCORET
             END-IF
           END-IF
           .
      *-----------------------------------------------------------------
      *N96TB. APPEL DU SOUS PROGRAMME
      *-----------------------------------------------------------------
       F96TB.
           MOVE SPACES                    TO S-SPCB-XCORET W-Z900-COSSPG
           MOVE 'ALCU100'                 TO W-Z900-COSSPG
           CALL W-Z900-COSSPG USING SQLCA
                                    S-SPCB
                                    W-9T99-YCOFCT
                                    Z93P
      *SI ABEND DB2
           IF SQLCODE NOT = ZERO AND SQLCODE NOT = 100
             MOVE '1'                     TO FT
      *'E'     CATG
             MOVE W-Z900-COSSPG           TO PROGE
      *F81ES   F80-FN
             PERFORM F98BD THRU F98BD-FN
           END-IF
      *SI ABEND DL1
           IF S-SPCB-XCORET NOT = SPACE
      *F80-ER  F80-FN
             PERFORM F99ER
           END-IF
           .
      *N97.           *************************************.
      *               *FONCTIONS UTILISATEURS             *
      *               *************************************.
      *+------------------------------+
      *I         PLAGE 97             I
      *I   FONCTIONS PRE/POST SQL     I
      *+------------------------------+
      *-----------------------------------------------------------------
      *N97DD. APPEL A MXTU1450 (DATES / HEURE)
      *-----------------------------------------------------------------
       F97DD.
           CALL W-DD00-CODSOUPRO USING W-DD00-ENVU045
           IF W-DD00-YCORET NOT = SPACE
             DISPLAY '******************************'
             DISPLAY '*ERREUR MXTU145               '
             DISPLAY '*CODE RETOUR = ' W-DD00-YCORET
             DISPLAY ' ZONE DE LIEN =' W-DD00-ENVU045
             DISPLAY '******************************'
             MOVE ALL '1'                 TO FT
             GO TO F20-FIN-TRAITEMENT
           END-IF
           .
      *N98.           *************************************.
      *               *FONCTIONS TECHNIQUES ARCHI.        *
      *               *************************************.
      *+------------------------------+
      *I          PLAGE 98            I
      *I   RESERVEE A L'ARCHITECTURE  I
      *+------------------------------+
      *-----------------------------------------------------------------
      *N98BD. TRAITEMENT DES ERREURS DB2
      *-----------------------------------------------------------------
       F98BD.
           EVALUATE SQLCODE
      *-----------------------------------------------------------------
      *N98BF. FIN DE LECTURE
      *-----------------------------------------------------------------
             WHEN 0
               MOVE 0                     TO IK
               GO TO F98BD-FN
             WHEN 100
               MOVE 1                     TO IK
               GO TO F98BD-FN
             WHEN OTHER
               CONTINUE
           END-EVALUATE
           MOVE 2                         TO IK
      *-----------------------------------------------------------------
      *N98BN. DSNTIAR
      *-----------------------------------------------------------------
      *+------------------------------+
      *I      MESSAGE DSNTIAR         I
      *+------------------------------+
           CALL W-CALL-DSNTIAR USING SQLCA
                                     W-MESS
                                     W-MESS-YQSQLS
      *-----------------------------------------------------------------
      *N98BP. EMISSION MESSAGE DSNTIAR
      *-----------------------------------------------------------------
           DISPLAY '--------------------------'
           DISPLAY '* ERREUR GRAVE DB2  PROGRAMME'
                   ' : ' PROGE
                   '  SEGMENT : ' W-9T99-YCSEG
                   '   ETIQUETTE : ' W-9T99-YCFON
           DISPLAY '--------------------------'
      *-----------------------------------------------------------------
      *N98BQ. EMISSION MESSAGE DSNTIAR
      *-----------------------------------------------------------------
           PERFORM VARYING J98BQR FROM 1 BY 1
                     UNTIL 10 < J98BQR
             DISPLAY W-MESS-YLSQLM (J98BQR)
           END-PERFORM
           .
      *-----------------------------------------------------------------
      *N98BX. ROLL  CANCEL
      *-----------------------------------------------------------------
       F98BX.
      *+------------------------------+
      *I  ROLL / ABORT   PROGRAMME    I
      *+------------------------------+.
           CALL W-9T99-COPROG
           .
       F98BD-FN.
           EXIT
           .
      *-----------------------------------------------------------------
      *N99ER. TEST CODE RETOUR  DL1
      *-----------------------------------------------------------------
       F99ER.
           IF S-SPCB-XCORET NOT = SPACE
           AND S-SPCB-XCORET NOT = 'GE'
           AND S-SPCB-XCORET NOT = 'GB'
           AND S-SPCB-XCORET NOT = 'GK'
           AND S-SPCB-XCORET NOT = 'GA'
           AND S-SPCB-XCORET NOT = 'II'
           AND S-SPCB-XCORET NOT = 'GG'
      *-----------------------------------------------------------------
      *N99EU. DISPLAYS  ABEND   DL1
      *-----------------------------------------------------------------
             DISPLAY '*'
             DISPLAY '******************************'
             DISPLAY '*******  ERREUR  DL1  ********'
             DISPLAY '*'
             DISPLAY 'PROGRAMME   : ' PROGR ' ' PROGE
             DISPLAY 'GENERE LE   : ' DATGN
             DISPLAY '*'
             DISPLAY 'FONCTION PAC   : ' S-SPCB-IPAC
             DISPLAY '*'
             DISPLAY 'CODE APPEL DL1 : ' S-SPCB-XFONC
             DISPLAY 'CODE RETOUR   : ' S-SPCB-XCORET
             DISPLAY '*'
             DISPLAY 'INFOS PCB      : ' S-SPCB
             DISPLAY '*'
             DISPLAY '******************************'
             DISPLAY '******************************'
             DISPLAY '*'
             PERFORM F98BX
           END-IF
           .
        COPY  WCISPAC.
       END PROGRAM ALCP519.
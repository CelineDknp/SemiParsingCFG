      *=================================================================
       LINKAGE SECTION.
      *=================================================================
       01 ZY01-YPCBIO.
      *SD: ZY BIB: 9B SEL: 05=01___ FORM: I DESC: 1 NIV: 3 ORG: _ SS: _
         02 ZY00.
       COPY CXTI9B05 REPLACING
             ==01 :PREF:== BY ==03 ZY01==
             ==:PREF:== BY ==ZY01==.
       COPY WCISLCAW.
      ******************************************************************
       PROCEDURE DIVISION USING ZY01-YPCBIO.
      ******************************************************************
      *N0A.           *************************************.
      *               *ARCHITECTURE                       *
      *               *************************************.
       F0A.
      *-----------------------------------------------------------------
      *N0A-A.  APPINIT WCIS
      *-----------------------------------------------------------------
           PERFORM WCIS-INIT-TRAITEMENT
      *-----------------------------------------------------------------
      *N0AZD. APPEL  MXTU1450 POUR 9B02-YDAJOU
      *-----------------------------------------------------------------
           MOVE SPACES                    TO W-DD00-ENVU045
           MOVE '1'                       TO W-DD00-ZA001H
           MOVE '1'                       TO W-DD00-ZA001D
           MOVE 'S'                       TO W-DD00-ZA001K
           PERFORM F97DD
           MOVE W-DD00-DATE8              TO 9B02-YDAJOU
           MOVE 9B02-YDAJOU               TO DAT8E DAT6C
           MOVE DAT83E                    TO DAT61C
           MOVE DAT81E                    TO DAT63C
           MOVE DAT82E                    TO DAT62C
           MOVE DAT6C                     TO DAT8
           MOVE DAT8                      TO DAT8E DAT6C
           MOVE DAT61C                    TO DAT81C
           MOVE DAT62C                    TO DAT82C
           MOVE DAT63C                    TO DAT83C
           MOVE W-DD00-HESOR              TO 9B02-YHESYS
           MOVE 9B02-YHESYS               TO DAT8E DAT6C
      *APPEL MXTU1450  POUR 9B02-YDABAT
           MOVE SPACES                    TO W-DD00-ENVU045
           MOVE '1'                       TO W-DD00-ZA001H
           MOVE '1'                       TO W-DD00-ZA001D
           MOVE 'L'                       TO W-DD00-ZA001K
           PERFORM F97DD
           MOVE W-DD00-DATE8              TO 9B02-YDABAT
           MOVE 9B02-YDABAT               TO DAT8E DAT6C
           MOVE DAT83E                    TO DAT61C
           MOVE DAT81E                    TO DAT63C
           MOVE DAT82E                    TO DAT62C
           MOVE DAT6C                     TO DAT8
           MOVE DAT8                      TO DAT8E DAT6C
           MOVE DAT61C                    TO DAT81C
           MOVE DAT62C                    TO DAT82C
           MOVE DAT63C                    TO DAT83C
           MOVE DAT8C                     TO 9B02-YDABA2
           MOVE '.'                       TO 9B02-YDABA2 (3 : 1)
                                             9B02-YDABA2 (6 : 1)
           MOVE W-DD00-HESOR              TO 9B02-YHEUL1
           MOVE 9B02-YHEUL1               TO DAT8E DAT6C
           .
       F0D.
      *+------------------------------+
      *I     INITIALISATIONS DB2      I
      *+------------------------------+
           MOVE 0                         TO SQLCODE IK
           EXEC SQL WHENEVER SQLWARNING CONTINUE END-EXEC
           EXEC SQL WHENEVER SQLERROR CONTINUE END-EXEC
      *-----------------------------------------------------------------
      *N0DDB. DISPLAY DEBUT PROGRAMME
      *-----------------------------------------------------------------
           DISPLAY '******************************'
                   '******************************'
                   '******************************'
           DISPLAY 'DEBUT PGM : ' PROGE
                   ' NOM PAC : ' PROGR ' / '
                   APPLI ' GENERE LE : ' DATGN
                   ' PAR : ' CODUTI ' SESSION : '
                   NUGNA
           .
      *N01.           *************************************.
      *               *INITIALISATIONS                    *
      *               *************************************.
       F01-INITIALISATIONS.
      *-----------------------------------------------------------------
      *N01AL. INITIALISATION FICHIER  AL-FICHIER
      *-----------------------------------------------------------------
           OPEN OUTPUT AL-FICHIER
      *-----------------------------------------------------------------
      *N01CR. INITIALISATION FICHIER  CR-FICHIER
      *-----------------------------------------------------------------
           OPEN OUTPUT CR-FICHIER
           PERFORM WITH TEST AFTER UNTIL TE-FT = '1'
             PERFORM F95TE
             IF TE-FT NOT = '1'
               ADD 1                      TO ITE00L
               IF ITE00L <= 0500
                 MOVE TE00                TO 1-TE00 (ITE00L)
               END-IF
             END-IF
           END-PERFORM
           IF ITE00L > ITE00M
             MOVE ITE00L                  TO ITE00R
             MOVE ITE00M                  TO ITE00L
           END-IF
      *-----------------------------------------------------------------
      *N01UA. INITIALISATION FICHIER  UA-FICHIER
      *-----------------------------------------------------------------
           OPEN INPUT UA-FICHIER
           READ UA-FICHIER
             AT END
             MOVE 1                       TO UA-FI
           END-READ
      *-----------------------------------------------------------------
      *N01UB. INITIALISATION FICHIER  UB-FICHIER
      *-----------------------------------------------------------------
           OPEN OUTPUT UB-FICHIER
           .
      *N02.           *************************************.
      *               *TRAITEMENT INITIAL                 *
      *               *************************************.
       F02.
      *-----------------------------------------------------------------
      *N02BB. INITIALISATION DU TOP TRAITEMENT
      *-----------------------------------------------------------------
           MOVE 'O'                       TO WC00-ZA001E
           INITIALIZE WE00-COICTA
             WE00-CTOPI2
             WE00-CODMCC
             WE00-CENOSH
             WE00-COCART
             WE00-CELGC2
             WE00-ZN002
      *-----------------------------------------------------------------
      *N02BE. CALCUL DES DATES PIVOTS
      *-----------------------------------------------------------------
      *-----------------------------------------------------------------
      *N02BF. DATE DE TRAITEMENT - 1 AN
      *-----------------------------------------------------------------
      *-----------------------------------------------------------------
      *N02BJ. APPEL AU MODULE RTRU004
      *-----------------------------------------------------------------
           INITIALIZE BC01
           MOVE 'CAL'                     TO BC01-COCOM
           MOVE SPACE                     TO BC01-CTFDAT
           MOVE 'ECO'                     TO BC01-COETBL
           MOVE '9999'                    TO BC01-COTYCA
           MOVE '3'                       TO BC01-COENV
           MOVE 9B02-YDABAT               TO BC01-DATEES (1)
           MOVE -1                        TO BC01-QTJSM
           MOVE 'A'                       TO BC01-CEUNIT
           PERFORM F96DB
      *-----------------------------------------------------------------
      *N02BN. CONTROLE DU CODE RETOUR : KO
      *-----------------------------------------------------------------
           IF BC01-YGREG NOT = SPACE
             DISPLAY '******************************'
             DISPLAY 'PROBLEME SUR APPEL A RTRU004'
             DISPLAY 'CODE RETOUR  : ' BC01-YGREG
             DISPLAY 'DATE TRAITEE : ' BC01-DATEES (1)
             DISPLAY 'LIBELLE ERREUR : ' BC01-YLIER2
             DISPLAY '******************************'
             PERFORM F98BX
           ELSE
      *-----------------------------------------------------------------
      *N02BR. CONTROLE DU CODE RETOUR : OK
      *       MEMO DE LA DATE TRAIT - 1 AN
      *-----------------------------------------------------------------
             MOVE BC01-DATEES (2)         TO WE00-DATEFI
      *-----------------------------------------------------------------
      *N02BT. DATE DE TRAITEMENT - 1 AN ET 67J
      *-----------------------------------------------------------------
             INITIALIZE BC01
             MOVE SPACE                   TO BC01-CTFDAT
             MOVE 'CAL'                   TO BC01-COCOM
             MOVE 'J'                     TO BC01-CEUNIT
             MOVE -67                     TO BC01-QTJSM
             MOVE WE00-DATEFI             TO BC01-DATEES (1)
             PERFORM F96DB
      *-----------------------------------------------------------------
      *N02BV. CONTROLE DU CODE RETOUR : KO
      *-----------------------------------------------------------------
             IF BC01-YGREG NOT = SPACE
               DISPLAY '******************************'
               DISPLAY 'PROBLEME SUR APPEL A RTRU004'
               DISPLAY 'CODE RETOUR  : ' BC01-YGREG
               DISPLAY 'DATE TRAITEE : ' BC01-DATEES (1)
               DISPLAY 'LIBELLE ERREUR : ' BC01-YLIER2
               DISPLAY '******************************'
               PERFORM F98BX
             ELSE
      *-----------------------------------------------------------------
      *N02BX. CONTROLE DU CODE RETOUR : OK
      *       MEMO DE LA DATE TT - 1 AN ET 67J
      *-----------------------------------------------------------------
               MOVE BC01-DATEES (2)       TO WE05-DATEFI
             END-IF
           END-IF
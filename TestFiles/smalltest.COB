      OPEN OUTPUT AL-FICHIER
      *-----------------------------------------------------------------
      *N01CR. INITIALISATION FICHIER  CR-FICHIER
      *-----------------------------------------------------------------
               IF WB61-MTFACR = ZERO OR WB61-MTFACR = 9999999.99
                 MOVE '48'                TO WW00-COMRJ1
               ELSE
                 MOVE '46'                TO WW00-COMRJ1
               END-IF
           DISPLAY 'MOTIF REJET NON TROUVE :'
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
           IF ITE00L > ITE00M
             MOVE ITE00L                  TO ITE00R.
        IF 9-TE00-YCFDB2 NOT = '1'
           *EXEC SQL OPEN C-TE00 END-EXEC
             PERFORM F98BD THRU F98BD-FN
             MOVE '1'                     TO 9-TE00-YCFDB2
           END-IF
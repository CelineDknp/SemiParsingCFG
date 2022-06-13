       IDENTIFICATION DIVISION.
       PROGRAM-ID.    PerformUntilTest1.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       PROCEDURE DIVISION.

      *-----------------------------------------------------------------
      *N98BQ. EMISSION MESSAGE DSNTIAR
      *-----------------------------------------------------------------
           PERFORM VARYING J98BQR FROM 1 BY 1
                     UNTIL 1 < J98BQR
             DISPLAY W-MESS-YLSQLM (J98BQR)
           END-PERFORM

      *-----------------------------------------------------------------
      *N98BQ. EMISSION MESSAGE DSNTIAR
      *-----------------------------------------------------------------
           PERFORM VARYING J98BQR FROM 1 BY 1
                     UNTIL 2 < J98BQR
             IF A > 0
               DISPLAY "A"
             END-IF 
           END-PERFORM
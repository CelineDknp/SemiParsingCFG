       IDENTIFICATION DIVISION.
       PROGRAM-ID.    IFTest11.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       PROCEDURE DIVISION.
           IF A > 0
             NEXT SENTENCE
           ELSE
             DISPLAY 'ELSE CONTENT ' 
           END-IF
           IF B = 0
             DISPLAY 'SECOND IF'
           END-IF.
       IDENTIFICATION DIVISION.
       PROGRAM-ID.    IFTest11NoMatch.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       PROCEDURE DIVISION.
           IF C > 0
             DISPLAY 'IF CONTENT '
             IF D > 0
              DISPLAY 'SECOND IF CONTENT '
             END-IF
           ELSE
             DISPLAY 'ELSE CONTENT ' 
           END-IF
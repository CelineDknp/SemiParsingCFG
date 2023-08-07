       IDENTIFICATION DIVISION.
       PROGRAM-ID.    IFTest11Skip.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       PROCEDURE DIVISION.
           IF A > 0
             DISPLAY 'IF CONTENT '
             IF B > 0
              DISPLAY 'SECOND IF CONTENT '
             END-IF
           ELSE
             DISPLAY 'ELSE CONTENT ' 
           END-IF
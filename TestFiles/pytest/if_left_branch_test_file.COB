       IDENTIFICATION DIVISION.
       PROGRAM-ID.    IFTest6.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       PROCEDURE DIVISION.
           IF A > 0
             EXEC SQL OPEN DB END-EXEC
           ELSE
             DISPLAY 'ELSE CONTENT ' 
           END-IF
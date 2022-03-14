       IDENTIFICATION DIVISION.
       PROGRAM-ID.    IFTest12.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       PROCEDURE DIVISION.
           IF A > 0
             DISPLAY 'IF CONTENT' 
           ELSE
             EXEC SQL OPEN DB END-EXEC
           END-IF
       IDENTIFICATION DIVISION.
       PROGRAM-ID.    IFTest1.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       PROCEDURE DIVISION.
           IF A > 0
             EXEC SQL OPEN DB END-EXEC
           ELSE
             EXEC SQL OPEN DB END-EXEC
           END-IF
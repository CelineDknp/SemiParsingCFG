       IDENTIFICATION DIVISION.
       PROGRAM-ID.    EVALUATETest1.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       PROCEDURE DIVISION.
           EVALUATE TRUE
             WHEN A > 0
               EXEC SQL OPEN DB1 END-EXEC
             WHEN A < 0
               EXEC SQL OPEN DB2 END-EXEC
             WHEN A = 0
               EXEC SQL OPEN DB3 END-EXEC
           END-EVALUATE
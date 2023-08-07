       IDENTIFICATION DIVISION.
       PROGRAM-ID.    BeforeEVALUATETest1.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       PROCEDURE DIVISION.
           IF A > 0
               EXEC SQL OPEN DB1 END-EXEC
           END-IF
           IF A < 0
               EXEC SQL OPEN DB2 END-EXEC
           END-IF
           IF A = 0
               EXEC SQL OPEN DB3 END-EXEC
           END-IF
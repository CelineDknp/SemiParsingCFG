       IDENTIFICATION DIVISION.
       PROGRAM-ID.    IFTest16.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       PROCEDURE DIVISION.
           IF A > 0
            DISPLAY 'IF 1'
           END-IF
           IF B > 0
            DISPLAY 'IF 1'
           END-IF
           IF C > 0
            EXEC SQL OPEN DB END-EXEC
           END-IF
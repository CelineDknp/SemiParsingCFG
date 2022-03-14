       IDENTIFICATION DIVISION.
       PROGRAM-ID.    IFTest13.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       PROCEDURE DIVISION.
           IF A > 0
            DISPLAY 'IF 1'
           END-IF
           IF B > 0
            DISPLAY 'IF 2'
           END-IF
           IF C > 0
            DISPLAY 'IF 3'
           END-IF
           IF D > 0
            DISPLAY 'IF 4'
           END-IF
           IF E > 0
            DISPLAY 'IF 5'
           END-IF
           EXEC SQL OPEN DB END-EXEC
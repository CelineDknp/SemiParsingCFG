       IDENTIFICATION DIVISION.
       PROGRAM-ID.    IFTest8.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       PROCEDURE DIVISION.
           IF A > 0
             IF B > 0
                DISPLAY 'INNER IF CONTENT'
             END-IF
           ELSE
              DISPLAY 'ELSE CONTENT'
           END-IF
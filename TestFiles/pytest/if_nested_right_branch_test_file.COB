       IDENTIFICATION DIVISION.
       PROGRAM-ID.    IFTest9.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       PROCEDURE DIVISION.
           IF A > 0
             DISPLAY 'ELSE CONTENT' 
           ELSE
             IF B > 0
                DISPLAY 'INNER IF CONTENT'
             END-IF
           END-IF
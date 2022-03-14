       IDENTIFICATION DIVISION.
       PROGRAM-ID.    IFTest7.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       PROCEDURE DIVISION.
           IF A > 0
             IF B > 0
                DISPLAY 'INNER IF1 CONTENT'
             END-IF
           ELSE
             IF C > 0
                DISPLAY 'INNER IF2 CONTENT'
             END-IF
           END-IF
       IDENTIFICATION DIVISION.
       PROGRAM-ID.    CommentTest.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       PROCEDURE DIVISION.
      * This is a comment to be ignored by the parser despite it having code : IF A > 0
           IF A > 0
             DISPLAY 'IF CONTENT '
           ELSE
             DISPLAY 'ELSE CONTENT ' 
           END-IF

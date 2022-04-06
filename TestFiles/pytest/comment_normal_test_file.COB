       IDENTIFICATION DIVISION.
       PROGRAM-ID.    CommentTest.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       PROCEDURE DIVISION.
      * This is a comment to be ignored by the parser despite it having code : IF A > 0
      * This is a comment that should be included in the first
           IF A > 0
             DISPLAY ' IF CONTENT '
           ELSE
             DISPLAY ' ELSE CONTENT '
           END-IF
      * This is a comment that should just be skipped by the parser
           IF B > 0
             DISPLAY 'String to ignore'
           END-IF


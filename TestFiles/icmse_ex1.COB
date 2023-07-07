       IDENTIFICATION DIVISION.
       PROGRAM-ID.    IFTest1.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       PROCEDURE DIVISION.
       P1.
           PERFORM P2.
           IF A < 0
              NEXT SENTENCE
           END-IF
       P2.
           IF B = 0
             EXEC SQL OPEN DB END-EXEC
           END-IF.
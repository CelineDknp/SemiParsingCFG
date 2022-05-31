       IDENTIFICATION   DIVISION.
       PROGRAM-ID.      Example1.
       PROCEDURE DIVISION.
       P0.
           DISPLAY "--- Start ---".
           IF A = 0 
               PERFORM P1
           END-IF
       PZ.        
           DISPLAY "--- End ---".
           STOP RUN.     
       P1.
           DISPLAY "--- P1 ---".


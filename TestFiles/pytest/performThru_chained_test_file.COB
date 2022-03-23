       IDENTIFICATION   DIVISION.
       PROGRAM-ID.      performTest2.
       PROCEDURE DIVISION.
       P0.
           DISPLAY "--- Start ---".
           PERFORM P1 THRU P3.
       PZ.        
           DISPLAY "--- End ---".
           STOP RUN.     
       P1.
           DISPLAY "--- P1 ---".
           PERFORM P4 THRU P5.
      * All below is dead code
       P2.
           DISPLAY "--- P2 ---".
       P3.
           DISPLAY "--- P3 ---".
       P4.
           DISPLAY "--- P4 ---".
       P5.
           DISPLAY "--- P5 ---".


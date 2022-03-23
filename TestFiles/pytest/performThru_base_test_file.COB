       IDENTIFICATION   DIVISION.
       PROGRAM-ID.      performTest1.
       PROCEDURE DIVISION.
       P0.
           DISPLAY "--- Start ---".
           PERFORM P1 THRU P4.
       PZ.        
           DISPLAY "--- End ---".
           STOP RUN.     
       P1.
           DISPLAY "--- P1 ---".
       P2.
           DISPLAY "--- P2 ---".
       P3.
           DISPLAY "--- P3 ---".
       P4.
           DISPLAY "--- P4 ---".
      * All below is dead code           
       P5.
           DISPLAY "--- P5 ---".


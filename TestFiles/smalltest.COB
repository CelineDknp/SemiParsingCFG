            IF 1-UA00-CEENRA = 0 OR 9
             MOVE A TO UB4
             ELSE 
             IF 1-UA00-CEENRA = 00
      *ALIMENTATION AVANT ECRITURE
               MOVE 1-UA00                TO UB40
             ELSE
               MOVE 1-UA00                TO UB49
             END-IF
      *ECRITURE
             PERFORM F90UB
            END-IF
           F30AR.
           EVALUATE FI31-COOPST (1:1)
             WHEN 'W'
               MOVE 'V'                   TO WW00-CORESO
               MOVE '4'                   TO WW00-ENR
               ADD 1                      TO WW00-VISACPT
             WHEN 'N'
               MOVE 'M'                   TO WW00-CORESO
               ADD 1                      TO WW00-MASTCPT
             WHEN '1'
               MOVE 'S'                   TO WW00-CORESO
               MOVE '1'                   TO WW00-ENR
             WHEN 'U'
               MOVE 'U'                   TO WW00-CORESO
               MOVE '1'                   TO WW00-ENR
             WHEN 'G'
      *'G'              WW00-CORESO
               MOVE 'V'                   TO WW00-CORESO
               MOVE '1'                   TO WW00-ENR
               ADD 1                      TO WW00-VISACPT
             WHEN 'E'
             WHEN 'F'
      *'E'              WW00-CORESO
               MOVE 'M'                   TO WW00-CORESO
               MOVE '1'                   TO WW00-ENR
               ADD 1                      TO WW00-MASTCPT
             WHEN '4'
               MOVE '5'                   TO WW00-ENR
               MOVE 'S'                   TO WW00-CORESO
             WHEN OTHER
               CONTINUE
           END-EVALUATE
           IF FI31-COOPST = 'N12' OR 'N17'
             MOVE '6'                     TO WW00-ENR
           END-IF
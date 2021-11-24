
      IF FT = ALL '1'
      *-----------------------------------------------------------------
      *N20AL. DISPLAY FICHIER ALERTE
      *-----------------------------------------------------------------
             DISPLAY '------------------------------'
             DISPLAY 'NOMBRE ENREGISTREMENTS '
                     'ECRIT'
                     ' DU FICHIER ALERTE : '
                     5-AL00-CPTENR
             DISPLAY '------------------------------'
             CLOSE AL-FICHIER
      *-----------------------------------------------------------------
      *N20BB.      CONTROLE MISE EN SUSPENS
      *                ANNULATION
      *-----------------------------------------------------------------
             IF TOP-ANN = '1' AND WA00-ZN009 NOT = 0
               DISPLAY '!!!! CONTROLE KO POUR UNE '
                       'ANNULATION !!!!'
               PERFORM F98BX
             END-IF
        END-IF
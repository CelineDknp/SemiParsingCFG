           IF ITE00R > 0
             DISPLAY 'CHARGEMENT INCOMPLET DE LA '
                     'TABLE ALCMAJ. '
                     'POSTES LUS : ' ITE00R
             PERFORM F98BX
           ELSE
             DISPLAY 'NOMBRE DE POSTES LUS : ' ITE00L
           END-IF
               DISPLAY '***************************'
               DISPLAY '* PROBLEME ACCES ALC00003 *'
               DISPLAY '***************************'
               DISPLAY '* NUM REMETTANT * ' QT47-CORRCO
                       '   *'
               DISPLAY '***************************'
               DISPLAY '* ARRET PROGRAMME !!!!!!! *'
               DISPLAY '***************************'
               PERFORM F98BX
           END-EVALUATE
           .
     
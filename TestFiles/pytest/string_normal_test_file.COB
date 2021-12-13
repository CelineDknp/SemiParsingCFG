01 CONSTANTES-PAC.
         05 FILLER             PIC  X(87)        VALUE 
          'This is a string with code: IF A > 0'
            .
           IF A > 0
             DISPLAY 'IF CONTENT '
           ELSE
             DISPLAY 'ELSE CONTENT ' 
           END-IF

           EVALUATE TRUE
             WHEN A > 0
               IF B > 1
                 EXEC SQL OPEN DB1 END-EXEC
               ELSE
                 DISPLAY '1'
               END-IF
             WHEN A < 0
               IF B > 2
                 DISPLAY '1'
               ELSE
                 EXEC SQL OPEN DB2 END-EXEC
               END-IF
             WHEN A = 0
               EXEC SQL OPEN DB3 END-EXEC
           END-EVALUATE
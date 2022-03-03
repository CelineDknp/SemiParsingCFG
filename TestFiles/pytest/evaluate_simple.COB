           EVALUATE TRUE
             WHEN A > 0
               EXEC SQL OPEN DB1 END-EXEC
             WHEN A < 0
               EXEC SQL OPEN DB2 END-EXEC
             WHEN A = 0
               EXEC SQL OPEN DB3 END-EXEC
           END-EVALUATE
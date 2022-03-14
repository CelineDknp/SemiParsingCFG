       IDENTIFICATION DIVISION.
       PROGRAM-ID.    EXECSQLTest1.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       PROCEDURE DIVISION.
      EXEC SQL
        CLOSE DB1
      END-EXEC

      EXEC SQL
        CLOSE DB2
      end-exec

      exec sql
        CLOSE DB3
      END-EXEC

      exec sql
        CLOSE DB4
      end-exec
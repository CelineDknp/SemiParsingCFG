       IDENTIFICATION DIVISION.
       PROGRAM-ID. COB004.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       COPY COB004.
       COPY DFHAID.
       COPY DFHBMSCA.
       COPY SQLCA.
       COPY C004CA.
       01 W-LINE.
         10 customerid pic 999999.
         10 FILLER pic x.
         10 lastname pic x(15).
         10 filler pic x.
         10 firstname pic x(15).
         10 filler pic x.
         10 zipcode pic xxxx.
         10 filler pic x.
         10 city pic x(10).
         10 filler pic x.
         10 birthdate pic x(10).
       01 W-ATTR PIC X.
       01 W-ROW PIC 99.
       01 W-SEL PIC 99.
       01 W-COLUMN PIC 99.
       01 W-MSG PIC X(80).
       01 W-EIBCPOSN PIC S9(4) COMP VALUE 0.
       01 W-CUSTOMERID-MIN PIC S9(9) COMP-5.
       01 W-CUSTOMERID-MAX PIC S9(9) COMP-5.
       01 W-I PIC S9(4) COMP.
       01 W-J PIC S9(4) COMP.
       01 W-FILTERCHANGE PIC 9 VALUE 0.
	   EXEC SQL
	     DECLARE CUR-F8 CURSOR FOR
		 SELECT CustomerId, FirstName, LastName, C.ZipCode,
         BirthDate
		 FROM
             dbo.Customer C,
             dbo.ZipCode Z
         WHERE
             CustomerId > :C004-CUSTOMERID-LAST AND
             CustomerId
                 BETWEEN
                     :W-CUSTOMERID-MIN AND
                     :W-CUSTOMERID-MAX AND
             LastName
                 LIKE RTRIM(:C004-LASTNAME-FILTER) || '%' AND
             Firstname
                 LIKE RTRIM(:C004-FIRSTNAME-FILTER) || '%' AND
             C.ZipCode
                 LIKE RTRIM(:C004-ZIPCODE-FILTER) || '%' AND
             BirthDate
                 LIKE RTRIM(:C004-BIRTHDATE-FILTER) || '%' AND
             Z.City
                 LIKE RTRIM(:C004-CITY-FILTER) || '%' AND
             Z.ZipCode = C.ZipCode
		 ORDER BY CustomerId
	   END-EXEC.
	   EXEC SQL
	     DECLARE CUR-F7 CURSOR FOR
		 SELECT CustomerId, FirstName, LastName, C.ZipCode,
         BirthDate
		 FROM
             dbo.Customer C,
             dbo.ZipCode Z
         WHERE
             CustomerId < :C004-CUSTOMERID-FIRST AND
             CustomerId
                 BETWEEN
                     :W-CUSTOMERID-MIN AND
                     :W-CUSTOMERID-MAX AND
             LastName
                 LIKE RTRIM(:C004-LASTNAME-FILTER) || '%' AND
             Firstname
                 LIKE RTRIM(:C004-FIRSTNAME-FILTER) || '%' AND
             C.ZipCode
                 LIKE RTRIM(:C004-ZIPCODE-FILTER) || '%' AND
             BirthDate
                 LIKE RTRIM(:C004-BIRTHDATE-FILTER) || '%' AND
             Z.City
                 LIKE RTRIM(:C004-CITY-FILTER) || '%' AND
             Z.ZipCode = C.ZipCode
		 ORDER BY CustomerId desc
	   END-EXEC.
       .

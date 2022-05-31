101900 IDENTIFICATION DIVISION.                                         IC2224.2
102000 PROGRAM-ID.                                                      IC2224.2
102100     IC222A-1.                                                    IC2224.2
102200****************************************************************  IC2224.2
102300*                                                              *  IC2224.2
102400*    THIS PROGRAM FORMS PART OF THE COBOL COMPILER VALIDATION  *  IC2224.2
102500*    SYSTEM (CCVS) USED TO TEST COBOL COMPILERS FOR            *  IC2224.2
102600*    CONFORMANCE WITH THE AMERICAN NATIONAL STANDARD           *  IC2224.2
102700*    (ANSI DOCUMENT REFERENCE: X3.23-1985) AND THE STANDARD OF *  IC2224.2
102800*    THE INTERNATIONAL ORGANIZATION FOR STANDARDISATION        *  IC2224.2
102900*    (ISO DOCUMENT REFERENCE: ISO-1989-1985).                  *  IC2224.2
103000*                                                              *  IC2224.2
103100*    THIS CCVS INCORPORATES ENHANCEMENTS TO THE CCVS FOR THE   *  IC2224.2
103200*    1974 STANDARD (ANSI DOCUMENT REFERENCE: X3.23-1974; ISO   *  IC2224.2
103300*    DOCUMENT REFERENCE: ISO-1989-1978).                       *  IC2224.2
103400*                                                              *  IC2224.2
103500*    THESE ENHANCEMENTS WERE SPECIFIED BY A PROJECT TEAM WHICH *  IC2224.2
103600*    WAS FUNDED BY THE COMMISSION FOR EUROPEAN COMMUNITIES AND *  IC2224.2
103700*    WHICH WAS RESPONSIBLE FOR TECHNICAL ISSUES TO:            *  IC2224.2
103800*                                                              *  IC2224.2
103900*          THE FEDERAL SOFTWARE TESTING CENTER                 *  IC2224.2
104000*          OFFICE OF SOFTWARE DEVELOPMENT                      *  IC2224.2
104100*                & INFORMATION TECHNOLOGY                      *  IC2224.2
104200*          TWO SKYLINE PLACE                                   *  IC2224.2
104300*          SUITE 1100                                          *  IC2224.2
104400*          5203 LEESBURG PIKE                                  *  IC2224.2
104500*          FALLS CHURCH                                        *  IC2224.2
104600*          VA 22041                                            *  IC2224.2
104700*          U.S.A.                                              *  IC2224.2
104800*                                                              *  IC2224.2
104900*    THE PROJECT TEAM MEMBERS WERE:                            *  IC2224.2
105000*                                                              *  IC2224.2
105100*          BIADI (BUREAU INTER ADMINISTRATION                  *  IC2224.2
105200*                 DE DOCUMENTATION INFORMATIQUE)               *  IC2224.2
105300*          21 RUE BARA                                         *  IC2224.2
105400*          F-92132 ISSY                                        *  IC2224.2
105500*          FRANCE                                              *  IC2224.2
105600*                                                              *  IC2224.2
105700*                                                              *  IC2224.2
105800*          GMD (GESELLSCHAFT FUR MATHEMATIK                    *  IC2224.2
105900*               UND DATENVERARBEITUNG MBH)                     *  IC2224.2
106000*          SCHLOSS BIRLINGHOVEN                                *  IC2224.2
106100*          POSTFACH 12 40                                      *  IC2224.2
106200*          D-5205 ST. AUGUSTIN 1                               *  IC2224.2
106300*          GERMANY FR                                          *  IC2224.2
106400*                                                              *  IC2224.2
106500*                                                              *  IC2224.2
106600*          NCC (THE NATIONAL COMPUTING CENTRE LTD)             *  IC2224.2
106700*          OXFORD ROAD                                         *  IC2224.2
106800*          MANCHESTER                                          *  IC2224.2
106900*          M1 7ED                                              *  IC2224.2
107000*          UNITED KINGDOM                                      *  IC2224.2
107100*                                                              *  IC2224.2
107200*                                                              *  IC2224.2
107300*    THIS TEST SUITE WAS PRODUCED BY THE NATIONAL COMPUTING    *  IC2224.2
107400*    CENTRE IN ENGLAND AND IS THE OFFICIAL CCVS TEST SUITE     *  IC2224.2
107500*    USED THROUGHOUT EUROPE AND THE UNITED STATES OF AMERICA.  *  IC2224.2
107600*                                                              *  IC2224.2
107700*    REVISED 1986 AUGUST                                       *  IC2224.2
107800*                                                              *  IC2224.2
107900****************************************************************  IC2224.2
108000*                                                              *  IC2224.2
108100*    VALIDATION FOR:-                                          *  IC2224.2
108200*                                                              *  IC2224.2
108300*    "ON-SITE VALIDATION, NATIONAL INSTITUTE OF STD & TECH.     ".IC2224.2
108400*                                                              *  IC2224.2
108500*    "COBOL 85 VERSION 4.2, Apr  1993 SSVG                      ".IC2224.2
108600*                                                              *  IC2224.2
108700****************************************************************  IC2224.2
108800*                                                              *  IC2224.2
108900*      X-CARDS USED BY THIS PROGRAM ARE :-                     *  IC2224.2
109000*                                                              *  IC2224.2
109100*            X-82   SOURCE-COMPUTER                            *  IC2224.2
109200*            X-83   OBJECT-COMPUTER.                           *  IC2224.2
109300*                                                              *  IC2224.2
109400****************************************************************  IC2224.2
109500*                                                              *  IC2224.2
109600*    THE SOURCE FILE CONTAINS TWO PROGRAMS, IC222A AND         *  IC2224.2
109700*    IC222A-1, WHICH TEST LANGUAGE ELEMENTS FROM  LEVEL 2 OF   *  IC2224.2
109800*    THE INTER-PROGRAM COMMUNICATION MODULE.  THE LANGUAGE     *  IC2224.2
109900*    ELEMENTS TESTED ARE:                                      *  IC2224.2
110000*          "ON EXCEPTION"     PHRASE                           *  IC2224.2
110100*          "NOT ON EXCEPTION" PHRASE                           *  IC2224.2
110200*          "END-CALL"         PHRASE                           *  IC2224.2
110300*          "ON OVERFLOW"      PHRASE                           *  IC2224.2
110400*                                                                 IC2224.2
110500*    THE TWO PROGRAMS SHOULD BE COMPILED IN THE SAME           *  IC2224.2
110600*    INVOCATION OF THE COMPILER TO TEST THE BATCH COMPILATION  *  IC2224.2
110700*    FEATURE AND RECOGNITION OF THE END PROGRAM HEADER.  THE   *  IC2224.2
110800*    ARRANGEMENT OF THE PROGRAMS IN THE SOURCE FILE IS:           IC2224.2
110900*                                                                 IC2224.2
111000*    IDENTIFICATION DIVISION.                                     IC2224.2
111100*    PROGRAM-ID. IC222A.                                          IC2224.2
111200*          .                                                      IC2224.2
111300*          .                                                      IC2224.2
111400*          .                                                      IC2224.2
111500*    END PROGRAM IC222A.                                          IC2224.2
111600*    IDENTIFICATION DIVISION.                                     IC2224.2
111700*    PROGRAM-ID. IC222A-1.                                        IC2224.2
111800*          .                                                      IC2224.2
111900*          .                                                      IC2224.2
112000*          .                                                      IC2224.2
112100*                                                                 IC2224.2
112200*    A FULL DESCRIPTION OF THE TWO PROGRAMS IS INCLUDED AS     *  IC2224.2
112300*    COMMENTS IN PROGRAM IC222A.                               *  IC2224.2
112400*                                                              *  IC2224.2
112500****************************************************************  IC2224.2
112600*                                                                 IC2224.2
112700 ENVIRONMENT DIVISION.                                            IC2224.2
112800 CONFIGURATION SECTION.                                           IC2224.2
112900 SOURCE-COMPUTER.                                                 IC2224.2
113000     Linux.                                                       IC2224.2
113100 OBJECT-COMPUTER.                                                 IC2224.2
113200     Linux.                                                       IC2224.2
113300 INPUT-OUTPUT SECTION.                                            IC2224.2
113400 FILE-CONTROL.                                                    IC2224.2
113500     SELECT PRINT-FILE ASSIGN TO                                  IC2224.2
113600     "report.log".                                                IC2224.2
113700*                                                                 IC2224.2
113800 DATA DIVISION.                                                   IC2224.2
113900 FILE SECTION.                                                    IC2224.2
114000 FD  PRINT-FILE.                                                  IC2224.2
114100 01  PRINT-REC PICTURE X(120).                                    IC2224.2
114200 01  DUMMY-RECORD PICTURE X(120).                                 IC2224.2
114300 WORKING-STORAGE SECTION.                                         IC2224.2
114400 77  WS1 PICTURE S999.                                            IC2224.2
114500 77  WS2 PICTURE S999                                             IC2224.2
114600         USAGE COMPUTATIONAL, VALUE ZERO.                         IC2224.2
114700 LINKAGE SECTION.                                                 IC2224.2
114800 77  DN1 PICTURE S99.                                             IC2224.2
114900 77  DN2 PICTURE S99 USAGE COMPUTATIONAL.                         IC2224.2
115000 77  DN3 PICTURE S99.                                             IC2224.2
115100 77  DN4 PICTURE S99 USAGE COMPUTATIONAL.                         IC2224.2
115200*                                                                 IC2224.2
115300 PROCEDURE DIVISION USING DN1, DN2, DN3, DN4.                     IC2224.2
115400 SECT-IC222A-1-001 SECTION.                                       IC2224.2
115500 CALL-TEST-001.                                                   IC2224.2
115600     MOVE DN1 TO WS1.                                             IC2224.2
115700     ADD 1 TO WS1.                                                IC2224.2
115800     ADD 1 TO WS2.                                                IC2224.2
115900     MOVE WS1 TO DN3.                                             IC2224.2
116000     MOVE WS2 TO DN4.                                             IC2224.2
116100 CALL-EXIT-001.                                                   IC2224.2
116200     EXIT PROGRAM.                                                IC2224.2

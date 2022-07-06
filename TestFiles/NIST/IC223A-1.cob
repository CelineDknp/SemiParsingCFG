064400 IDENTIFICATION DIVISION.                                         IC2234.2
064500 PROGRAM-ID.                                                      IC2234.2
064600     IC223A-1.                                                    IC2234.2
064700****************************************************************  IC2234.2
064800*                                                              *  IC2234.2
064900*    THIS PROGRAM FORMS PART OF THE COBOL COMPILER VALIDATION  *  IC2234.2
065000*    SYSTEM (CCVS) USED TO TEST COBOL COMPILERS FOR            *  IC2234.2
065100*    CONFORMANCE WITH THE AMERICAN NATIONAL STANDARD           *  IC2234.2
065200*    (ANSI DOCUMENT REFERENCE: X3.23-1985) AND THE STANDARD OF *  IC2234.2
065300*    THE INTERNATIONAL ORGANIZATION FOR STANDARDISATION        *  IC2234.2
065400*    (ISO DOCUMENT REFERENCE: ISO-1989-1985).                  *  IC2234.2
065500*                                                              *  IC2234.2
065600*    THIS CCVS INCORPORATES ENHANCEMENTS TO THE CCVS FOR THE   *  IC2234.2
065700*    1974 STANDARD (ANSI DOCUMENT REFERENCE: X3.23-1974; ISO   *  IC2234.2
065800*    DOCUMENT REFERENCE: ISO-1989-1978).                       *  IC2234.2
065900*                                                              *  IC2234.2
066000*    THESE ENHANCEMENTS WERE SPECIFIED BY A PROJECT TEAM WHICH *  IC2234.2
066100*    WAS FUNDED BY THE COMMISSION FOR EUROPEAN COMMUNITIES AND *  IC2234.2
066200*    WHICH WAS RESPONSIBLE FOR TECHNICAL ISSUES TO:            *  IC2234.2
066300*                                                              *  IC2234.2
066400*          THE FEDERAL SOFTWARE TESTING CENTER                 *  IC2234.2
066500*          OFFICE OF SOFTWARE DEVELOPMENT                      *  IC2234.2
066600*                & INFORMATION TECHNOLOGY                      *  IC2234.2
066700*          TWO SKYLINE PLACE                                   *  IC2234.2
066800*          SUITE 1100                                          *  IC2234.2
066900*          5203 LEESBURG PIKE                                  *  IC2234.2
067000*          FALLS CHURCH                                        *  IC2234.2
067100*          VA 22041                                            *  IC2234.2
067200*          U.S.A.                                              *  IC2234.2
067300*                                                              *  IC2234.2
067400*    THE PROJECT TEAM MEMBERS WERE:                            *  IC2234.2
067500*                                                              *  IC2234.2
067600*          BIADI (BUREAU INTER ADMINISTRATION                  *  IC2234.2
067700*                 DE DOCUMENTATION INFORMATIQUE)               *  IC2234.2
067800*          21 RUE BARA                                         *  IC2234.2
067900*          F-92132 ISSY                                        *  IC2234.2
068000*          FRANCE                                              *  IC2234.2
068100*                                                              *  IC2234.2
068200*                                                              *  IC2234.2
068300*          GMD (GESELLSCHAFT FUR MATHEMATIK                    *  IC2234.2
068400*               UND DATENVERARBEITUNG MBH)                     *  IC2234.2
068500*          SCHLOSS BIRLINGHOVEN                                *  IC2234.2
068600*          POSTFACH 12 40                                      *  IC2234.2
068700*          D-5205 ST. AUGUSTIN 1                               *  IC2234.2
068800*          GERMANY FR                                          *  IC2234.2
068900*                                                              *  IC2234.2
069000*                                                              *  IC2234.2
069100*          NCC (THE NATIONAL COMPUTING CENTRE LTD)             *  IC2234.2
069200*          OXFORD ROAD                                         *  IC2234.2
069300*          MANCHESTER                                          *  IC2234.2
069400*          M1 7ED                                              *  IC2234.2
069500*          UNITED KINGDOM                                      *  IC2234.2
069600*                                                              *  IC2234.2
069700*                                                              *  IC2234.2
069800*    THIS TEST SUITE WAS PRODUCED BY THE NATIONAL COMPUTING    *  IC2234.2
069900*    CENTRE IN ENGLAND AND IS THE OFFICIAL CCVS TEST SUITE     *  IC2234.2
070000*    USED THROUGHOUT EUROPE AND THE UNITED STATES OF AMERICA.  *  IC2234.2
070100*                                                              *  IC2234.2
070200****************************************************************  IC2234.2
070300*                                                              *  IC2234.2
070400*    VALIDATION FOR:-                                          *  IC2234.2
070500*                                                              *  IC2234.2
070600*    "ON-SITE VALIDATION, NATIONAL INSTITUTE OF STD & TECH.     ".IC2234.2
070700*                                                              *  IC2234.2
070800*    "COBOL 85 VERSION 4.2, Apr  1993 SSVG                      ".IC2234.2
070900*                                                              *  IC2234.2
071000****************************************************************  IC2234.2
071100*                                                              *  IC2234.2
071200*      X-CARDS USED BY THIS PROGRAM ARE :-                     *  IC2234.2
071300*                                                              *  IC2234.2
071400*        X-55  - SYSTEM PRINTER NAME.                          *  IC2234.2
071500*        X-82  - SOURCE COMPUTER NAME.                         *  IC2234.2
071600*        X-83  - OBJECT COMPUTER NAME.                         *  IC2234.2
071700*                                                              *  IC2234.2
071800****************************************************************  IC2234.2
071900*                                                              *  IC2234.2
072000*    PROGRAM IC223A AND IC223A-1 WILL TEST THE NEW LANGUAGE    *  IC2234.2
072100*    ELEMENTS FOR THE LEVEL 2 INTER-PROGRAM COMMUNICATION      *  IC2234.2
072200*    MODULE.                                                   *  IC2234.2
072300*    THE NEW LANGUAGE ELEMENTS TO BE TESTED WILL BE:           *  IC2234.2
072400*          "BY REFERENCE"     PHRASE                           *  IC2234.2
072500*    THE TWO PROGRAMS WILL BE COMPILED IN THE SAME FLOW        *  IC2234.2
072600*    (TO TEST THE "END PROGRAM" STATEMENT) AS SHOWN BELOW:     *  IC2234.2
072700*    IDENTIFICATION DIVISION.                                  *  IC2234.2
072800*    PROGRAM-ID. IC223A.                                       *  IC2234.2
072900*              .                                               *  IC2234.2
073000*              .                                               *  IC2234.2
073100*              .                                               *  IC2234.2
073200*    END PROGRAM IC223A.                                       *  IC2234.2
073300*    PROGRAM-ID. IC223A-1.                                     *  IC2234.2
073400*              .                                               *  IC2234.2
073500*              .                                               *  IC2234.2
073600*              .                                               *  IC2234.2
073700****************************************************************  IC2234.2
073800 ENVIRONMENT DIVISION.                                            IC2234.2
073900 CONFIGURATION SECTION.                                           IC2234.2
074000 SOURCE-COMPUTER.                                                 IC2234.2
074100     Linux.                                                       IC2234.2
074200 OBJECT-COMPUTER.                                                 IC2234.2
074300     Linux.                                                       IC2234.2
074400 INPUT-OUTPUT SECTION.                                            IC2234.2
074500 FILE-CONTROL.                                                    IC2234.2
074600     SELECT PRINT-FILE ASSIGN TO                                  IC2234.2
074700     "report.log".                                                IC2234.2
074800 DATA DIVISION.                                                   IC2234.2
074900 FILE SECTION.                                                    IC2234.2
075000 FD  PRINT-FILE.                                                  IC2234.2
075100 01  PRINT-REC PICTURE X(120).                                    IC2234.2
075200 01  DUMMY-RECORD PICTURE X(120).                                 IC2234.2
075300 WORKING-STORAGE SECTION.                                         IC2234.2
075400 77  WS1 PICTURE S999.                                            IC2234.2
075500 77  WS2 PICTURE S999                                             IC2234.2
075600         USAGE COMPUTATIONAL, VALUE ZERO.                         IC2234.2
075700 LINKAGE SECTION.                                                 IC2234.2
075800 77  DN1 PICTURE S99.                                             IC2234.2
075900 77  DN2 PICTURE S99 USAGE COMPUTATIONAL.                         IC2234.2
076000 77  DN3 PICTURE S99.                                             IC2234.2
076100 77  DN4 PICTURE S99 USAGE COMPUTATIONAL.                         IC2234.2
076200 PROCEDURE DIVISION USING DN1, DN2, DN3, DN4.                     IC2234.2
076300 SECT-IC223A-1-001 SECTION.                                       IC2234.2
076400 CALL-TEST-001.                                                   IC2234.2
076500     MOVE DN1 TO WS1.                                             IC2234.2
076600     ADD 1 TO WS1.                                                IC2234.2
076700     ADD 1 TO WS2.                                                IC2234.2
076800     MOVE WS1 TO DN3.                                             IC2234.2
076900     MOVE WS2 TO DN4.                                             IC2234.2
077000 CALL-EXIT-001.                                                   IC2234.2
077100     EXIT PROGRAM.                                                IC2234.2


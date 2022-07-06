093300 IDENTIFICATION DIVISION.                                         IC2254.2
093400 PROGRAM-ID.                                                      IC2254.2
093500     IC225A-1.                                                    IC2254.2
093600****************************************************************  IC2254.2
093700*                                                              *  IC2254.2
093800*    THIS PROGRAM FORMS PART OF THE COBOL COMPILER VALIDATION  *  IC2254.2
093900*    SYSTEM (CCVS) USED TO TEST COBOL COMPILERS FOR            *  IC2254.2
094000*    CONFORMANCE WITH THE AMERICAN NATIONAL STANDARD           *  IC2254.2
094100*    (ANSI DOCUMENT REFERENCE: X3.23-1985) AND THE STANDARD OF *  IC2254.2
094200*    THE INTERNATIONAL ORGANIZATION FOR STANDARDISATION        *  IC2254.2
094300*    (ISO DOCUMENT REFERENCE: ISO-1989-1985).                  *  IC2254.2
094400*                                                              *  IC2254.2
094500*    THIS CCVS INCORPORATES ENHANCEMENTS TO THE CCVS FOR THE   *  IC2254.2
094600*    1974 STANDARD (ANSI DOCUMENT REFERENCE: X3.23-1974; ISO   *  IC2254.2
094700*    DOCUMENT REFERENCE: ISO-1989-1978).                       *  IC2254.2
094800*                                                              *  IC2254.2
094900*    THESE ENHANCEMENTS WERE SPECIFIED BY A PROJECT TEAM WHICH *  IC2254.2
095000*    WAS FUNDED BY THE COMMISSION FOR EUROPEAN COMMUNITIES AND *  IC2254.2
095100*    WHICH WAS RESPONSIBLE FOR TECHNICAL ISSUES TO:            *  IC2254.2
095200*                                                              *  IC2254.2
095300*          THE FEDERAL SOFTWARE TESTING CENTER                 *  IC2254.2
095400*          OFFICE OF SOFTWARE DEVELOPMENT                      *  IC2254.2
095500*                & INFORMATION TECHNOLOGY                      *  IC2254.2
095600*          TWO SKYLINE PLACE                                   *  IC2254.2
095700*          SUITE 1100                                          *  IC2254.2
095800*          5203 LEESBURG PIKE                                  *  IC2254.2
095900*          FALLS CHURCH                                        *  IC2254.2
096000*          VA 22041                                            *  IC2254.2
096100*          U.S.A.                                              *  IC2254.2
096200*                                                              *  IC2254.2
096300*    THE PROJECT TEAM MEMBERS WERE:                            *  IC2254.2
096400*                                                              *  IC2254.2
096500*          BIADI (BUREAU INTER ADMINISTRATION                  *  IC2254.2
096600*                 DE DOCUMENTATION INFORMATIQUE)               *  IC2254.2
096700*          21 RUE BARA                                         *  IC2254.2
096800*          F-92132 ISSY                                        *  IC2254.2
096900*          FRANCE                                              *  IC2254.2
097000*                                                              *  IC2254.2
097100*                                                              *  IC2254.2
097200*          GMD (GESELLSCHAFT FUR MATHEMATIK                    *  IC2254.2
097300*               UND DATENVERARBEITUNG MBH)                     *  IC2254.2
097400*          SCHLOSS BIRLINGHOVEN                                *  IC2254.2
097500*          POSTFACH 12 40                                      *  IC2254.2
097600*          D-5205 ST. AUGUSTIN 1                               *  IC2254.2
097700*          GERMANY FR                                          *  IC2254.2
097800*                                                              *  IC2254.2
097900*                                                              *  IC2254.2
098000*          NCC (THE NATIONAL COMPUTING CENTRE LTD)             *  IC2254.2
098100*          OXFORD ROAD                                         *  IC2254.2
098200*          MANCHESTER                                          *  IC2254.2
098300*          M1 7ED                                              *  IC2254.2
098400*          UNITED KINGDOM                                      *  IC2254.2
098500*                                                              *  IC2254.2
098600*                                                              *  IC2254.2
098700*    THIS TEST SUITE WAS PRODUCED BY THE NATIONAL COMPUTING    *  IC2254.2
098800*    CENTRE IN ENGLAND AND IS THE OFFICIAL CCVS TEST SUITE     *  IC2254.2
098900*    USED THROUGHOUT EUROPE AND THE UNITED STATES OF AMERICA.  *  IC2254.2
099000*                                                              *  IC2254.2
099100****************************************************************  IC2254.2
099200*                                                              *  IC2254.2
099300*    VALIDATION FOR:-                                          *  IC2254.2
099400*                                                              *  IC2254.2
099500*    "ON-SITE VALIDATION, NATIONAL INSTITUTE OF STD & TECH.     ".IC2254.2
099600*                                                              *  IC2254.2
099700*    "COBOL 85 VERSION 4.2, Apr  1993 SSVG                      ".IC2254.2
099800*                                                              *  IC2254.2
099900****************************************************************  IC2254.2
100000*                                                              *  IC2254.2
100100*      X-CARDS USED BY THIS PROGRAM ARE :-                     *  IC2254.2
100200*                                                              *  IC2254.2
100300*        X-55  - SYSTEM PRINTER NAME.                          *  IC2254.2
100400*        X-82  - SOURCE COMPUTER NAME.                         *  IC2254.2
100500*        X-83  - OBJECT COMPUTER NAME.                         *  IC2254.2
100600*                                                              *  IC2254.2
100700****************************************************************  IC2254.2
100800*                                                              *  IC2254.2
100900*    PROGRAM IC225A AND IC225A-1 WILL TEST THE NEW LANGUAGE    *  IC2254.2
101000*    ELEMENTS FOR THE LEVEL 2 INTER-PROGRAM COMMUNICATION      *  IC2254.2
101100*    MODULE.                                                   *  IC2254.2
101200*    THE NEW LANGUAGE ELEMENTS TO BE TESTED WILL BE:           *  IC2254.2
101300*          "BY REFERENCE"     PHRASE                           *  IC2254.2
101400*    THE TWO PROGRAMS WILL BE COMPILED IN THE SAME FLOW        *  IC2254.2
101500*    (TO TEST THE "END PROGRAM" STATEMENT) AS SHOWN BELOW:     *  IC2254.2
101600*    IDENTIFICATION DIVISION.                                  *  IC2254.2
101700*    PROGRAM-ID. IC225A.                                       *  IC2254.2
101800*              .                                               *  IC2254.2
101900*              .                                               *  IC2254.2
102000*              .                                               *  IC2254.2
102100*    END PROGRAM IC225A.                                       *  IC2254.2
102200*    PROGRAM-ID. IC225A-1.                                     *  IC2254.2
102300*              .                                               *  IC2254.2
102400*              .                                               *  IC2254.2
102500*              .                                               *  IC2254.2
102600****************************************************************  IC2254.2
102700 ENVIRONMENT DIVISION.                                            IC2254.2
102800 CONFIGURATION SECTION.                                           IC2254.2
102900 SOURCE-COMPUTER.                                                 IC2254.2
103000     Linux.                                                       IC2254.2
103100 OBJECT-COMPUTER.                                                 IC2254.2
103200     Linux.                                                       IC2254.2
103300*INPUT-OUTPUT SECTION.                                            IC2254.2
103400 DATA DIVISION.                                                   IC2254.2
103500 FILE SECTION.                                                    IC2254.2
103600 WORKING-STORAGE SECTION.                                         IC2254.2
103700 77  WS1 PICTURE S999.                                            IC2254.2
103800 77  WS2 PICTURE S999                                             IC2254.2
103900         USAGE COMPUTATIONAL, VALUE ZERO.                         IC2254.2
104000 LINKAGE SECTION.                                                 IC2254.2
104100 77  DN1 PICTURE S99.                                             IC2254.2
104200 77  DN2 PICTURE S99 USAGE COMPUTATIONAL.                         IC2254.2
104300 77  DN3 PICTURE S99.                                             IC2254.2
104400 77  DN4 PICTURE S99 USAGE COMPUTATIONAL.                         IC2254.2
104500 PROCEDURE DIVISION USING DN1, DN2, DN3, DN4.                     IC2254.2
104600 SECT-IC225A-1-001 SECTION.                                       IC2254.2
104700 CALL-TEST-001.                                                   IC2254.2
104800     MOVE DN1 TO WS1.                                             IC2254.2
104900     ADD 1 TO WS1.                                                IC2254.2
105000     ADD 1 TO WS2.                                                IC2254.2
105100     MOVE WS1 TO DN3.                                             IC2254.2
105200     MOVE WS2 TO DN4.                                             IC2254.2
105300 CALL-EXIT-001.                                                   IC2254.2
105400     EXIT PROGRAM.                                                IC2254.2

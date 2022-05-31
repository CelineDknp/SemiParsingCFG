038800 IDENTIFICATION DIVISION.                                         IC2264.2
038900 PROGRAM-ID.                                                      IC2264.2
039000     IC226A-1.                                                    IC2264.2
039100****************************************************************  IC2264.2
039200*                                                              *  IC2264.2
039300*    THIS PROGRAM FORMS PART OF THE COBOL COMPILER VALIDATION  *  IC2264.2
039400*    SYSTEM (CCVS) USED TO TEST COBOL COMPILERS FOR            *  IC2264.2
039500*    CONFORMANCE WITH THE AMERICAN NATIONAL STANDARD           *  IC2264.2
039600*    (ANSI DOCUMENT REFERENCE: X3.23-1985) AND THE STANDARD OF *  IC2264.2
039700*    THE INTERNATIONAL ORGANIZATION FOR STANDARDISATION        *  IC2264.2
039800*    (ISO DOCUMENT REFERENCE: ISO-1989-1985).                  *  IC2264.2
039900*                                                              *  IC2264.2
040000*    THIS CCVS INCORPORATES ENHANCEMENTS TO THE CCVS FOR THE   *  IC2264.2
040100*    1974 STANDARD (ANSI DOCUMENT REFERENCE: X3.23-1974; ISO   *  IC2264.2
040200*    DOCUMENT REFERENCE: ISO-1989-1978).                       *  IC2264.2
040300*                                                              *  IC2264.2
040400*    THESE ENHANCEMENTS WERE SPECIFIED BY A PROJECT TEAM WHICH *  IC2264.2
040500*    WAS FUNDED BY THE COMMISSION FOR EUROPEAN COMMUNITIES AND *  IC2264.2
040600*    WHICH WAS RESPONSIBLE FOR TECHNICAL ISSUES TO:            *  IC2264.2
040700*                                                              *  IC2264.2
040800*          THE FEDERAL SOFTWARE TESTING CENTER                 *  IC2264.2
040900*          OFFICE OF SOFTWARE DEVELOPMENT                      *  IC2264.2
041000*                & INFORMATION TECHNOLOGY                      *  IC2264.2
041100*          TWO SKYLINE PLACE                                   *  IC2264.2
041200*          SUITE 1100                                          *  IC2264.2
041300*          5203 LEESBURG PIKE                                  *  IC2264.2
041400*          FALLS CHURCH                                        *  IC2264.2
041500*          VA 22041                                            *  IC2264.2
041600*          U.S.A.                                              *  IC2264.2
041700*                                                              *  IC2264.2
041800*    THE PROJECT TEAM MEMBERS WERE:                            *  IC2264.2
041900*                                                              *  IC2264.2
042000*          BIADI (BUREAU INTER ADMINISTRATION                  *  IC2264.2
042100*                 DE DOCUMENTATION INFORMATIQUE)               *  IC2264.2
042200*          21 RUE BARA                                         *  IC2264.2
042300*          F-92132 ISSY                                        *  IC2264.2
042400*          FRANCE                                              *  IC2264.2
042500*                                                              *  IC2264.2
042600*                                                              *  IC2264.2
042700*          GMD (GESELLSCHAFT FUR MATHEMATIK                    *  IC2264.2
042800*               UND DATENVERARBEITUNG MBH)                     *  IC2264.2
042900*          SCHLOSS BIRLINGHOVEN                                *  IC2264.2
043000*          POSTFACH 12 40                                      *  IC2264.2
043100*          D-5205 ST. AUGUSTIN 1                               *  IC2264.2
043200*          GERMANY FR                                          *  IC2264.2
043300*                                                              *  IC2264.2
043400*                                                              *  IC2264.2
043500*          NCC (THE NATIONAL COMPUTING CENTRE LTD)             *  IC2264.2
043600*          OXFORD ROAD                                         *  IC2264.2
043700*          MANCHESTER                                          *  IC2264.2
043800*          M1 7ED                                              *  IC2264.2
043900*          UNITED KINGDOM                                      *  IC2264.2
044000*                                                              *  IC2264.2
044100*                                                              *  IC2264.2
044200*    THIS TEST SUITE WAS PRODUCED BY THE NATIONAL COMPUTING    *  IC2264.2
044300*    CENTRE IN ENGLAND AND IS THE OFFICIAL CCVS TEST SUITE     *  IC2264.2
044400*    USED THROUGHOUT EUROPE AND THE UNITED STATES OF AMERICA.  *  IC2264.2
044500*                                                              *  IC2264.2
044600****************************************************************  IC2264.2
044700*                                                              *  IC2264.2
044800*    VALIDATION FOR:-                                          *  IC2264.2
044900*                                                              *  IC2264.2
045000*    "ON-SITE VALIDATION, NATIONAL INSTITUTE OF STD & TECH.     ".IC2264.2
045100*                                                              *  IC2264.2
045200*    "COBOL 85 VERSION 4.2, Apr  1993 SSVG                      ".IC2264.2
045300*                                                              *  IC2264.2
045400****************************************************************  IC2264.2
045500*                                                              *  IC2264.2
045600*      X-CARDS USED BY THIS PROGRAM ARE :-                     *  IC2264.2
045700*                                                              *  IC2264.2
045800*        X-14  - SEQUENTIAL MASS STORAGE                       *  IC2264.2
045900*        X-55  - SYSTEM PRINTER NAME.                          *  IC2264.2
046000*        X-82  - SOURCE COMPUTER NAME.                         *  IC2264.2
046100*        X-83  - OBJECT COMPUTER NAME.                         *  IC2264.2
046200*                                                              *  IC2264.2
046300****************************************************************  IC2264.2
046400*                                                              *  IC2264.2
046500*    PROGRAM IC226A AND IC226A-1 WILL TEST THE NEW LANGUAGE    *  IC2264.2
046600*    ELEMENTS FOR THE LEVEL 2 INTER-PROGRAM COMMUNICATION      *  IC2264.2
046700*    MODULE.                                                   *  IC2264.2
046800*    THE NEW LANGUAGE ELEMENTS TO BE TESTED WILL BE:           *  IC2264.2
046900*           THE "EXTERNAL" CLAUSE IN WORKING-STORAGE.          *  IC2264.2
047000*    THE TWO PROGRAMS WILL BE COMPILED IN THE SAME FLOW        *  IC2264.2
047100*    (TO TEST THE "END PROGRAM" STATEMENT) AS SHOWN BELOW:     *  IC2264.2
047200*    IDENTIFICATION DIVISION.                                  *  IC2264.2
047300*    PROGRAM-ID. IC226A.                                       *  IC2264.2
047400*              .                                               *  IC2264.2
047500*              .                                               *  IC2264.2
047600*              .                                               *  IC2264.2
047700*    END PROGRAM IC226A.                                       *  IC2264.2
047800*    PROGRAM-ID. IC226A-1.                                     *  IC2264.2
047900*              .                                               *  IC2264.2
048000*              .                                               *  IC2264.2
048100*              .                                               *  IC2264.2
048200****************************************************************  IC2264.2
048300 ENVIRONMENT DIVISION.                                            IC2264.2
048400 CONFIGURATION SECTION.                                           IC2264.2
048500 SOURCE-COMPUTER.                                                 IC2264.2
048600     Linux.                                                       IC2264.2
048700 OBJECT-COMPUTER.                                                 IC2264.2
048800     Linux.                                                       IC2264.2
048900*INPUT-OUTPUT SECTION.                                            IC2264.2
049000 DATA DIVISION.                                                   IC2264.2
049100 FILE SECTION.                                                    IC2264.2
049200 WORKING-STORAGE SECTION.                                         IC2264.2
049300 01  EXTERNAL-DATA IS EXTERNAL.                                   IC2264.2
049400   03        EXT-DATA-1          PIC X(2).                        IC2264.2
049500   03        EXT-DATA-2          PIC X(6).                        IC2264.2
049600   03        EXT-DATA-3          PIC 9(8).                        IC2264.2
049700   03        EXT-DATA-4          PIC 9(4).                        IC2264.2
049800 PROCEDURE DIVISION.                                              IC2264.2
049900 SECT-IC226A-1-001 SECTION.                                       IC2264.2
050000 EXT-TEST-001.                                                    IC2264.2
050100     MOVE   "ZZ"      TO EXT-DATA-1.                              IC2264.2
050200     MOVE   "CHANGE"  TO EXT-DATA-2.                              IC2264.2
050300     MOVE    87654321 TO EXT-DATA-3.                              IC2264.2
050400     ADD     10       TO EXT-DATA-4.                              IC2264.2
050500 EXT-EXIT-001.                                                    IC2264.2
050600     EXIT PROGRAM.                                                IC2264.2

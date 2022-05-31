032700 IDENTIFICATION DIVISION.                                         IC2374.2
032800 PROGRAM-ID.                                                      IC2374.2
032900     IC237A-1.                                                    IC2374.2
033000****************************************************************  IC2374.2
033100*                                                              *  IC2374.2
033200*    THIS PROGRAM FORMS PART OF THE COBOL COMPILER VALIDATION  *  IC2374.2
033300*    SYSTEM (CCVS) USED TO TEST COBOL COMPILERS FOR            *  IC2374.2
033400*    CONFORMANCE WITH THE AMERICAN NATIONAL STANDARD           *  IC2374.2
033500*    (ANSI DOCUMENT REFERENCE: X3.23-1985) AND THE STANDARD OF *  IC2374.2
033600*    THE INTERNATIONAL ORGANIZATION FOR STANDARDISATION        *  IC2374.2
033700*    (ISO DOCUMENT REFERENCE: ISO-1989-1985).                  *  IC2374.2
033800*                                                              *  IC2374.2
033900*    THIS CCVS INCORPORATES ENHANCEMENTS TO THE CCVS FOR THE   *  IC2374.2
034000*    1974 STANDARD (ANSI DOCUMENT REFERENCE: X3.23-1974; ISO   *  IC2374.2
034100*    DOCUMENT REFERENCE: ISO-1989-1978).                       *  IC2374.2
034200*                                                              *  IC2374.2
034300*    THESE ENHANCEMENTS WERE SPECIFIED BY A PROJECT TEAM WHICH *  IC2374.2
034400*    WAS FUNDED BY THE COMMISSION FOR EUROPEAN COMMUNITIES AND *  IC2374.2
034500*    WHICH WAS RESPONSIBLE FOR TECHNICAL ISSUES TO:            *  IC2374.2
034600*                                                              *  IC2374.2
034700*          THE FEDERAL SOFTWARE TESTING CENTER                 *  IC2374.2
034800*          OFFICE OF SOFTWARE DEVELOPMENT                      *  IC2374.2
034900*                & INFORMATION TECHNOLOGY                      *  IC2374.2
035000*          TWO SKYLINE PLACE                                   *  IC2374.2
035100*          SUITE 1100                                          *  IC2374.2
035200*          5203 LEESBURG PIKE                                  *  IC2374.2
035300*          FALLS CHURCH                                        *  IC2374.2
035400*          VA 22041                                            *  IC2374.2
035500*          U.S.A.                                              *  IC2374.2
035600*                                                              *  IC2374.2
035700*    THE PROJECT TEAM MEMBERS WERE:                            *  IC2374.2
035800*                                                              *  IC2374.2
035900*          BIADI (BUREAU INTER ADMINISTRATION                  *  IC2374.2
036000*                 DE DOCUMENTATION INFORMATIQUE)               *  IC2374.2
036100*          21 RUE BARA                                         *  IC2374.2
036200*          F-92132 ISSY                                        *  IC2374.2
036300*          FRANCE                                              *  IC2374.2
036400*                                                              *  IC2374.2
036500*                                                              *  IC2374.2
036600*          GMD (GESELLSCHAFT FUR MATHEMATIK                    *  IC2374.2
036700*               UND DATENVERARBEITUNG MBH)                     *  IC2374.2
036800*          SCHLOSS BIRLINGHOVEN                                *  IC2374.2
036900*          POSTFACH 12 40                                      *  IC2374.2
037000*          D-5205 ST. AUGUSTIN 1                               *  IC2374.2
037100*          GERMANY FR                                          *  IC2374.2
037200*                                                              *  IC2374.2
037300*                                                              *  IC2374.2
037400*          NCC (THE NATIONAL COMPUTING CENTRE LTD)             *  IC2374.2
037500*          OXFORD ROAD                                         *  IC2374.2
037600*          MANCHESTER                                          *  IC2374.2
037700*          M1 7ED                                              *  IC2374.2
037800*          UNITED KINGDOM                                      *  IC2374.2
037900*                                                              *  IC2374.2
038000*                                                              *  IC2374.2
038100*    THIS TEST SUITE WAS PRODUCED BY THE NATIONAL COMPUTING    *  IC2374.2
038200*    CENTRE IN ENGLAND AND IS THE OFFICIAL CCVS TEST SUITE     *  IC2374.2
038300*    USED THROUGHOUT EUROPE AND THE UNITED STATES OF AMERICA.  *  IC2374.2
038400*                                                              *  IC2374.2
038500****************************************************************  IC2374.2
038600*                                                              *  IC2374.2
038700*    VALIDATION FOR:-                                          *  IC2374.2
038800*                                                              *  IC2374.2
038900*    "ON-SITE VALIDATION, NATIONAL INSTITUTE OF STD & TECH.     ".IC2374.2
039000*                                                              *  IC2374.2
039100*    "COBOL 85 VERSION 4.2, Apr  1993 SSVG                      ".IC2374.2
039200*                                                              *  IC2374.2
039300****************************************************************  IC2374.2
039400*                                                              *  IC2374.2
039500*      X-CARDS USED BY THIS PROGRAM ARE :-                     *  IC2374.2
039600*                                                              *  IC2374.2
039700*        X-55  - SYSTEM PRINTER NAME.                          *  IC2374.2
039800*        X-82  - SOURCE COMPUTER NAME.                         *  IC2374.2
039900*        X-83  - OBJECT COMPUTER NAME.                         *  IC2374.2
040000*                                                              *  IC2374.2
040100****************************************************************  IC2374.2
040200 ENVIRONMENT DIVISION.                                            IC2374.2
040300 CONFIGURATION SECTION.                                           IC2374.2
040400 SOURCE-COMPUTER.                                                 IC2374.2
040500     Linux.                                                       IC2374.2
040600 OBJECT-COMPUTER.                                                 IC2374.2
040700     Linux.                                                       IC2374.2
040800 INPUT-OUTPUT SECTION.                                            IC2374.2
040900 FILE-CONTROL.                                                    IC2374.2
041000     SELECT PRINT-FILE ASSIGN TO                                  IC2374.2
041100     "report.log".                                                IC2374.2
041200 DATA DIVISION.                                                   IC2374.2
041300 FILE SECTION.                                                    IC2374.2
041400 FD  PRINT-FILE.                                                  IC2374.2
041500 01  PRINT-REC PICTURE X(120).                                    IC2374.2
041600 01  DUMMY-RECORD PICTURE X(120).                                 IC2374.2
041700 WORKING-STORAGE SECTION.                                         IC2374.2
041800*                                                                 IC2374.2
041900 LINKAGE SECTION.                                                 IC2374.2
042000 01  L-A                   PIC 9.                                 IC2374.2
042100 01  L-A1 REDEFINES L-A    PIC 9.                                 IC2374.2
042200 01  L-B                   PIC 9.                                 IC2374.2
042300 01  L-C                   PIC 9.                                 IC2374.2
042400 PROCEDURE DIVISION USING L-A L-B L-C.                            IC2374.2
042500*                                                                 IC2374.2
042600 SECT-IC237A-1-001 SECTION.                                       IC2374.2
042700*                                                                 IC2374.2
042800 CALLED-FROM-NC121A-FUNCTION.                                     IC2374.2
042900     MOVE    L-A1 TO L-C.                                         IC2374.2
043000 IC237A-EXIT.                                                     IC2374.2
043100     EXIT PROGRAM.                                                IC2374.2
043200 END-OF-PROGRAM.                                                  IC2374.2
043300 END PROGRAM IC237A-1.                                            IC2374.2

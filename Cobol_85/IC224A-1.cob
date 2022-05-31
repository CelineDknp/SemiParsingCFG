057600 IDENTIFICATION DIVISION.                                         IC2244.2
057700 PROGRAM-ID.                                                      IC2244.2
057800     IC224A-1.                                                    IC2244.2
057900****************************************************************  IC2244.2
058000*                                                              *  IC2244.2
058100*    THIS PROGRAM FORMS PART OF THE COBOL COMPILER VALIDATION  *  IC2244.2
058200*    SYSTEM (CCVS) USED TO TEST COBOL COMPILERS FOR            *  IC2244.2
058300*    CONFORMANCE WITH THE AMERICAN NATIONAL STANDARD           *  IC2244.2
058400*    (ANSI DOCUMENT REFERENCE: X3.23-1985) AND THE STANDARD OF *  IC2244.2
058500*    THE INTERNATIONAL ORGANIZATION FOR STANDARDISATION        *  IC2244.2
058600*    (ISO DOCUMENT REFERENCE: ISO-1989-1985).                  *  IC2244.2
058700*                                                              *  IC2244.2
058800*    THIS CCVS INCORPORATES ENHANCEMENTS TO THE CCVS FOR THE   *  IC2244.2
058900*    1974 STANDARD (ANSI DOCUMENT REFERENCE: X3.23-1974; ISO   *  IC2244.2
059000*    DOCUMENT REFERENCE: ISO-1989-1978).                       *  IC2244.2
059100*                                                              *  IC2244.2
059200*    THESE ENHANCEMENTS WERE SPECIFIED BY A PROJECT TEAM WHICH *  IC2244.2
059300*    WAS FUNDED BY THE COMMISSION FOR EUROPEAN COMMUNITIES AND *  IC2244.2
059400*    WHICH WAS RESPONSIBLE FOR TECHNICAL ISSUES TO:            *  IC2244.2
059500*                                                              *  IC2244.2
059600*          THE FEDERAL SOFTWARE TESTING CENTER                 *  IC2244.2
059700*          OFFICE OF SOFTWARE DEVELOPMENT                      *  IC2244.2
059800*                & INFORMATION TECHNOLOGY                      *  IC2244.2
059900*          TWO SKYLINE PLACE                                   *  IC2244.2
060000*          SUITE 1100                                          *  IC2244.2
060100*          5203 LEESBURG PIKE                                  *  IC2244.2
060200*          FALLS CHURCH                                        *  IC2244.2
060300*          VA 22041                                            *  IC2244.2
060400*          U.S.A.                                              *  IC2244.2
060500*                                                              *  IC2244.2
060600*    THE PROJECT TEAM MEMBERS WERE:                            *  IC2244.2
060700*                                                              *  IC2244.2
060800*          BIADI (BUREAU INTER ADMINISTRATION                  *  IC2244.2
060900*                 DE DOCUMENTATION INFORMATIQUE)               *  IC2244.2
061000*          21 RUE BARA                                         *  IC2244.2
061100*          F-92132 ISSY                                        *  IC2244.2
061200*          FRANCE                                              *  IC2244.2
061300*                                                              *  IC2244.2
061400*                                                              *  IC2244.2
061500*          GMD (GESELLSCHAFT FUR MATHEMATIK                    *  IC2244.2
061600*               UND DATENVERARBEITUNG MBH)                     *  IC2244.2
061700*          SCHLOSS BIRLINGHOVEN                                *  IC2244.2
061800*          POSTFACH 12 40                                      *  IC2244.2
061900*          D-5205 ST. AUGUSTIN 1                               *  IC2244.2
062000*          GERMANY FR                                          *  IC2244.2
062100*                                                              *  IC2244.2
062200*                                                              *  IC2244.2
062300*          NCC (THE NATIONAL COMPUTING CENTRE LTD)             *  IC2244.2
062400*          OXFORD ROAD                                         *  IC2244.2
062500*          MANCHESTER                                          *  IC2244.2
062600*          M1 7ED                                              *  IC2244.2
062700*          UNITED KINGDOM                                      *  IC2244.2
062800*                                                              *  IC2244.2
062900*                                                              *  IC2244.2
063000*    THIS TEST SUITE WAS PRODUCED BY THE NATIONAL COMPUTING    *  IC2244.2
063100*    CENTRE IN ENGLAND AND IS THE OFFICIAL CCVS TEST SUITE     *  IC2244.2
063200*    USED THROUGHOUT EUROPE AND THE UNITED STATES OF AMERICA.  *  IC2244.2
063300*                                                              *  IC2244.2
063400****************************************************************  IC2244.2
063500*                                                              *  IC2244.2
063600*    VALIDATION FOR:-                                          *  IC2244.2
063700*                                                              *  IC2244.2
063800*    "ON-SITE VALIDATION, NATIONAL INSTITUTE OF STD & TECH.     ".IC2244.2
063900*                                                              *  IC2244.2
064000*    "COBOL 85 VERSION 4.2, Apr  1993 SSVG                      ".IC2244.2
064100*                                                              *  IC2244.2
064200****************************************************************  IC2244.2
064300*                                                              *  IC2244.2
064400*      X-CARDS USED BY THIS PROGRAM ARE :-                     *  IC2244.2
064500*                                                              *  IC2244.2
064600*        X-55  - SYSTEM PRINTER NAME.                          *  IC2244.2
064700*        X-82  - SOURCE COMPUTER NAME.                         *  IC2244.2
064800*        X-83  - OBJECT COMPUTER NAME.                         *  IC2244.2
064900*                                                              *  IC2244.2
065000****************************************************************  IC2244.2
065100*                                                              *  IC2244.2
065200*    PROGRAM IC224A AND IC224A-1 WILL TEST THE NEW LANGUAGE    *  IC2244.2
065300*    ELEMENTS FOR THE LEVEL 2 INTER-PROGRAM COMMUNICATION      *  IC2244.2
065400*    MODULE.                                                   *  IC2244.2
065500*    THE NEW LANGUAGE ELEMENTS TO BE TESTED WILL BE:           *  IC2244.2
065600*          "BY CONTENT"       PHRASE                           *  IC2244.2
065700*    THE TWO PROGRAMS WILL BE COMPILED IN THE SAME FLOW        *  IC2244.2
065800*    (TO TEST THE "END PROGRAM" STATEMENT) AS SHOWN BELOW:     *  IC2244.2
065900*    IDENTIFICATION DIVISION.                                  *  IC2244.2
066000*    PROGRAM-ID. IC224A.                                       *  IC2244.2
066100*              .                                               *  IC2244.2
066200*              .                                               *  IC2244.2
066300*              .                                               *  IC2244.2
066400*    END PROGRAM IC224A.                                       *  IC2244.2
066500*    PROGRAM-ID. IC224A-1.                                     *  IC2244.2
066600*              .                                               *  IC2244.2
066700*              .                                               *  IC2244.2
066800*              .                                               *  IC2244.2
066900****************************************************************  IC2244.2
067000 ENVIRONMENT DIVISION.                                            IC2244.2
067100 CONFIGURATION SECTION.                                           IC2244.2
067200 SOURCE-COMPUTER.                                                 IC2244.2
067300     Linux.                                                       IC2244.2
067400 OBJECT-COMPUTER.                                                 IC2244.2
067500     Linux.                                                       IC2244.2
067600 INPUT-OUTPUT SECTION.                                            IC2244.2
067700 FILE-CONTROL.                                                    IC2244.2
067800     SELECT PRINT-FILE ASSIGN TO                                  IC2244.2
067900     "report.log".                                                IC2244.2
068000 DATA DIVISION.                                                   IC2244.2
068100 FILE SECTION.                                                    IC2244.2
068200 FD  PRINT-FILE.                                                  IC2244.2
068300 01  PRINT-REC PICTURE X(120).                                    IC2244.2
068400 01  DUMMY-RECORD PICTURE X(120).                                 IC2244.2
068500 WORKING-STORAGE SECTION.                                         IC2244.2
068600 77  WS1 PICTURE S999.                                            IC2244.2
068700 77  WS2 PICTURE S999                                             IC2244.2
068800         USAGE COMPUTATIONAL, VALUE ZERO.                         IC2244.2
068900 LINKAGE SECTION.                                                 IC2244.2
069000 77  DN1 PICTURE S99.                                             IC2244.2
069100 77  DN2 PICTURE S99 USAGE COMPUTATIONAL.                         IC2244.2
069200 77  DN3 PICTURE S99.                                             IC2244.2
069300 77  DN4 PICTURE S99 USAGE COMPUTATIONAL.                         IC2244.2
069400 PROCEDURE DIVISION USING DN1, DN2, DN3, DN4.                     IC2244.2
069500 SECT-IC224A-1-001 SECTION.                                       IC2244.2
069600 CALL-TEST-001.                                                   IC2244.2
069700     MOVE DN1 TO WS1.                                             IC2244.2
069800     ADD 1 TO WS1.                                                IC2244.2
069900     ADD 1 TO WS2.                                                IC2244.2
070000     MOVE WS1 TO DN3.                                             IC2244.2
070100     MOVE WS2 TO DN4.                                             IC2244.2
070200 CALL-EXIT-001.                                                   IC2244.2
070300     EXIT PROGRAM.                                                IC2244.2

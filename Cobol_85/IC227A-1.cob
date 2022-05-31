096900 IDENTIFICATION DIVISION.                                         IC2274.2
097000 PROGRAM-ID.                                                      IC2274.2
097100     IC227A-1.                                                    IC2274.2
097200****************************************************************  IC2274.2
097300*                                                              *  IC2274.2
097400*    THIS PROGRAM FORMS PART OF THE COBOL COMPILER VALIDATION  *  IC2274.2
097500*    SYSTEM (CCVS) USED TO TEST COBOL COMPILERS FOR            *  IC2274.2
097600*    CONFORMANCE WITH THE AMERICAN NATIONAL STANDARD           *  IC2274.2
097700*    (ANSI DOCUMENT REFERENCE: X3.23-1985) AND THE STANDARD OF *  IC2274.2
097800*    THE INTERNATIONAL ORGANIZATION FOR STANDARDISATION        *  IC2274.2
097900*    (ISO DOCUMENT REFERENCE: ISO-1989-1985).                  *  IC2274.2
098000*                                                              *  IC2274.2
098100*    THIS CCVS INCORPORATES ENHANCEMENTS TO THE CCVS FOR THE   *  IC2274.2
098200*    1974 STANDARD (ANSI DOCUMENT REFERENCE: X3.23-1974; ISO   *  IC2274.2
098300*    DOCUMENT REFERENCE: ISO-1989-1978).                       *  IC2274.2
098400*                                                              *  IC2274.2
098500*    THESE ENHANCEMENTS WERE SPECIFIED BY A PROJECT TEAM WHICH *  IC2274.2
098600*    WAS FUNDED BY THE COMMISSION FOR EUROPEAN COMMUNITIES AND *  IC2274.2
098700*    WHICH WAS RESPONSIBLE FOR TECHNICAL ISSUES TO:            *  IC2274.2
098800*                                                              *  IC2274.2
098900*          THE FEDERAL SOFTWARE TESTING CENTER                 *  IC2274.2
099000*          OFFICE OF SOFTWARE DEVELOPMENT                      *  IC2274.2
099100*                & INFORMATION TECHNOLOGY                      *  IC2274.2
099200*          TWO SKYLINE PLACE                                   *  IC2274.2
099300*          SUITE 1100                                          *  IC2274.2
099400*          5203 LEESBURG PIKE                                  *  IC2274.2
099500*          FALLS CHURCH                                        *  IC2274.2
099600*          VA 22041                                            *  IC2274.2
099700*          U.S.A.                                              *  IC2274.2
099800*                                                              *  IC2274.2
099900*    THE PROJECT TEAM MEMBERS WERE:                            *  IC2274.2
100000*                                                              *  IC2274.2
100100*          BIADI (BUREAU INTER ADMINISTRATION                  *  IC2274.2
100200*                 DE DOCUMENTATION INFORMATIQUE)               *  IC2274.2
100300*          21 RUE BARA                                         *  IC2274.2
100400*          F-92132 ISSY                                        *  IC2274.2
100500*          FRANCE                                              *  IC2274.2
100600*                                                              *  IC2274.2
100700*                                                              *  IC2274.2
100800*          GMD (GESELLSCHAFT FUR MATHEMATIK                    *  IC2274.2
100900*               UND DATENVERARBEITUNG MBH)                     *  IC2274.2
101000*          SCHLOSS BIRLINGHOVEN                                *  IC2274.2
101100*          POSTFACH 12 40                                      *  IC2274.2
101200*          D-5205 ST. AUGUSTIN 1                               *  IC2274.2
101300*          GERMANY FR                                          *  IC2274.2
101400*                                                              *  IC2274.2
101500*                                                              *  IC2274.2
101600*          NCC (THE NATIONAL COMPUTING CENTRE LTD)             *  IC2274.2
101700*          OXFORD ROAD                                         *  IC2274.2
101800*          MANCHESTER                                          *  IC2274.2
101900*          M1 7ED                                              *  IC2274.2
102000*          UNITED KINGDOM                                      *  IC2274.2
102100*                                                              *  IC2274.2
102200*                                                              *  IC2274.2
102300*    THIS TEST SUITE WAS PRODUCED BY THE NATIONAL COMPUTING    *  IC2274.2
102400*    CENTRE IN ENGLAND AND IS THE OFFICIAL CCVS TEST SUITE     *  IC2274.2
102500*    USED THROUGHOUT EUROPE AND THE UNITED STATES OF AMERICA.  *  IC2274.2
102600*                                                              *  IC2274.2
102700*    REVISED 1986 AUGUST                                       *  IC2274.2
102800*                                                              *  IC2274.2
102900****************************************************************  IC2274.2
103000*                                                              *  IC2274.2
103100*    VALIDATION FOR:-                                          *  IC2274.2
103200*                                                              *  IC2274.2
103300*    "ON-SITE VALIDATION, NATIONAL INSTITUTE OF STD & TECH.     ".IC2274.2
103400*                                                              *  IC2274.2
103500*    "COBOL 85 VERSION 4.2, Apr  1993 SSVG                      ".IC2274.2
103600*                                                              *  IC2274.2
103700****************************************************************  IC2274.2
103800*                                                              *  IC2274.2
103900*      X-CARDS USED BY THIS PROGRAM ARE :-                     *  IC2274.2
104000*                                                              *  IC2274.2
104100*            X-82   SOURCE-COMPUTER                            *  IC2274.2
104200*            X-83   OBJECT-COMPUTER.                           *  IC2274.2
104300*                                                              *  IC2274.2
104400****************************************************************  IC2274.2
104500*                                                              *  IC2274.2
104600*    PROGRAMS IC227A AND IC227A-1 TEST LEVEL 2 LANGUAGE        *  IC2274.2
104700*    ELEMENTS FROM THE INTER-PROGRAM COMMUNICATION MODULE.     *  IC2274.2
104800*    THE PARTICULAR ELEMENTS TESTED ARE:                       *  IC2274.2
104900*        THE "EXTERNAL" CLAUSE IN THE FILE DESCRIPTION ENTRY   *  IC2274.2
105000*                                                              *  IC2274.2
105100*    ALTHOUGH IC227A AND IC227A-1 ARE SEPARATELY COMPILED      *  IC2274.2
105200*    PROGRAMS, BOTH ARE INTENDED TO BE COMPILED BY THE SAME    *  IC2274.2
105300*    INVOCATION OF THE COMPILER, IN ORDER TO TEST STREAM       *  IC2274.2
105400*    COMPILATION AND RECOGNITION OF THE END PROGRAM HEADER.    *  IC2274.2
105500*                                                              *  IC2274.2
105600*    THE STRUCTURE OF THE SOURCE FILE IS:                      *  IC2274.2
105700*                                                              *  IC2274.2
105800*    IDENTIFICATION DIVISION.                                  *  IC2274.2
105900*    PROGRAM-ID.  IC227A.                                      *  IC2274.2
106000*              .                                               *  IC2274.2
106100*              .                                               *  IC2274.2
106200*              .                                               *  IC2274.2
106300*    END PROGRAM IC227A.                                       *  IC2274.2
106400*    IDENTIFICATION DIVISION.                                  *  IC2274.2
106500*    PROGRAM-ID.  IC227A-1.                                    *  IC2274.2
106600*              .                                               *  IC2274.2
106700*              .                                               *  IC2274.2
106800*              .                                               *  IC2274.2
106900*    END PROGRAM IC227A-1.                                     *  IC2274.2
107000*                                                              *  IC2274.2
107100****************************************************************  IC2274.2
107200*                                                                 IC2274.2
107300 ENVIRONMENT DIVISION.                                            IC2274.2
107400 CONFIGURATION SECTION.                                           IC2274.2
107500 SOURCE-COMPUTER.                                                 IC2274.2
107600     Linux.                                                       IC2274.2
107700 OBJECT-COMPUTER.                                                 IC2274.2
107800     Linux.                                                       IC2274.2
107900*                                                                 IC2274.2
108000 INPUT-OUTPUT SECTION.                                            IC2274.2
108100 FILE-CONTROL.                                                    IC2274.2
108200     SELECT EXTERNAL-FILE ASSIGN TO                               IC2274.2
108300     "XXXXX014"                                                   IC2274.2
108400     FILE STATUS IS LINKAGE-FS.                                   IC2274.2
108500*                                                                 IC2274.2
108600 DATA DIVISION.                                                   IC2274.2
108700 FILE SECTION.                                                    IC2274.2
108800 FD  EXTERNAL-FILE                                                IC2274.2
108900         IS EXTERNAL                                              IC2274.2
109000         RECORD CONTAINS 18 CHARACTERS.                           IC2274.2
109100 01  EXTERNAL-FILE-RECORD.                                        IC2274.2
109200     03  EXT-DATA-1              PIC X(2).                        IC2274.2
109300     03  EXT-DATA-2              PIC X(6).                        IC2274.2
109400     03  EXT-DATA-3              PIC 9(6).                        IC2274.2
109500     03  EXT-DATA-4              PIC 9(4).                        IC2274.2
109600*                                                                 IC2274.2
109700 WORKING-STORAGE SECTION.                                         IC2274.2
109800*                                                                 IC2274.2
109900***************************************************************   IC2274.2
110000*                                                             *   IC2274.2
110100*    WORKING-STORAGE DATA ITEMS SPECIFIC TO THIS TEST SUITE   *   IC2274.2
110200*                                                             *   IC2274.2
110300***************************************************************   IC2274.2
110400*                                                                 IC2274.2
110500 01  EXTERNAL-RECORD-WORK.                                        IC2274.2
110600     03  WRK-DATA-1              PIC X(2).                        IC2274.2
110700     03  WRK-DATA-2              PIC X(6).                        IC2274.2
110800     03  WRK-DATA-3              PIC 9(6).                        IC2274.2
110900     03  WRK-DATA-4              PIC 9(4).                        IC2274.2
111000*                                                                 IC2274.2
111100 LINKAGE SECTION.                                                 IC2274.2
111200*                                                                 IC2274.2
111300 01  LINKAGE-RECORD-WORK.                                         IC2274.2
111400     05  WRK-DATA-1              PIC X(2).                        IC2274.2
111500     05  WRK-DATA-2              PIC X(6).                        IC2274.2
111600     05  WRK-DATA-3              PIC 9(6).                        IC2274.2
111700     05  WRK-DATA-4              PIC 9(4).                        IC2274.2
111800*                                                                 IC2274.2
111900 01  LINKAGE-FS                  PIC XX.                          IC2274.2
112000 01  ACTION-CODE                 PIC 99.                          IC2274.2
112100*                                                                 IC2274.2
112200*                                                                 IC2274.2
112300 PROCEDURE DIVISION USING ACTION-CODE                             IC2274.2
112400                          LINKAGE-RECORD-WORK                     IC2274.2
112500                          LINKAGE-FS.                             IC2274.2
112600*                                                                 IC2274.2
112700 SECT-IC227A-1-01 SECTION.                                        IC2274.2
112800 EXT-DECODE-01.                                                   IC2274.2
112900*                                                                 IC2274.2
113000*    *************************************************            IC2274.2
113100*    *                                               *            IC2274.2
113200*    *    USE THE ACTION CODE PARAMETER TO IDENTIFY  *            IC2274.2
113300*    *    THE FUNCTION REQUIRED ON THIS ENTRY.       *            IC2274.2
113400*    *                                               *            IC2274.2
113500*    *************************************************            IC2274.2
113600*                                                                 IC2274.2
113700     GO TO   SUBPROGRAM-FUNCTION-01                               IC2274.2
113800             SUBPROGRAM-FUNCTION-02                               IC2274.2
113900             SUBPROGRAM-FUNCTION-03                               IC2274.2
114000             SUBPROGRAM-FUNCTION-04                               IC2274.2
114100             SUBPROGRAM-FUNCTION-05                               IC2274.2
114200                 DEPENDING ON ACTION-CODE.                        IC2274.2
114300*                                                                 IC2274.2
114400*    CONTROL SHOULD NEVER REACH HERE, BUT ...                     IC2274.2
114500*                                                                 IC2274.2
114600     MOVE   "FFFFFFFFFFFFFFFFFF" TO LINKAGE-RECORD-WORK           IC2274.2
114700     MOVE   "FF"                 TO LINKAGE-FS                    IC2274.2
114800     EXIT PROGRAM.                                                IC2274.2
114900*                                                                 IC2274.2
115000*                                                                 IC2274.2
115100 SUBPROGRAM-FUNCTION-01.                                          IC2274.2
115200     MOVE    EXTERNAL-FILE-RECORD TO EXTERNAL-RECORD-WORK         IC2274.2
115300     MOVE    LINKAGE-RECORD-WORK  TO EXTERNAL-FILE-RECORD         IC2274.2
115400     MOVE    EXTERNAL-RECORD-WORK TO LINKAGE-RECORD-WORK.         IC2274.2
115500     MOVE   "XX"                  TO LINKAGE-FS.                  IC2274.2
115600     EXIT PROGRAM.                                                IC2274.2
115700*                                                                 IC2274.2
115800*                                                                 IC2274.2
115900 SUBPROGRAM-FUNCTION-02.                                          IC2274.2
116000*                                                                 IC2274.2
116100*        WRITE A RECORD TO THE EXTERNAL FILE                      IC2274.2
116200*                                                                 IC2274.2
116300     MOVE    LINKAGE-RECORD-WORK TO EXTERNAL-FILE-RECORD.         IC2274.2
116400     WRITE   EXTERNAL-FILE-RECORD.                                IC2274.2
116500     EXIT    PROGRAM.                                             IC2274.2
116600*                                                                 IC2274.2
116700*                                                                 IC2274.2
116800 SUBPROGRAM-FUNCTION-03.                                          IC2274.2
116900*                                                                 IC2274.2
117000*        CLOSE THE EXTERNAL FILE                                  IC2274.2
117100*                                                                 IC2274.2
117200     CLOSE   EXTERNAL-FILE.                                       IC2274.2
117300     EXIT    PROGRAM.                                             IC2274.2
117400*                                                                 IC2274.2
117500*                                                                 IC2274.2
117600 SUBPROGRAM-FUNCTION-04.                                          IC2274.2
117700*                                                                 IC2274.2
117800*        OPEN THE EXTERNAL FILE FOR INPUT                         IC2274.2
117900*                                                                 IC2274.2
118000     OPEN    INPUT EXTERNAL-FILE.                                 IC2274.2
118100     MOVE   "OPEN   OPEN   OPEN"  TO EXTERNAL-FILE-RECORD.        IC2274.2
118200     MOVE    EXTERNAL-FILE-RECORD TO LINKAGE-RECORD-WORK.         IC2274.2
118300     EXIT    PROGRAM.                                             IC2274.2
118400*                                                                 IC2274.2
118500*                                                                 IC2274.2
118600 SUBPROGRAM-FUNCTION-05.                                          IC2274.2
118700*                                                                 IC2274.2
118800*        READ A RECORD FROM THE EXTERNAL FILE                     IC2274.2
118900*                                                                 IC2274.2
119000     READ    EXTERNAL-FILE                                        IC2274.2
119100                AT END GO TO SUBPROGRAM-FUNCTION-05-EOF.          IC2274.2
119200     MOVE    EXTERNAL-FILE-RECORD TO LINKAGE-RECORD-WORK.         IC2274.2
119300     EXIT    PROGRAM.                                             IC2274.2
119400*                                                                 IC2274.2
119500 SUBPROGRAM-FUNCTION-05-EOF.                                      IC2274.2
119600     MOVE    EXTERNAL-FILE-RECORD TO LINKAGE-RECORD-WORK.         IC2274.2
119700     MOVE   "END-FILE  END-FILE"  TO EXTERNAL-FILE-RECORD.        IC2274.2
119800     EXIT    PROGRAM.                                             IC2274.2
119900*                                                                 IC2274.2
120000 END PROGRAM IC227A-1.                                            IC2274.2

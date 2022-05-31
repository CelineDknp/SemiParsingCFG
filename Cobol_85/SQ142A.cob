000100 IDENTIFICATION DIVISION.                                         SQ1424.2
000200 PROGRAM-ID.                                                      SQ1424.2
000300     SQ142A.                                                      SQ1424.2
000400****************************************************************  SQ1424.2
000500*                                                              *  SQ1424.2
000600*    VALIDATION FOR:-                                          *  SQ1424.2
000700*    "ON-SITE VALIDATION, NATIONAL INSTITUTE OF STD & TECH.     ".SQ1424.2
000800*    USING CCVS85 VERSION 1.0 ISSUED IN JANUARY 1986.          *  SQ1424.2
000900*                             REVISED 1986, AUGUST             *  SQ1424.2
001000*                                                              *  SQ1424.2
001100*    CREATION DATE     /     VALIDATION DATE                   *  SQ1424.2
001200*    "COBOL 85 VERSION 4.2, Apr  1993 SSVG                      ".SQ1424.2
001300*                                                              *  SQ1424.2
001400****************************************************************  SQ1424.2
001500*                                                              *  SQ1424.2
001600*      X-CARDS USED BY THIS PROGRAM ARE :-                     *  SQ1424.2
001700*                                                              *  SQ1424.2
001800*            X-01   SEQUENTIAL MAGNETIC TAPE FILE.             *  SQ1424.2
001900*            X-55   SYSTEM PRINTER                             *  SQ1424.2
002000*            X-82   SOURCE-COMPUTER                            *  SQ1424.2
002100*            X-83   OBJECT-COMPUTER.                           *  SQ1424.2
002200*                                                              *  SQ1424.2
002300*                                                              *  SQ1424.2
002400****************************************************************  SQ1424.2
002500*                                                              *  SQ1424.2
002600*    SPLIT FROM SQ129A, THIS PROGRAM REPEATS THE SEQUENCE OF   *  SQ1424.2
002700*    FILE HANDLING ROUTINES IN ORDER TO CARRY OUT THE ISOLATED *  SQ1424.2
002800*    SPLIT TEST THAT CHECKS FOR THE CORRECT RESPONSE TO AN     *  SQ1424.2
002900*    OPEN FOR INPUT ON A TAPE FILE WHICH IS NOT PRESENT.       *  SQ1424.2
003000*    (SEE SQ129A).                                             *  SQ1424.2
003100*                                                              *  SQ1424.2
003200****************************************************************  SQ1424.2
003300*                                                                 SQ1424.2
003400 ENVIRONMENT DIVISION.                                            SQ1424.2
003500 CONFIGURATION SECTION.                                           SQ1424.2
003600 SOURCE-COMPUTER.                                                 SQ1424.2
003700     Linux.                                                       SQ1424.2
003800 OBJECT-COMPUTER.                                                 SQ1424.2
003900     Linux.                                                       SQ1424.2
004000*                                                                 SQ1424.2
004100 INPUT-OUTPUT SECTION.                                            SQ1424.2
004200 FILE-CONTROL.                                                    SQ1424.2
004300     SELECT PRINT-FILE ASSIGN TO                                  SQ1424.2
004400     "report.log".                                                SQ1424.2
004500*                                                                 SQ1424.2
004600*P   SELECT RAW-DATA   ASSIGN TO                                  SQ1424.2
004700*P   "XXXXX062"                                                   SQ1424.2
004800*P         ORGANIZATION IS INDEXED                                SQ1424.2
004900*P         ACCESS MODE  IS RANDOM                                 SQ1424.2
005000*P         RECORD-KEY   IS RAW-DATA-KEY.                          SQ1424.2
005100*P                                                                SQ1424.2
005200     SELECT SQ-FS1 ASSIGN TO                                      SQ1424.2
005300     "XXXXX001"                                                   SQ1424.2
005400            FILE STATUS IS SQ-FS1-STATUS.                         SQ1424.2
005500*                                                                 SQ1424.2
005600*                                                                 SQ1424.2
005700 DATA DIVISION.                                                   SQ1424.2
005800 FILE SECTION.                                                    SQ1424.2
005900 FD  PRINT-FILE                                                   SQ1424.2
006000*C   LABEL RECORDS                                                SQ1424.2
006100*C       OMITTED                                                  SQ1424.2
006200*C   DATA RECORD IS PRINT-REC DUMMY-RECORD                        SQ1424.2
006300               .                                                  SQ1424.2
006400 01  PRINT-REC    PICTURE X(120).                                 SQ1424.2
006500 01  DUMMY-RECORD PICTURE X(120).                                 SQ1424.2
006600*P                                                                SQ1424.2
006700*PD  RAW-DATA.                                                    SQ1424.2
006800*P1  RAW-DATA-SATZ.                                               SQ1424.2
006900*P   05  RAW-DATA-KEY        PIC X(6).                            SQ1424.2
007000*P   05  C-DATE              PIC 9(6).                            SQ1424.2
007100*P   05  C-TIME              PIC 9(8).                            SQ1424.2
007200*P   05  NO-OF-TESTS         PIC 99.                              SQ1424.2
007300*P   05  C-OK                PIC 999.                             SQ1424.2
007400*P   05  C-ALL               PIC 999.                             SQ1424.2
007500*P   05  C-FAIL              PIC 999.                             SQ1424.2
007600*P   05  C-DELETED           PIC 999.                             SQ1424.2
007700*P   05  C-INSPECT           PIC 999.                             SQ1424.2
007800*P   05  C-NOTE              PIC X(13).                           SQ1424.2
007900*P   05  C-INDENT            PIC X.                               SQ1424.2
008000*P   05  C-ABORT             PIC X(8).                            SQ1424.2
008100*                                                                 SQ1424.2
008200 FD  SQ-FS1                                                       SQ1424.2
008300*C   LABEL RECORD IS STANDARD                                     SQ1424.2
008400                .                                                 SQ1424.2
008500 01  SQ-FS1R1-F-G-120 PIC X(120).                                 SQ1424.2
008600*                                                                 SQ1424.2
008700 WORKING-STORAGE SECTION.                                         SQ1424.2
008800*                                                                 SQ1424.2
008900***************************************************************   SQ1424.2
009000*                                                             *   SQ1424.2
009100*    WORKING-STORAGE DATA ITEMS SPECIFIC TO THIS TEST SUITE   *   SQ1424.2
009200*                                                             *   SQ1424.2
009300***************************************************************   SQ1424.2
009400*                                                                 SQ1424.2
009500 01  SQ-FS1-STATUS.                                               SQ1424.2
009600   03  SQ-FS1-KEY-1   PIC X.                                      SQ1424.2
009700   03  SQ-FS1-KEY-2   PIC X.                                      SQ1424.2
009800*                                                                 SQ1424.2
009900 01  DECL-EXEC-SW  PIC 9.                                         SQ1424.2
010000*                                                                 SQ1424.2
010100***************************************************************   SQ1424.2
010200*                                                             *   SQ1424.2
010300*    WORKING-STORAGE DATA ITEMS USED BY THE CCVS              *   SQ1424.2
010400*                                                             *   SQ1424.2
010500***************************************************************   SQ1424.2
010600*                                                                 SQ1424.2
010700 01  REC-SKEL-SUB   PIC 99.                                       SQ1424.2
010800*                                                                 SQ1424.2
010900 01  FILE-RECORD-INFORMATION-REC.                                 SQ1424.2
011000     03 FILE-RECORD-INFO-SKELETON.                                SQ1424.2
011100        05 FILLER                 PICTURE X(48)       VALUE       SQ1424.2
011200             "FILE=      ,RECORD=      /0,RECNO=000000,UPDT=00".  SQ1424.2
011300        05 FILLER                 PICTURE X(46)       VALUE       SQ1424.2
011400             ",ODO=0000,PGM=     ,LRECL=000000,BLKSIZ  =0000".    SQ1424.2
011500        05 FILLER                 PICTURE X(26)       VALUE       SQ1424.2
011600             ",LFIL=000000,ORG=  ,LBLR= ".                        SQ1424.2
011700        05 FILLER                 PICTURE X(37)       VALUE       SQ1424.2
011800             ",RECKEY=                             ".             SQ1424.2
011900        05 FILLER                 PICTURE X(38)       VALUE       SQ1424.2
012000             ",ALTKEY1=                             ".            SQ1424.2
012100        05 FILLER                 PICTURE X(38)       VALUE       SQ1424.2
012200             ",ALTKEY2=                             ".            SQ1424.2
012300        05 FILLER                 PICTURE X(7)        VALUE SPACE.SQ1424.2
012400     03 FILE-RECORD-INFO          OCCURS  10  TIMES.              SQ1424.2
012500        05 FILE-RECORD-INFO-P1-120.                               SQ1424.2
012600           07 FILLER              PIC X(5).                       SQ1424.2
012700           07 XFILE-NAME          PIC X(6).                       SQ1424.2
012800           07 FILLER              PIC X(8).                       SQ1424.2
012900           07 XRECORD-NAME        PIC X(6).                       SQ1424.2
013000           07 FILLER              PIC X(1).                       SQ1424.2
013100           07 REELUNIT-NUMBER     PIC 9(1).                       SQ1424.2
013200           07 FILLER              PIC X(7).                       SQ1424.2
013300           07 XRECORD-NUMBER      PIC 9(6).                       SQ1424.2
013400           07 FILLER              PIC X(6).                       SQ1424.2
013500           07 UPDATE-NUMBER       PIC 9(2).                       SQ1424.2
013600           07 FILLER              PIC X(5).                       SQ1424.2
013700           07 ODO-NUMBER          PIC 9(4).                       SQ1424.2
013800           07 FILLER              PIC X(5).                       SQ1424.2
013900           07 XPROGRAM-NAME       PIC X(5).                       SQ1424.2
014000           07 FILLER              PIC X(7).                       SQ1424.2
014100           07 XRECORD-LENGTH      PIC 9(6).                       SQ1424.2
014200           07 FILLER              PIC X(7).                       SQ1424.2
014300           07 CHARS-OR-RECORDS    PIC X(2).                       SQ1424.2
014400           07 FILLER              PIC X(1).                       SQ1424.2
014500           07 XBLOCK-SIZE         PIC 9(4).                       SQ1424.2
014600           07 FILLER              PIC X(6).                       SQ1424.2
014700           07 RECORDS-IN-FILE     PIC 9(6).                       SQ1424.2
014800           07 FILLER              PIC X(5).                       SQ1424.2
014900           07 XFILE-ORGANIZATION  PIC X(2).                       SQ1424.2
015000           07 FILLER              PIC X(6).                       SQ1424.2
015100           07 XLABEL-TYPE         PIC X(1).                       SQ1424.2
015200        05 FILE-RECORD-INFO-P121-240.                             SQ1424.2
015300           07 FILLER              PIC X(8).                       SQ1424.2
015400           07 XRECORD-KEY         PIC X(29).                      SQ1424.2
015500           07 FILLER              PIC X(9).                       SQ1424.2
015600           07 ALTERNATE-KEY1      PIC X(29).                      SQ1424.2
015700           07 FILLER              PIC X(9).                       SQ1424.2
015800           07 ALTERNATE-KEY2      PIC X(29).                      SQ1424.2
015900           07 FILLER              PIC X(7).                       SQ1424.2
016000*                                                                 SQ1424.2
016100 01  TEST-RESULTS.                                                SQ1424.2
016200     02 FILLER              PIC X      VALUE SPACE.               SQ1424.2
016300     02 FEATURE             PIC X(24)  VALUE SPACE.               SQ1424.2
016400     02 FILLER              PIC X      VALUE SPACE.               SQ1424.2
016500     02 P-OR-F              PIC X(5)   VALUE SPACE.               SQ1424.2
016600     02 FILLER              PIC X      VALUE SPACE.               SQ1424.2
016700     02  PAR-NAME.                                                SQ1424.2
016800       03 FILLER              PIC X(14)  VALUE SPACE.             SQ1424.2
016900       03 PARDOT-X            PIC X      VALUE SPACE.             SQ1424.2
017000       03 DOTVALUE            PIC 99     VALUE ZERO.              SQ1424.2
017100     02 FILLER              PIC X(9)   VALUE SPACE.               SQ1424.2
017200     02 RE-MARK             PIC X(61).                            SQ1424.2
017300 01  TEST-COMPUTED.                                               SQ1424.2
017400   02 FILLER  PIC X(30)  VALUE SPACE.                             SQ1424.2
017500   02 FILLER  PIC X(17)  VALUE "      COMPUTED =".                SQ1424.2
017600   02 COMPUTED-X.                                                 SQ1424.2
017700     03 COMPUTED-A    PIC X(20)  VALUE SPACE.                     SQ1424.2
017800     03 COMPUTED-N    REDEFINES COMPUTED-A PIC -9(9).9(9).        SQ1424.2
017900     03 COMPUTED-0V18 REDEFINES COMPUTED-A PIC -.9(18).           SQ1424.2
018000     03 COMPUTED-4V14 REDEFINES COMPUTED-A PIC -9(4).9(14).       SQ1424.2
018100     03 COMPUTED-14V4 REDEFINES COMPUTED-A PIC -9(14).9(4).       SQ1424.2
018200     03       CM-18V0 REDEFINES COMPUTED-A.                       SQ1424.2
018300        04 COMPUTED-18V0                   PIC -9(18).            SQ1424.2
018400        04 FILLER                          PIC X.                 SQ1424.2
018500     03 FILLER PIC X(50) VALUE SPACE.                             SQ1424.2
018600 01  TEST-CORRECT.                                                SQ1424.2
018700     02 FILLER PIC X(30) VALUE SPACE.                             SQ1424.2
018800     02 FILLER PIC X(17) VALUE "       CORRECT =".                SQ1424.2
018900     02 CORRECT-X.                                                SQ1424.2
019000     03 CORRECT-A                  PIC X(20) VALUE SPACE.         SQ1424.2
019100     03 CORRECT-N    REDEFINES CORRECT-A     PIC -9(9).9(9).      SQ1424.2
019200     03 CORRECT-0V18 REDEFINES CORRECT-A     PIC -.9(18).         SQ1424.2
019300     03 CORRECT-4V14 REDEFINES CORRECT-A     PIC -9(4).9(14).     SQ1424.2
019400     03 CORRECT-14V4 REDEFINES CORRECT-A     PIC -9(14).9(4).     SQ1424.2
019500     03      CR-18V0 REDEFINES CORRECT-A.                         SQ1424.2
019600         04 CORRECT-18V0                     PIC -9(18).          SQ1424.2
019700         04 FILLER                           PIC X.               SQ1424.2
019800     03 FILLER PIC X(2) VALUE SPACE.                              SQ1424.2
019900     03 COR-ANSI-REFERENCE             PIC X(48) VALUE SPACE.     SQ1424.2
020000 01  CCVS-C-1.                                                    SQ1424.2
020100     02 FILLER  PIC IS X(4)     VALUE SPACE.                      SQ1424.2
020200     02 FILLER  PIC IS X(98)    VALUE IS "FEATURE               PASQ1424.2
020300-    "SS  PARAGRAPH-NAME                                          SQ1424.2
020400-    "       REMARKS".                                            SQ1424.2
020500     02 FILLER           PIC X(17)    VALUE SPACE.                SQ1424.2
020600 01  CCVS-C-2.                                                    SQ1424.2
020700     02 FILLER           PIC XXXX     VALUE SPACE.                SQ1424.2
020800     02 FILLER           PIC X(6)     VALUE "TESTED".             SQ1424.2
020900     02 FILLER           PIC X(16)    VALUE SPACE.                SQ1424.2
021000     02 FILLER           PIC X(4)     VALUE "FAIL".               SQ1424.2
021100     02 FILLER           PIC X(90)    VALUE SPACE.                SQ1424.2
021200 01  REC-SKL-SUB       PIC 9(2)     VALUE ZERO.                   SQ1424.2
021300 01  REC-CT            PIC 99       VALUE ZERO.                   SQ1424.2
021400 01  DELETE-COUNTER    PIC 999      VALUE ZERO.                   SQ1424.2
021500 01  ERROR-COUNTER     PIC 999      VALUE ZERO.                   SQ1424.2
021600 01  INSPECT-COUNTER   PIC 999      VALUE ZERO.                   SQ1424.2
021700 01  PASS-COUNTER      PIC 999      VALUE ZERO.                   SQ1424.2
021800 01  TOTAL-ERROR       PIC 999      VALUE ZERO.                   SQ1424.2
021900 01  ERROR-HOLD        PIC 999      VALUE ZERO.                   SQ1424.2
022000 01  DUMMY-HOLD        PIC X(120)   VALUE SPACE.                  SQ1424.2
022100 01  RECORD-COUNT      PIC 9(5)     VALUE ZERO.                   SQ1424.2
022200 01  ANSI-REFERENCE    PIC X(48)    VALUE SPACES.                 SQ1424.2
022300 01  CCVS-H-1.                                                    SQ1424.2
022400     02  FILLER          PIC X(39)    VALUE SPACES.               SQ1424.2
022500     02  FILLER          PIC X(42)    VALUE                       SQ1424.2
022600     "OFFICIAL COBOL COMPILER VALIDATION SYSTEM".                 SQ1424.2
022700     02  FILLER          PIC X(39)    VALUE SPACES.               SQ1424.2
022800 01  CCVS-H-2A.                                                   SQ1424.2
022900   02  FILLER            PIC X(40)  VALUE SPACE.                  SQ1424.2
023000   02  FILLER            PIC X(7)   VALUE "CCVS85 ".              SQ1424.2
023100   02  FILLER            PIC XXXX   VALUE                         SQ1424.2
023200     "4.2 ".                                                      SQ1424.2
023300   02  FILLER            PIC X(28)  VALUE                         SQ1424.2
023400            " COPY - NOT FOR DISTRIBUTION".                       SQ1424.2
023500   02  FILLER            PIC X(41)  VALUE SPACE.                  SQ1424.2
023600*                                                                 SQ1424.2
023700 01  CCVS-H-2B.                                                   SQ1424.2
023800   02  FILLER            PIC X(15)  VALUE "TEST RESULT OF ".      SQ1424.2
023900   02  TEST-ID           PIC X(9).                                SQ1424.2
024000   02  FILLER            PIC X(4)   VALUE " IN ".                 SQ1424.2
024100   02  FILLER            PIC X(12)  VALUE                         SQ1424.2
024200     " HIGH       ".                                              SQ1424.2
024300   02  FILLER            PIC X(22)  VALUE                         SQ1424.2
024400            " LEVEL VALIDATION FOR ".                             SQ1424.2
024500   02  FILLER            PIC X(58)  VALUE                         SQ1424.2
024600     "ON-SITE VALIDATION, NATIONAL INSTITUTE OF STD & TECH.     ".SQ1424.2
024700 01  CCVS-H-3.                                                    SQ1424.2
024800     02  FILLER          PIC X(34)  VALUE                         SQ1424.2
024900            " FOR OFFICIAL USE ONLY    ".                         SQ1424.2
025000     02  FILLER          PIC X(58)  VALUE                         SQ1424.2
025100     "COBOL 85 VERSION 4.2, Apr  1993 SSVG                      ".SQ1424.2
025200     02  FILLER          PIC X(28)  VALUE                         SQ1424.2
025300            "  COPYRIGHT   1985,1986 ".                           SQ1424.2
025400 01  CCVS-E-1.                                                    SQ1424.2
025500     02 FILLER           PIC X(52)  VALUE SPACE.                  SQ1424.2
025600     02 FILLER  PIC X(14) VALUE IS "END OF TEST-  ".              SQ1424.2
025700     02 ID-AGAIN         PIC X(9).                                SQ1424.2
025800     02 FILLER           PIC X(45)  VALUE SPACES.                 SQ1424.2
025900 01  CCVS-E-2.                                                    SQ1424.2
026000     02  FILLER          PIC X(31)  VALUE SPACE.                  SQ1424.2
026100     02  FILLER          PIC X(21)  VALUE SPACE.                  SQ1424.2
026200     02  CCVS-E-2-2.                                              SQ1424.2
026300         03 ERROR-TOTAL    PIC XXX    VALUE SPACE.                SQ1424.2
026400         03 FILLER         PIC X      VALUE SPACE.                SQ1424.2
026500         03 ENDER-DESC     PIC X(44)  VALUE                       SQ1424.2
026600            "ERRORS ENCOUNTERED".                                 SQ1424.2
026700 01  CCVS-E-3.                                                    SQ1424.2
026800     02  FILLER          PIC X(22)  VALUE                         SQ1424.2
026900            " FOR OFFICIAL USE ONLY".                             SQ1424.2
027000     02  FILLER          PIC X(12)  VALUE SPACE.                  SQ1424.2
027100     02  FILLER          PIC X(58)  VALUE                         SQ1424.2
027200     "ON-SITE VALIDATION, NATIONAL INSTITUTE OF STD & TECH.     ".SQ1424.2
027300     02  FILLER          PIC X(8)   VALUE SPACE.                  SQ1424.2
027400     02  FILLER          PIC X(20)  VALUE                         SQ1424.2
027500             " COPYRIGHT 1985,1986".                              SQ1424.2
027600 01  CCVS-E-4.                                                    SQ1424.2
027700     02 CCVS-E-4-1       PIC XXX    VALUE SPACE.                  SQ1424.2
027800     02 FILLER           PIC X(4)   VALUE " OF ".                 SQ1424.2
027900     02 CCVS-E-4-2       PIC XXX    VALUE SPACE.                  SQ1424.2
028000     02 FILLER           PIC X(40)  VALUE                         SQ1424.2
028100      "  TESTS WERE EXECUTED SUCCESSFULLY".                       SQ1424.2
028200 01  XXINFO.                                                      SQ1424.2
028300     02 FILLER           PIC X(19)  VALUE "*** INFORMATION ***".  SQ1424.2
028400     02 INFO-TEXT.                                                SQ1424.2
028500       04 FILLER             PIC X(8)   VALUE SPACE.              SQ1424.2
028600       04 XXCOMPUTED         PIC X(20).                           SQ1424.2
028700       04 FILLER             PIC X(5)   VALUE SPACE.              SQ1424.2
028800       04 XXCORRECT          PIC X(20).                           SQ1424.2
028900     02 INF-ANSI-REFERENCE PIC X(48).                             SQ1424.2
029000 01  HYPHEN-LINE.                                                 SQ1424.2
029100     02 FILLER  PIC IS X VALUE IS SPACE.                          SQ1424.2
029200     02 FILLER  PIC IS X(65)    VALUE IS "************************SQ1424.2
029300-    "*****************************************".                 SQ1424.2
029400     02 FILLER  PIC IS X(54)    VALUE IS "************************SQ1424.2
029500-    "******************************".                            SQ1424.2
029600 01  CCVS-PGM-ID  PIC X(9)   VALUE                                SQ1424.2
029700     "SQ142A".                                                    SQ1424.2
029800*                                                                 SQ1424.2
029900*                                                                 SQ1424.2
030000 PROCEDURE DIVISION.                                              SQ1424.2
030100 DECLARATIVES.                                                    SQ1424.2
030200 SQ142A-DECLARATIVE-001-SECT SECTION.                             SQ1424.2
030300     USE AFTER STANDARD EXCEPTION PROCEDURE ON INPUT.             SQ1424.2
030400 INPUT-ERROR-PROCEDURE.                                           SQ1424.2
030500     IF DECL-EXEC-SW NOT = 9                                      SQ1424.2
030600         GO TO   NOT-DECL-9.                                      SQ1424.2
030700*                                                                 SQ1424.2
030800*    DECLARATIVE PROCEDURE ENTERED FROM OPEN INPUT                SQ1424.2
030900*                                                                 SQ1424.2
031000 DECL-OPEN-TEST.                                                  SQ1424.2
031100     MOVE    SPACE TO DUMMY-RECORD                                SQ1424.2
031200     PERFORM DECL-WRITE-LINE                                      SQ1424.2
031300     MOVE   "ABNORMAL TERMINATION AT THIS POINT IS ACCEPTABLE"    SQ1424.2
031400               TO DUMMY-RECORD                                    SQ1424.2
031500     PERFORM DECL-WRITE-LINE 3 TIMES.                             SQ1424.2
031600     GO TO   END-DECLS.                                           SQ1424.2
031700*                                                                 SQ1424.2
031800*                                                                 SQ1424.2
031900 NOT-DECL-9.                                                      SQ1424.2
032000     MOVE   "NOT-DECL-9"  TO PAR-NAME.                            SQ1424.2
032100     MOVE    DECL-EXEC-SW TO COMPUTED-18V0.                       SQ1424.2
032200     MOVE    9            TO CORRECT-18V0.                        SQ1424.2
032300     PERFORM DECL-FAIL.                                           SQ1424.2
032400     GO TO   END-DECLS.                                           SQ1424.2
032500*                                                                 SQ1424.2
032600*                                                                 SQ1424.2
032700*                                                                 SQ1424.2
032800 DECL-PASS.                                                       SQ1424.2
032900     MOVE   "PASS " TO P-OR-F.                                    SQ1424.2
033000     ADD     1 TO PASS-COUNTER.                                   SQ1424.2
033100     PERFORM DECL-PRINT-DETAIL.                                   SQ1424.2
033200*                                                                 SQ1424.2
033300 DECL-FAIL.                                                       SQ1424.2
033400     MOVE   "FAIL*" TO P-OR-F.                                    SQ1424.2
033500     ADD     1 TO ERROR-COUNTER.                                  SQ1424.2
033600     PERFORM DECL-PRINT-DETAIL.                                   SQ1424.2
033700*                                                                 SQ1424.2
033800 DECL-PRINT-DETAIL.                                               SQ1424.2
033900     IF REC-CT NOT EQUAL TO ZERO                                  SQ1424.2
034000             MOVE "." TO PARDOT-X                                 SQ1424.2
034100             MOVE REC-CT TO DOTVALUE.                             SQ1424.2
034200     MOVE    TEST-RESULTS TO PRINT-REC.                           SQ1424.2
034300     PERFORM DECL-WRITE-LINE.                                     SQ1424.2
034400     IF P-OR-F EQUAL TO "FAIL*"                                   SQ1424.2
034500         PERFORM DECL-WRITE-LINE                                  SQ1424.2
034600         PERFORM DECL-FAIL-ROUTINE THRU DECL-FAIL-EX              SQ1424.2
034700     ELSE                                                         SQ1424.2
034800         PERFORM DECL-BAIL THRU DECL-BAIL-EX.                     SQ1424.2
034900     MOVE    SPACE TO P-OR-F.                                     SQ1424.2
035000     MOVE    SPACE TO COMPUTED-X.                                 SQ1424.2
035100     MOVE    SPACE TO CORRECT-X.                                  SQ1424.2
035200     IF REC-CT EQUAL TO ZERO                                      SQ1424.2
035300         MOVE    SPACE TO PAR-NAME.                               SQ1424.2
035400     MOVE    SPACE TO RE-MARK.                                    SQ1424.2
035500*                                                                 SQ1424.2
035600 DECL-WRITE-LINE.                                                 SQ1424.2
035700     ADD     1 TO RECORD-COUNT.                                   SQ1424.2
035800     IF RECORD-COUNT GREATER 50                                   SQ1424.2
035900         MOVE    DUMMY-RECORD TO DUMMY-HOLD                       SQ1424.2
036000         MOVE    SPACE TO DUMMY-RECORD                            SQ1424.2
036100         WRITE   DUMMY-RECORD AFTER ADVANCING 1 LINES                SQ1424.2
036200         MOVE    CCVS-C-1 TO DUMMY-RECORD PERFORM DECL-WRT-LN     SQ1424.2
036300         MOVE    CCVS-C-2 TO DUMMY-RECORD                         SQ1424.2
036400         PERFORM DECL-WRT-LN 2 TIMES                              SQ1424.2
036500         MOVE    HYPHEN-LINE TO DUMMY-RECORD                      SQ1424.2
036600         PERFORM DECL-WRT-LN                                      SQ1424.2
036700         MOVE    DUMMY-HOLD TO DUMMY-RECORD                       SQ1424.2
036800         MOVE    ZERO TO RECORD-COUNT.                            SQ1424.2
036900     PERFORM DECL-WRT-LN.                                         SQ1424.2
037000*                                                                 SQ1424.2
037100 DECL-WRT-LN.                                                     SQ1424.2
037200     WRITE   DUMMY-RECORD AFTER ADVANCING 1 LINES.                SQ1424.2
037300     MOVE    SPACE TO DUMMY-RECORD.                               SQ1424.2
037400*                                                                 SQ1424.2
037500 DECL-FAIL-ROUTINE.                                               SQ1424.2
037600     IF COMPUTED-X NOT EQUAL TO SPACE GO TO DECL-FAIL-WRITE.      SQ1424.2
037700     IF CORRECT-X NOT EQUAL TO SPACE GO TO DECL-FAIL-WRITE.       SQ1424.2
037800     MOVE    ANSI-REFERENCE TO INF-ANSI-REFERENCE.                SQ1424.2
037900     MOVE   "NO FURTHER INFORMATION, SEE PROGRAM." TO INFO-TEXT.  SQ1424.2
038000     MOVE    XXINFO TO DUMMY-RECORD.                              SQ1424.2
038100     PERFORM DECL-WRITE-LINE 2 TIMES.                             SQ1424.2
038200     MOVE    SPACES TO INF-ANSI-REFERENCE.                        SQ1424.2
038300     GO TO   DECL-FAIL-EX.                                        SQ1424.2
038400 DECL-FAIL-WRITE.                                                 SQ1424.2
038500     MOVE    TEST-COMPUTED TO PRINT-REC                           SQ1424.2
038600     PERFORM DECL-WRITE-LINE                                      SQ1424.2
038700     MOVE    ANSI-REFERENCE TO COR-ANSI-REFERENCE.                SQ1424.2
038800     MOVE    TEST-CORRECT TO PRINT-REC                            SQ1424.2
038900     PERFORM DECL-WRITE-LINE 2 TIMES.                             SQ1424.2
039000     MOVE    SPACES TO COR-ANSI-REFERENCE.                        SQ1424.2
039100 DECL-FAIL-EX.                                                    SQ1424.2
039200     EXIT.                                                        SQ1424.2
039300*                                                                 SQ1424.2
039400 DECL-BAIL.                                                       SQ1424.2
039500     IF COMPUTED-A NOT EQUAL TO SPACE GO TO DECL-BAIL-WRITE.      SQ1424.2
039600     IF CORRECT-A EQUAL TO SPACE GO TO DECL-BAIL-EX.              SQ1424.2
039700 DECL-BAIL-WRITE.                                                 SQ1424.2
039800     MOVE    CORRECT-A TO XXCORRECT.                              SQ1424.2
039900     MOVE    COMPUTED-A TO XXCOMPUTED.                            SQ1424.2
040000     MOVE    XXINFO TO DUMMY-RECORD.                              SQ1424.2
040100     PERFORM DECL-WRITE-LINE 2 TIMES.                             SQ1424.2
040200 DECL-BAIL-EX.                                                    SQ1424.2
040300     EXIT.                                                        SQ1424.2
040400*                                                                 SQ1424.2
040500 END-DECLS.                                                       SQ1424.2
040600     MOVE    ZERO TO DECL-EXEC-SW.                                SQ1424.2
040700 END DECLARATIVES.                                                SQ1424.2
040800*                                                                 SQ1424.2
040900*                                                                 SQ1424.2
041000 CCVS1 SECTION.                                                   SQ1424.2
041100 OPEN-FILES.                                                      SQ1424.2
041200*P   OPEN    I-O RAW-DATA.                                        SQ1424.2
041300*P   MOVE    CCVS-PGM-ID TO RAW-DATA-KEY.                         SQ1424.2
041400*P   READ    RAW-DATA INVALID KEY GO TO END-E-1.                  SQ1424.2
041500*P   MOVE   "ABORTED "   TO C-ABORT.                              SQ1424.2
041600*P   ADD     1           TO C-NO-OF-TESTS.                        SQ1424.2
041700*P   ACCEPT  C-DATE      FROM DATE.                               SQ1424.2
041800*P   ACCEPT  C-TIME      FROM TIME.                               SQ1424.2
041900*P   REWRITE RAW-DATA-SATZ INVALID KEY CONTINUE.                  SQ1424.2
042000*PND-E-1.                                                         SQ1424.2
042100*P   CLOSE   RAW-DATA.                                            SQ1424.2
042200     OPEN    OUTPUT PRINT-FILE.                                   SQ1424.2
042300     MOVE    CCVS-PGM-ID TO TEST-ID.                              SQ1424.2
042400     MOVE    CCVS-PGM-ID TO ID-AGAIN.                             SQ1424.2
042500     MOVE    SPACE TO TEST-RESULTS.                               SQ1424.2
042600     PERFORM HEAD-ROUTINE THRU COLUMN-NAMES-ROUTINE.              SQ1424.2
042700     MOVE    ZERO TO REC-SKEL-SUB.                                SQ1424.2
042800     PERFORM CCVS-INIT-FILE 10 TIMES.                             SQ1424.2
042900     GO TO CCVS1-EXIT.                                            SQ1424.2
043000*                                                                 SQ1424.2
043100 CCVS-INIT-FILE.                                                  SQ1424.2
043200     ADD     1 TO REC-SKL-SUB.                                    SQ1424.2
043300     MOVE    FILE-RECORD-INFO-SKELETON TO                         SQ1424.2
043400                  FILE-RECORD-INFO (REC-SKL-SUB).                 SQ1424.2
043500*                                                                 SQ1424.2
043600 CLOSE-FILES.                                                     SQ1424.2
043700     PERFORM END-ROUTINE THRU END-ROUTINE-13.                     SQ1424.2
043800     CLOSE   PRINT-FILE.                                          SQ1424.2
043900*P   OPEN    I-O RAW-DATA.                                        SQ1424.2
044000*P   MOVE    CCVS-PGM-ID TO RAW-DATA-KEY.                         SQ1424.2
044100*P   READ    RAW-DATA INVALID KEY GO TO END-E-2.                  SQ1424.2
044200*P   MOVE   "OK.     " TO C-ABORT.                                SQ1424.2
044300*P   MOVE    PASS-COUNTER  TO C-OK.                               SQ1424.2
044400*P   MOVE    ERROR-HOLD    TO C-ALL.                              SQ1424.2
044500*P   MOVE    ERROR-COUNTER TO C-FAIL.                             SQ1424.2
044600*P   MOVE    DELETE-CNT    TO C-DELETED.                          SQ1424.2
044700*P   MOVE    INSPECT-COUNTER TO C-INSPECT.                        SQ1424.2
044800*P   REWRITE RAW-DATA-SATZ INVALID KEY CONTINUE.                  SQ1424.2
044900*PND-E-2.                                                         SQ1424.2
045000*P   CLOSE   RAW-DATA.                                            SQ1424.2
045100 TERMINATE-CCVS.                                                  SQ1424.2
045200*S   EXIT    PROGRAM.                                             SQ1424.2
045300     STOP    RUN.                                                 SQ1424.2
045400*                                                                 SQ1424.2
045500 INSPT.                                                           SQ1424.2
045600     MOVE   "INSPT" TO P-OR-F.                                    SQ1424.2
045700     ADD     1 TO INSPECT-COUNTER.                                SQ1424.2
045800     PERFORM PRINT-DETAIL.                                        SQ1424.2
045900                                                                  SQ1424.2
046000 PASS.                                                            SQ1424.2
046100     MOVE   "PASS " TO P-OR-F.                                    SQ1424.2
046200     ADD     1 TO PASS-COUNTER.                                   SQ1424.2
046300     PERFORM PRINT-DETAIL.                                        SQ1424.2
046400*                                                                 SQ1424.2
046500 FAIL.                                                            SQ1424.2
046600     MOVE   "FAIL*" TO P-OR-F.                                    SQ1424.2
046700     ADD     1 TO ERROR-COUNTER.                                  SQ1424.2
046800     PERFORM PRINT-DETAIL.                                        SQ1424.2
046900*                                                                 SQ1424.2
047000 DE-LETE.                                                         SQ1424.2
047100     MOVE   "****TEST DELETED****" TO RE-MARK.                    SQ1424.2
047200     MOVE   "*****" TO P-OR-F.                                    SQ1424.2
047300     ADD     1 TO DELETE-COUNTER.                                 SQ1424.2
047400     PERFORM PRINT-DETAIL.                                        SQ1424.2
047500*                                                                 SQ1424.2
047600 PRINT-DETAIL.                                                    SQ1424.2
047700     IF REC-CT NOT EQUAL TO ZERO                                  SQ1424.2
047800         MOVE   "." TO PARDOT-X                                   SQ1424.2
047900         MOVE    REC-CT TO DOTVALUE.                              SQ1424.2
048000     MOVE    TEST-RESULTS TO PRINT-REC.                           SQ1424.2
048100     PERFORM WRITE-LINE.                                          SQ1424.2
048200     IF P-OR-F EQUAL TO "FAIL*"                                   SQ1424.2
048300         PERFORM WRITE-LINE                                       SQ1424.2
048400         PERFORM FAIL-ROUTINE THRU FAIL-ROUTINE-EX                SQ1424.2
048500     ELSE                                                         SQ1424.2
048600         PERFORM BAIL-OUT THRU BAIL-OUT-EX.                       SQ1424.2
048700     MOVE    SPACE TO P-OR-F.                                     SQ1424.2
048800     MOVE    SPACE TO COMPUTED-X.                                 SQ1424.2
048900     MOVE    SPACE TO CORRECT-X.                                  SQ1424.2
049000     IF REC-CT EQUAL TO ZERO  MOVE SPACE TO PAR-NAME.             SQ1424.2
049100     MOVE    SPACE TO RE-MARK.                                    SQ1424.2
049200*                                                                 SQ1424.2
049300 HEAD-ROUTINE.                                                    SQ1424.2
049400     MOVE CCVS-H-1  TO DUMMY-RECORD. PERFORM WRITE-LINE 2 TIMES.  SQ1424.2
049500     MOVE CCVS-H-2A TO DUMMY-RECORD. PERFORM WRITE-LINE 2 TIMES.  SQ1424.2
049600     MOVE CCVS-H-2B TO DUMMY-RECORD. PERFORM WRITE-LINE 3 TIMES.  SQ1424.2
049700     MOVE CCVS-H-3  TO DUMMY-RECORD. PERFORM WRITE-LINE 3 TIMES.  SQ1424.2
049800 COLUMN-NAMES-ROUTINE.                                            SQ1424.2
049900     MOVE CCVS-C-1 TO DUMMY-RECORD. PERFORM WRITE-LINE.           SQ1424.2
050000     MOVE CCVS-C-2 TO DUMMY-RECORD. PERFORM WRITE-LINE 2 TIMES.   SQ1424.2
050100     MOVE HYPHEN-LINE TO DUMMY-RECORD. PERFORM WRITE-LINE.        SQ1424.2
050200 END-ROUTINE.                                                     SQ1424.2
050300     MOVE    HYPHEN-LINE TO DUMMY-RECORD.                         SQ1424.2
050400     PERFORM WRITE-LINE 5 TIMES.                                  SQ1424.2
050500 END-RTN-EXIT.                                                    SQ1424.2
050600     MOVE    CCVS-E-1 TO DUMMY-RECORD.                            SQ1424.2
050700     PERFORM WRITE-LINE 2 TIMES.                                  SQ1424.2
050800*                                                                 SQ1424.2
050900 END-ROUTINE-1.                                                   SQ1424.2
051000     ADD     ERROR-COUNTER   TO ERROR-HOLD                        SQ1424.2
051100     ADD     INSPECT-COUNTER TO ERROR-HOLD.                       SQ1424.2
051200     ADD     DELETE-COUNTER  TO ERROR-HOLD.                       SQ1424.2
051300     ADD     PASS-COUNTER    TO ERROR-HOLD.                       SQ1424.2
051400     MOVE    PASS-COUNTER    TO CCVS-E-4-1.                       SQ1424.2
051500     MOVE    ERROR-HOLD      TO CCVS-E-4-2.                       SQ1424.2
051600     MOVE    CCVS-E-4        TO CCVS-E-2-2.                       SQ1424.2
051700     MOVE    CCVS-E-2        TO DUMMY-RECORD                      SQ1424.2
051800     PERFORM WRITE-LINE.                                          SQ1424.2
051900     MOVE   "TEST(S) FAILED" TO ENDER-DESC.                       SQ1424.2
052000     IF ERROR-COUNTER IS EQUAL TO ZERO                            SQ1424.2
052100         MOVE   "NO " TO ERROR-TOTAL                              SQ1424.2
052200     ELSE                                                         SQ1424.2
052300         MOVE    ERROR-COUNTER TO ERROR-TOTAL.                    SQ1424.2
052400     MOVE    CCVS-E-2 TO DUMMY-RECORD.                            SQ1424.2
052500     PERFORM WRITE-LINE.                                          SQ1424.2
052600 END-ROUTINE-13.                                                  SQ1424.2
052700     IF DELETE-COUNTER IS EQUAL TO ZERO                           SQ1424.2
052800         MOVE   "NO " TO ERROR-TOTAL                              SQ1424.2
052900     ELSE                                                         SQ1424.2
053000         MOVE    DELETE-COUNTER TO ERROR-TOTAL.                   SQ1424.2
053100     MOVE   "TEST(S) DELETED     " TO ENDER-DESC.                 SQ1424.2
053200     MOVE    CCVS-E-2 TO DUMMY-RECORD.                            SQ1424.2
053300     PERFORM WRITE-LINE.                                          SQ1424.2
053400     IF INSPECT-COUNTER EQUAL TO ZERO                             SQ1424.2
053500         MOVE   "NO " TO ERROR-TOTAL                              SQ1424.2
053600     ELSE                                                         SQ1424.2
053700         MOVE    INSPECT-COUNTER TO ERROR-TOTAL.                  SQ1424.2
053800     MOVE   "TEST(S) REQUIRE INSPECTION" TO ENDER-DESC.           SQ1424.2
053900     MOVE    CCVS-E-2 TO DUMMY-RECORD. PERFORM WRITE-LINE.        SQ1424.2
054000     MOVE    CCVS-E-3 TO DUMMY-RECORD. PERFORM WRITE-LINE.        SQ1424.2
054100*                                                                 SQ1424.2
054200 WRITE-LINE.                                                      SQ1424.2
054300     ADD     1 TO RECORD-COUNT.                                   SQ1424.2
054400     IF RECORD-COUNT GREATER 50                                   SQ1424.2
054500         MOVE  DUMMY-RECORD TO DUMMY-HOLD                         SQ1424.2
054600         MOVE  SPACE TO DUMMY-RECORD                              SQ1424.2
054700         WRITE DUMMY-RECORD AFTER ADVANCING 1 LINES                  SQ1424.2
054800         MOVE  CCVS-C-1 TO DUMMY-RECORD PERFORM WRT-LN            SQ1424.2
054900         MOVE  CCVS-C-2 TO DUMMY-RECORD PERFORM WRT-LN 2 TIMES    SQ1424.2
055000         MOVE  HYPHEN-LINE TO DUMMY-RECORD PERFORM WRT-LN         SQ1424.2
055100         MOVE  DUMMY-HOLD TO DUMMY-RECORD                         SQ1424.2
055200         MOVE  ZERO TO RECORD-COUNT.                              SQ1424.2
055300     PERFORM WRT-LN.                                              SQ1424.2
055400*                                                                 SQ1424.2
055500 WRT-LN.                                                          SQ1424.2
055600     WRITE   DUMMY-RECORD AFTER ADVANCING 1 LINES.                SQ1424.2
055700     MOVE    SPACE TO DUMMY-RECORD.                               SQ1424.2
055800 BLANK-LINE-PRINT.                                                SQ1424.2
055900     PERFORM WRT-LN.                                              SQ1424.2
056000 FAIL-ROUTINE.                                                    SQ1424.2
056100     IF COMPUTED-X NOT EQUAL TO SPACE GO TO FAIL-ROUTINE-WRITE.   SQ1424.2
056200     IF CORRECT-X NOT EQUAL TO SPACE GO TO FAIL-ROUTINE-WRITE.    SQ1424.2
056300     MOVE    ANSI-REFERENCE TO INF-ANSI-REFERENCE.                SQ1424.2
056400     MOVE   "NO FURTHER INFORMATION, SEE PROGRAM." TO INFO-TEXT.  SQ1424.2
056500     MOVE    XXINFO TO DUMMY-RECORD.                              SQ1424.2
056600     PERFORM WRITE-LINE 2 TIMES.                                  SQ1424.2
056700     MOVE    SPACES TO INF-ANSI-REFERENCE.                        SQ1424.2
056800     GO TO   FAIL-ROUTINE-EX.                                     SQ1424.2
056900 FAIL-ROUTINE-WRITE.                                              SQ1424.2
057000     MOVE    TEST-COMPUTED  TO PRINT-REC                          SQ1424.2
057100     PERFORM WRITE-LINE                                           SQ1424.2
057200     MOVE    ANSI-REFERENCE TO COR-ANSI-REFERENCE.                SQ1424.2
057300     MOVE    TEST-CORRECT   TO PRINT-REC                          SQ1424.2
057400     PERFORM WRITE-LINE 2 TIMES.                                  SQ1424.2
057500     MOVE    SPACES         TO COR-ANSI-REFERENCE.                SQ1424.2
057600 FAIL-ROUTINE-EX.                                                 SQ1424.2
057700     EXIT.                                                        SQ1424.2
057800 BAIL-OUT.                                                        SQ1424.2
057900     IF COMPUTED-A NOT EQUAL TO SPACE GO TO BAIL-OUT-WRITE.       SQ1424.2
058000     IF CORRECT-A EQUAL TO SPACE GO TO BAIL-OUT-EX.               SQ1424.2
058100 BAIL-OUT-WRITE.                                                  SQ1424.2
058200     MOVE    CORRECT-A      TO XXCORRECT.                         SQ1424.2
058300     MOVE    COMPUTED-A     TO XXCOMPUTED.                        SQ1424.2
058400     MOVE    ANSI-REFERENCE TO INF-ANSI-REFERENCE.                SQ1424.2
058500     MOVE    XXINFO TO DUMMY-RECORD.                              SQ1424.2
058600     PERFORM WRITE-LINE 2 TIMES.                                  SQ1424.2
058700     MOVE    SPACES TO INF-ANSI-REFERENCE.                        SQ1424.2
058800 BAIL-OUT-EX.                                                     SQ1424.2
058900     EXIT.                                                        SQ1424.2
059000 CCVS1-EXIT.                                                      SQ1424.2
059100     EXIT.                                                        SQ1424.2
059200*                                                                 SQ1424.2
059300****************************************************************  SQ1424.2
059400*                                                              *  SQ1424.2
059500*    THIS POINT MARKS THE END OF THE CCVS MONITOR ROUTINES AND *  SQ1424.2
059600*    THE START OF THE TESTS OF SPECIFIC COBOL FEATURES.        *  SQ1424.2
059700*                                                              *  SQ1424.2
059800****************************************************************  SQ1424.2
059900*                                                                 SQ1424.2
060000 SECT-SQ142A-MAIN SECTION.                                        SQ1424.2
060100 OPEN-INIT-01.                                                    SQ1424.2
060200*                                                                 SQ1424.2
060300*    THIS PROGRAM ATTEMPTS TO OPEN A FILE WHICH IS NOT            SQ1424.2
060400*    PRESENT AND AVAILABLE TO IT.                                 SQ1424.2
060500*                                                                 SQ1424.2
060600     MOVE    1 TO REC-CT                                          SQ1424.2
060700     MOVE   "OPEN ABSENT FILE INPUT" TO FEATURE                   SQ1424.2
060800     MOVE   "OPEN-TEST-01" TO PAR-NAME                            SQ1424.2
060900     MOVE    9 TO DECL-EXEC-SW                                    SQ1424.2
061000     MOVE   "**" TO SQ-FS1-STATUS.                                SQ1424.2
061100 OPEN-TEST-01.                                                    SQ1424.2
061200     OPEN    INPUT SQ-FS1.                                        SQ1424.2
061300     MOVE   "OPEN-TEST-01" TO PAR-NAME.                           SQ1424.2
061400     MOVE    1 TO REC-CT.                                         SQ1424.2
061500     ADD     1 TO REC-CT.                                         SQ1424.2
061600     IF  SQ-FS1-STATUS NOT = "35"                                 SQ1424.2
061700         MOVE   "INCORRECT STATUS CODE RETURNED" TO RE-MARK       SQ1424.2
061800         MOVE   "VII-4, 1.5.3(3)C" TO ANSI-REFERENCE              SQ1424.2
061900         MOVE   "35" TO CORRECT-A                                 SQ1424.2
062000         MOVE    SQ-FS1-STATUS TO COMPUTED-A                      SQ1424.2
062100         PERFORM FAIL                                             SQ1424.2
062200     ELSE                                                         SQ1424.2
062300         PERFORM PASS.                                            SQ1424.2
062400*                                                                 SQ1424.2
062500*                                                                 SQ1424.2
062600 CCVS-EXIT SECTION.                                               SQ1424.2
062700 CCVS-999999.                                                     SQ1424.2
062800     GO TO   CLOSE-FILES.                                         SQ1424.2

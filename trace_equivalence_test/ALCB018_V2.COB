digraph ALCB018_V2.COBV2 {
node
276 [Node 534 START]
node
277 [F0A]
node
278 [PERFORM WCIS-INIT-TRAITEMENT]
node
279 [PERFORM F96BB]
node
280 [PERFORM F96BB]
node
281 [F0D]
node
282 [WHENEVER SQLWARNING CONTINUE]
node
283 [WHENEVER SQLERROR CONTINUE]
node
284 [F01-INITIALISATIONS]
node
285 [F04BB]
node
286 [PERFORM F94BB]
node
287 [IF BC01-YGREG = SPACES]
node
288 [PERFORM F9520-S]
node
289 [PERFORM F98BX]
node
290 [PERFORM F94BB]
node
291 [IF BC01-YGREG = SPACES]
node
292 [PERFORM F9520-S]
node
293 [PERFORM F98BX]
node
294 [F05-LECTURES]
node
295 [IF TR-FT = '0']
node
296 [PERFORM F95TR THRU F95TR-FN]
node
297 [IF TR-FT NOT = '1']
node
298 [F20-FIN-TRAITEMENT]
node
299 [IF FT = ALL '1']
node
300 [PERFORM WCIS-FIN-TRAITEMENT]
node
301 [F40BC]
node
302 [PERFORM F95-TR00-P]
node
303 [PERFORM  IK-TR NOT = 0]
node
304 [PERFORM F95-EN00-P]
node
305 [PERFORM  IK-EN NOT = 0]
node
306 [EVALUATE EN00-CEDEC5]
node
307 [PERFORM F95-EN00-RN]
node
308 [END PERFORM]
node
309 [PERFORM F91BB]
node
310 [PERFORM F95-EN00-CL]
node
311 [END PERFORM]
node
312 [PERFORM F95-TR00-CL]
node
313 [F90-ECRITURES]
node
314 [GO TO F05-LECTURES]
node
315 [F91BB]
node
316 [F94BB]
node
317 [IF SQLCODE NOT = ZERO AND SQLCODE NOT = 100]
node
318 [PERFORM F98BD THRU F98BD-FN]
node
319 [IF S-SPCB-XCORET NOT = SPACE]
node
320 [PERFORM F99ER]
node
321 [F95-EN00-P]
node
322 [IF 9-EN00-YCFDB2 NOT = '1']
node
323 [OPEN C-EN00]
node
324 [PERFORM F98BD THRU F98BD-FN]
node
325 [F95-EN00-RN]
node
326 [FETCH C-EN00 INTO
               :EN00-COETBB :V-EN00-COETBB ,
               :EN00-COCACC :V-EN00-COCACC ,
               :EN00-MTCPR3 :V-EN00-MTCPR3 ,
               :EN00-QTOPM1 :V-EN00-QTOPM1 ,
               :EN00-QTOPM2 :V-EN00-QTOPM2 ,
               :EN00-MTBRR1 :V-EN00-MTBRR1 ,
               :EN00-MTBRR2 :V-EN00-MTBRR2 ,
               :EN00-MTBRR3 :V-EN00-MTBRR3 ,
               :EN00-QTOPM3 :V-EN00-QTOPM3 ,
               :EN00-QTOPM4 :V-EN00-QTOPM4 ,
               :EN00-MTCPR1 :V-EN00-MTCPR1 ,
               :EN00-QTOPM5 :V-EN00-QTOPM5 ,
               :EN00-MTCPR2 :V-EN00-MTCPR2 ,
               :EN00-MTCORE :V-EN00-MTCORE ,
               :EN00-CEDEC5 :V-EN00-CEDEC5 ,
               :EN00-DAREGL :V-EN00-DAREGL ,
               :EN00-DATRA2 :V-EN00-DATRA2]
node
327 [PERFORM F98BD THRU F98BD-FN]
node
328 [EVALUATE IK]
node
329 [F95-EN00-CL]
node
330 [IF 9-EN00-YCFDB2 NOT = '0']
node
331 [CLOSE C-EN00]
node
332 [PERFORM F98BD THRU F98BD-FN]
node
333 [F95TR]
node
334 [F95-TR00-P]
node
335 [IF 9-TR00-YCFDB2 NOT = '1']
node
336 [OPEN C-TR00]
node
337 [PERFORM F98BD THRU F98BD-FN]
node
338 [F95-TR00-RN]
node
339 [FETCH C-TR00 INTO
               :TR00-COETBB :V-TR00-COETBB ,
               :TR00-COCACC :V-TR00-COCACC ,
               :TR00-MTCPR3 :V-TR00-MTCPR3 ,
               :TR00-QTOPM1 :V-TR00-QTOPM1 ,
               :TR00-QTOPM2 :V-TR00-QTOPM2 ,
               :TR00-MTBRR1 :V-TR00-MTBRR1 ,
               :TR00-MTBRR2 :V-TR00-MTBRR2 ,
               :TR00-MTBRR3 :V-TR00-MTBRR3 ,
               :TR00-QTOPM3 :V-TR00-QTOPM3 ,
               :TR00-QTOPM4 :V-TR00-QTOPM4 ,
               :TR00-MTCPR1 :V-TR00-MTCPR1 ,
               :TR00-QTOPM5 :V-TR00-QTOPM5 ,
               :TR00-MTCPR2 :V-TR00-MTCPR2]
node
340 [PERFORM F98BD THRU F98BD-FN]
node
341 [IF SQLCODE = +100]
node
342 [EVALUATE IK]
node
343 [F95TR-FN]
node
344 [F95-TR00-CL]
node
345 [IF 9-TR00-YCFDB2 NOT = '0']
node
346 [CLOSE C-TR00]
node
347 [PERFORM F98BD THRU F98BD-FN]
node
348 [F9520-S]
node
349 [IF T-DAT (1) = '1']
node
350 [IF T-DAT (2) = '1']
node
351 [IF T-DAT (3) = '1']
node
352 [IF T-DAT (4) = '1']
node
353 [F96BB]
node
354 [IF W-BB00-YCORET NOT = SPACE]
node
355 [GO TO F20-FIN-TRAITEMENT]
node
356 [F98BD]
node
357 [EVALUATE SQLCODE]
node
358 [GO TO F98BD-FN]
node
359 [GO TO F98BD-FN]
node
360 [PERFORM VARYING J98BQR FROM 1 BY 1 10 < J98BQR]
node
361 [END PERFORM]
node
362 [F98BX]
node
363 [F98BD-FN]
node
364 [F99ER]
node
365 [IF S-SPCB-XCORET NOT = SPACE AND S-SPCB-XCORET NOT = 'GE' AND S-SPCB-XCORET NOT = 'GB' AND S-SPCB-XCORET NOT = 'GK' AND S-SPCB-XCORET NOT = 'GA' AND S-SPCB-XCORET NOT = 'II' AND S-SPCB-XCORET NOT = 'GG']
node
366 [PERFORM F98BX]
node
367 [Node 573 END]
276 -> 277 [match:1]
277 -> 278 [match:1]
278 -> 279 [match:1]
279 -> 280 [match:1]
356 -> 279 [match:1]
279 -> 353 [match:1]
280 -> 281 [match:-1]
356 -> 280 [match:1]
280 -> 353 [match:-1]
281 -> 282 [match:-1]
282 -> 283 [match:-1]
283 -> 284 [match:-1]
284 -> 285 [match:-1]
285 -> 286 [match:-1]
286 -> 287 [match:-1]
321 -> 286 [match:-1]
286 -> 316 [match:-1]
287 -> 288 [match:-1]
287 -> 289 [match:-1]
353 -> 288 [match:-1]
288 -> 348 [match:-1]
288 -> 290 [match:-1]
363 -> 289 [match:-1]
289 -> 362 [match:-1]
289 -> 290 [match:-1]
290 -> 291 [match:-1]
321 -> 290 [match:-1]
290 -> 316 [match:-1]
291 -> 292 [match:-1]
291 -> 293 [match:-1]
353 -> 292 [match:-1]
292 -> 348 [match:-1]
292 -> 294 [match:-1]
363 -> 293 [match:-1]
293 -> 362 [match:-1]
293 -> 294 [match:-1]
294 -> 295 [match:-1]
295 -> 296 [match:-1]
295 -> 298 [match:-1]
296 -> 297 [match:-1]
344 -> 296 [match:-1]
296 -> 333 [match:-1]
297 -> 298 [match:-1]
297 -> 298 [match:-1]
298 -> 299 [match:-1]
299 -> 300 [match:-1]
299 -> 301 [match:-1]
300 -> 301 [match:-1]
301 -> 302 [match:-1]
302 -> 303 [match:-1]
338 -> 302 [match:-1]
302 -> 334 [match:-1]
303 -> 303 [match:-1]
303 -> 304 [match:-1]
304 -> 305 [match:-1]
325 -> 304 [match:-1]
304 -> 321 [match:-1]
305 -> 305 [match:-1]
305 -> 306 [match:-1]
306 -> 307 [match:-1]
307 -> 308 [match:-1]
329 -> 307 [match:-1]
307 -> 325 [match:-1]
308 -> 305 [match:-1]
308 -> 309 [match:-1]
309 -> 310 [match:-1]
316 -> 309 [match:-1]
309 -> 315 [match:-1]
310 -> 311 [match:-1]
333 -> 310 [match:-1]
310 -> 329 [match:-1]
311 -> 303 [match:-1]
311 -> 312 [match:-1]
312 -> 313 [match:-1]
348 -> 312 [match:-1]
312 -> 344 [match:-1]
313 -> 314 [match:-1]
314 -> 294 [match:-1]
315 -> 316 [match:-1]
316 -> 317 [match:-1]
317 -> 318 [match:-1]
317 -> 319 [match:-1]
364 -> 318 [match:-1]
318 -> 356 [match:-1]
318 -> 319 [match:-1]
319 -> 320 [match:-1]
319 -> 321 [match:-1]
367 -> 320 [match:-1]
320 -> 364 [match:1]
320 -> 321 [match:1]
321 -> 322 [match:-1]
322 -> 323 [match:-1]
322 -> 325 [match:-1]
323 -> 324 [match:-1]
364 -> 324 [match:-1]
324 -> 356 [match:-1]
324 -> 325 [match:-1]
325 -> 326 [match:-1]
326 -> 327 [match:-1]
327 -> 328 [match:-1]
364 -> 327 [match:-1]
327 -> 356 [match:-1]
328 -> 329 [match:-1]
329 -> 330 [match:-1]
330 -> 331 [match:-1]
330 -> 333 [match:-1]
331 -> 332 [match:-1]
364 -> 332 [match:-1]
332 -> 356 [match:-1]
332 -> 333 [match:-1]
333 -> 334 [match:-1]
334 -> 335 [match:-1]
335 -> 336 [match:-1]
335 -> 338 [match:-1]
336 -> 337 [match:-1]
364 -> 337 [match:-1]
337 -> 356 [match:-1]
337 -> 338 [match:-1]
338 -> 339 [match:-1]
339 -> 340 [match:-1]
340 -> 341 [match:-1]
364 -> 340 [match:-1]
340 -> 356 [match:-1]
341 -> 342 [match:-1]
341 -> 342 [match:-1]
342 -> 343 [match:-1]
343 -> 344 [match:-1]
344 -> 345 [match:-1]
345 -> 346 [match:-1]
345 -> 348 [match:-1]
346 -> 347 [match:-1]
364 -> 347 [match:-1]
347 -> 356 [match:-1]
347 -> 348 [match:-1]
348 -> 349 [match:-1]
349 -> 350 [match:-1]
349 -> 350 [match:-1]
350 -> 351 [match:-1]
350 -> 351 [match:-1]
351 -> 352 [match:-1]
351 -> 352 [match:-1]
352 -> 353 [match:-1]
352 -> 353 [match:-1]
353 -> 354 [match:1]
354 -> 355 [match:1]
354 -> 356 [match:1]
355 -> 298 [match:-1]
356 -> 357 [match:1]
357 -> 358 [match:1]
357 -> 359 [match:1]
357 -> 360 [match:1]
358 -> 363 [match:1]
359 -> 363 [match:-1]
360 -> 361 [match:-1]
360 -> 360 [match:-1]
361 -> 362 [match:-1]
362 -> 363 [match:1]
363 -> 364 [match:1]
364 -> 365 [match:1]
365 -> 366 [match:-1]
365 -> 367 [match:-1]
363 -> 366 [match:-1]
366 -> 362 [match:-1]

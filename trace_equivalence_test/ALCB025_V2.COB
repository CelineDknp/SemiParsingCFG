digraph ALCB025_V2.COBV2 {
node
226 [Node 489 START at depth 0]
node
227 [Node LABEL F0A]
node
228 [Node LOOP (label) to WCIS-INIT-TRAITEMENT]
node
229 [Node LOOP (label) to F96BB]
node
230 [Node LOOP (label) to F96BB]
node
231 [Node LABEL F0IAA]
node
232 [Node LABEL F0PPC]
node
233 [Node LABEL F0XDD]
node
234 [Node IF ZY01-YCOPCB NOT = SPACES]
node
235 [Node LOOP (label) to F98BX]
node
236 [Node IF WWBR-XRSTID NOT = SPACES]
node
237 [	Node IF PC00-YCTREP = 'ARRET']
node
238 [Node LOOP (label) to F20-FIN-TRAITEMENT]
node
239 [Node LABEL F0YAI]
node
240 [Node IF ZI1A-YAIRET = 256 OR 260]
node
241 [Node LOOP (label) to F99EA]
node
242 [Node IF ZI1A-YAIRET = 0 OR 2304]
node
243 [Node EVALUATE ZI1A-YAIRET]
node
244 [Node LOOP (label) to F99EA]
node
245 [Node LABEL F0ZFI]
node
246 [Node IF WWBR-XRSTID = SPACES]
node
247 [	Node IF Z101-YCOPCB NOT = SPACES]
node
248 [Node LOOP (label) to F98BX]
node
249 [	Node IF Z201-YCOPCB NOT = SPACES]
node
250 [Node LOOP (label) to F98BX]
node
251 [Node LOOP (label) to F9ROO]
node
252 [Node LOOP (label) to F9RPP]
node
253 [Node LABEL F03BB]
node
254 [Node IF ZL9Z-YGREG NOT = 'A']
node
255 [Node LOOP (label) to F98BX]
node
256 [Node EVALUATE ZL9Z-COENVP]
node
257 [Node LABEL F05-LECTURES]
node
258 [Node IF FI-FT = '0']
node
259 [Node LOOP (label) to F95FI]
node
260 [	Node IF FI-FT NOT = '1']
node
261 [Node LABEL F10-LECTURES-A-RUPTURE]
node
262 [Node IF WWBR-XRSTID NOT = SPACES AND WWBR-ZA001 = '1']
node
263 [Node LABEL F20-FIN-TRAITEMENT]
node
264 [Node IF FT = ALL '1']
node
265 [	Node IF Z101-YCOPCB = SPACES]
node
266 [Node LOOP (label) to F98BX]
node
267 [	Node IF Z201-YCOPCB = SPACES]
node
268 [Node LOOP (label) to F98BX]
node
269 [Node LOOP (label) to WCIS-FIN-TRAITEMENT]
node
270 [Node LABEL F30BB]
node
271 [Node IF WW00-COETCF NOT = '30004']
node
272 [Node LOOP (label) to F31BB]
node
273 [Node IF FI94-CODARA = '01']
node
274 [	Node IF FI94-CODARA = '09']
node
275 [		Node IF FI94-CODARA = '02' AND FI94-COOPST (1:1) = 'C']
node
276 [			Node EVALUATE TRUE]
node
277 [Node LOOP (label) to F31BB]
node
278 [Node LOOP (label) to F90FM]
node
279 [Node LOOP (label) to F05-LECTURES]
node
280 [Node LOOP (label) to F90FM]
node
281 [Node LOOP (label) to F05-LECTURES]
node
282 [Node LOOP (label) to F90FM]
node
283 [Node LOOP (label) to F05-LECTURES]
node
284 [Node LOOP (label) to F90FM]
node
285 [Node LOOP (label) to F05-LECTURES]
node
286 [Node LOOP (label) to F90FM]
node
287 [Node LOOP (label) to F05-LECTURES]
node
288 [Node LABEL F31BB]
node
289 [Node IF WW00-COETCF = '30004']
node
290 [Node LOOP (label) to F9R]
node
291 [Node LOOP (label) to F90FM]
node
292 [Node LOOP (label) to F05-LECTURES]
node
293 [Node LABEL F9R]
node
294 [Node IF WWBR-YQTMAJ < WWBR-YQTRE9]
node
295 [Node LOOP (label) to F05-LECTURES]
node
296 [Node LABEL F9ROO]
node
297 [Node LABEL F9RPP]
node
298 [Node IF ZY01-YCOPCB NOT = SPACES AND ZY01-YCOPCB NOT = 'QC']
node
299 [Node LOOP (label) to F98BX]
node
300 [Node LABEL F9Z99-RETOUR-BOUCLE]
node
301 [Node LOOP (label) to F05-LECTURES]
node
302 [Node LABEL F90FM]
node
303 [Node IF Z201-YCOPCB = SPACES]
node
304 [Node LOOP (label) to F98BX]
node
305 [Node LABEL F95FI]
node
306 [Node IF FI-FT = '0']
node
307 [	Node EVALUATE TRUE]
node
308 [Node LOOP (label) to F98BX]
node
309 [Node LABEL F96BB]
node
310 [Node IF W-DA00-YCORET NOT = SPACE]
node
311 [Node LOOP (label) to F20-FIN-TRAITEMENT]
node
312 [Node LABEL F98BX]
node
313 [Node LABEL F99EA]
node
314 [Node LOOP (label) to F98BX]
node
315 [Node IF S-SPCB-XCORET NOT = SPACE AND S-SPCB-XCORET NOT = 'GE' AND S-SPCB-XCORET NOT = 'GB' AND S-SPCB-XCORET NOT = 'GK' AND S-SPCB-XCORET NOT = 'GA' AND S-SPCB-XCORET NOT = 'II' AND S-SPCB-XCORET NOT = 'GG']
node
316 [Node LOOP (label) to F98BX]
node
317 [Node 543 END at depth 0]
226 -> 227 [match:1]
227 -> 228 [match:1]
228 -> 229 [match:1]
229 -> 230 [match:1]
312 -> 229 [match:1]
229 -> 309 [match:1]
230 -> 231 [match:1]
312 -> 230 [match:1]
230 -> 309 [match:1]
231 -> 232 [match:1]
232 -> 233 [match:1]
233 -> 234 [match:1]
234 -> 235 [match:-1]
234 -> 236 [match:-1]
313 -> 235 [match:-1]
235 -> 312 [match:-1]
235 -> 236 [match:-1]
236 -> 237 [match:-1]
236 -> 239 [match:-1]
237 -> 238 [match:-1]
237 -> 239 [match:-1]
238 -> 263 [match:-1]
239 -> 240 [match:-1]
240 -> 241 [match:-1]
240 -> 242 [match:-1]
241 -> 313 [match:-1]
242 -> 243 [match:-1]
242 -> 243 [match:-1]
243 -> 244 [match:-1]
243 -> 245 [match:-1]
244 -> 313 [match:-1]
245 -> 246 [match:-1]
246 -> 247 [match:-1]
246 -> 253 [match:-1]
247 -> 248 [match:-1]
247 -> 249 [match:-1]
313 -> 248 [match:-1]
248 -> 312 [match:-1]
248 -> 249 [match:-1]
249 -> 250 [match:-1]
249 -> 251 [match:-1]
313 -> 250 [match:-1]
250 -> 312 [match:-1]
250 -> 251 [match:-1]
251 -> 252 [match:-1]
297 -> 251 [match:-1]
251 -> 296 [match:-1]
300 -> 252 [match:-1]
252 -> 297 [match:-1]
252 -> 253 [match:-1]
253 -> 254 [match:-1]
254 -> 255 [match:-1]
254 -> 256 [match:-1]
313 -> 255 [match:-1]
255 -> 312 [match:-1]
255 -> 256 [match:-1]
256 -> 257 [match:-1]
257 -> 258 [match:-1]
258 -> 259 [match:-1]
258 -> 261 [match:-1]
259 -> 260 [match:-1]
309 -> 259 [match:-1]
259 -> 305 [match:-1]
260 -> 261 [match:-1]
260 -> 261 [match:-1]
261 -> 262 [match:-1]
262 -> 263 [match:-1]
262 -> 263 [match:-1]
263 -> 264 [match:-1]
264 -> 265 [match:-1]
264 -> 270 [match:-1]
265 -> 266 [match:-1]
265 -> 267 [match:-1]
313 -> 266 [match:-1]
266 -> 312 [match:-1]
266 -> 267 [match:-1]
267 -> 268 [match:-1]
267 -> 269 [match:-1]
313 -> 268 [match:-1]
268 -> 312 [match:-1]
268 -> 269 [match:-1]
269 -> 270 [match:-1]
270 -> 271 [match:-1]
271 -> 272 [match:-1]
271 -> 273 [match:-1]
272 -> 288 [match:-1]
273 -> 274 [match:-1]
273 -> 286 [match:-1]
274 -> 275 [match:-1]
274 -> 284 [match:-1]
275 -> 276 [match:-1]
275 -> 282 [match:-1]
276 -> 277 [match:-1]
276 -> 278 [match:-1]
276 -> 280 [match:-1]
277 -> 288 [match:-1]
278 -> 279 [match:-1]
305 -> 278 [match:-1]
278 -> 302 [match:-1]
279 -> 257 [match:-1]
280 -> 281 [match:-1]
305 -> 280 [match:-1]
280 -> 302 [match:-1]
281 -> 257 [match:-1]
282 -> 283 [match:-1]
305 -> 282 [match:-1]
282 -> 302 [match:-1]
283 -> 257 [match:-1]
284 -> 285 [match:-1]
305 -> 284 [match:-1]
284 -> 302 [match:-1]
285 -> 257 [match:-1]
286 -> 287 [match:-1]
305 -> 286 [match:-1]
286 -> 302 [match:-1]
287 -> 257 [match:-1]
288 -> 289 [match:-1]
289 -> 290 [match:-1]
289 -> 291 [match:-1]
290 -> 293 [match:-1]
291 -> 292 [match:-1]
305 -> 291 [match:-1]
291 -> 302 [match:-1]
292 -> 257 [match:-1]
293 -> 294 [match:-1]
294 -> 295 [match:-1]
294 -> 296 [match:-1]
295 -> 257 [match:-1]
296 -> 297 [match:-1]
297 -> 298 [match:-1]
298 -> 299 [match:-1]
298 -> 300 [match:-1]
313 -> 299 [match:-1]
299 -> 312 [match:-1]
299 -> 300 [match:-1]
300 -> 301 [match:-1]
301 -> 257 [match:-1]
302 -> 303 [match:-1]
303 -> 304 [match:-1]
303 -> 305 [match:-1]
313 -> 304 [match:-1]
304 -> 312 [match:-1]
304 -> 305 [match:-1]
305 -> 306 [match:-1]
306 -> 307 [match:-1]
306 -> 309 [match:-1]
307 -> 308 [match:-1]
307 -> 309 [match:-1]
313 -> 308 [match:-1]
308 -> 312 [match:-1]
308 -> 309 [match:-1]
309 -> 310 [match:1]
310 -> 311 [match:1]
310 -> 312 [match:1]
311 -> 263 [match:-1]
312 -> 313 [match:1]
313 -> 314 [match:1]
313 -> 314 [match:-1]
314 -> 312 [match:1]
314 -> 315 [match:1]
315 -> 316 [match:-1]
315 -> 317 [match:-1]
313 -> 316 [match:-1]
316 -> 312 [match:1]

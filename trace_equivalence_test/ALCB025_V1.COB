digraph ALCB025_V1.COBV1 {
node
0 [Node 284 START at depth 0]
node
1 [Node LABEL F0A]
node
2 [Node LABEL F0A-A]
node
3 [Node LOOP (label) to WCIS-INIT-TRAITEMENT]
node
4 [Node LABEL F0A-A-FN]
node
5 [Node LABEL F0ADB]
node
6 [Node LABEL F0ADB-FN]
node
7 [Node LABEL F0AZD]
node
8 [Node LOOP (multiple labels) to ['F96BB', 'F96BB-FN']]
node
9 [Node LOOP (multiple labels) to ['F96BB', 'F96BB-FN']]
node
10 [Node LABEL F0AZD-FN]
node
11 [Node LABEL F0A-FN]
node
12 [Node LABEL F0IAA]
node
13 [Node LABEL F0IAA-FN]
node
14 [Node LABEL F0L]
node
15 [Node LABEL F0L-FN]
node
16 [Node LABEL F0PPC]
node
17 [Node LABEL F0PPC-FN]
node
18 [Node LABEL F0XDD]
node
19 [Node IF ZY01-YCOPCB NOT = SPACES]
node
20 [Node LOOP (multiple labels) to ['F98BX', 'F98BX-FN']]
node
21 [Node LABEL F0XDD-FN]
node
22 [Node LABEL F0XHD]
node
23 [Node IF WWBR-XRSTID NOT = SPACES]
node
24 [Node LOOP to END_]
node
25 [Node LOOP (label) to F0XHD-FN]
node
26 [Node IF PC00-YCTREP = 'ARRET']
node
27 [Node LOOP (label) to F20]
node
28 [Node LABEL F0XHD-FN]
node
29 [Node LABEL F0YAI]
node
30 [Node IF ZI1A-YAIRET = 256 OR = 260]
node
31 [Node LOOP (label) to F99EA]
node
32 [Node IF ZI1A-YAIRET = ZERO OR = 2304]
node
33 [Node LABEL F0YAI-FN]
node
34 [Node LABEL F0YAJ]
node
35 [Node IF ZI1A-YAIRET = 256 OR = 260]
node
36 [Node LOOP (label) to F99EA]
node
37 [Node IF ZI1A-YAIRET = ZERO OR = 2304]
node
38 [Node LABEL F0YAJ-FN]
node
39 [Node LABEL F0ZFI]
node
40 [Node IF WWBR-XRSTID = SPACES]
node
41 [Node LOOP to END_]
node
42 [Node LOOP (label) to F0ZFI-FN]
node
43 [Node IF Z101-YCOPCB NOT = SPACES]
node
44 [Node LOOP (multiple labels) to ['F98BX', 'F98BX-FN']]
node
45 [Node LABEL F0ZFI-FN]
node
46 [Node LABEL F0ZFM]
node
47 [Node IF WWBR-XRSTID = SPACES]
node
48 [Node LOOP to END_]
node
49 [Node LOOP (label) to F0ZFM-FN]
node
50 [Node IF Z201-YCOPCB NOT = SPACES]
node
51 [Node LOOP (multiple labels) to ['F98BX', 'F98BX-FN']]
node
52 [Node LABEL F0ZFM-FN]
node
53 [Node LABEL F0Z90]
node
54 [Node IF WWBR-XRSTID = SPACES]
node
55 [Node LOOP to END_]
node
56 [Node LOOP (label) to F0Z90-FN]
node
57 [Node LOOP (multiple labels) to ['F9ROO', 'F9ROO-FN']]
node
58 [Node LABEL F0Z92]
node
59 [Node LABEL F0Z92-FN]
node
60 [Node LABEL F0Z94]
node
61 [Node LOOP (multiple labels) to ['F9RPP', 'F9RPP-FN']]
node
62 [Node LABEL F0Z94-FN]
node
63 [Node LABEL F0Z90-FN]
node
64 [Node LABEL F01]
node
65 [Node LABEL F01-FN]
node
66 [Node LABEL F03BB]
node
67 [Node LOOP (multiple labels) to ['F96EV', 'F96EV-FN']]
node
68 [Node IF ZL9Z-YGREG NOT = 'A']
node
69 [Node LOOP (multiple labels) to ['F98BX', 'F98BX-FN']]
node
70 [Node IF ZL9Z-COENVP = SPACES]
node
71 [Node IF ZL9Z-COENVP = '3']
node
72 [Node IF ZL9Z-COENVP = '4']
node
73 [Node IF ZL9Z-COENVP = '5']
node
74 [Node IF ZL9Z-COENVP = '6']
node
75 [Node LABEL F03BB-FN]
node
76 [Node LABEL F05]
node
77 [Node LABEL F05FI]
node
78 [Node IF FI-FT = '0']
node
79 [Node LOOP to END_]
node
80 [Node LOOP (label) to F05FI-FN]
node
81 [Node LABEL F05FI-10]
node
82 [Node LOOP (multiple labels) to ['F95FI', 'F95FI-FN']]
node
83 [Node IF FI-FT = '1']
node
84 [Node LOOP (label) to F05FI-FN]
node
85 [Node LABEL F05FI-FN]
node
86 [Node LABEL F05-FN]
node
87 [Node LABEL F1090]
node
88 [Node IF WWBR-XRSTID NOT = SPACES AND WWBR-ZA001 = '1']
node
89 [Node LOOP to END_]
node
90 [Node LOOP (label) to F1090-FN]
node
91 [Node LABEL F1090-FN]
node
92 [Node LABEL F20]
node
93 [Node IF FT = ALL '1']
node
94 [Node LOOP to END_]
node
95 [Node LOOP (label) to F20-FN]
node
96 [Node LABEL F20FI]
node
97 [Node IF Z101-YCOPCB NOT = SPACES]
node
98 [Node LOOP (multiple labels) to ['F98BX', 'F98BX-FN']]
node
99 [Node LABEL F20FI-FN]
node
100 [Node LABEL F20FM]
node
101 [Node IF Z201-YCOPCB NOT = SPACES]
node
102 [Node LOOP (multiple labels) to ['F98BX', 'F98BX-FN']]
node
103 [Node LABEL F20FM-FN]
node
104 [Node LABEL F20PC]
node
105 [Node LABEL F20PC-FN]
node
106 [Node LABEL F2098]
node
107 [Node LABEL F2099]
node
108 [Node LOOP (label) to WCIS-FIN-TRAITEMENT]
node
109 [Node LABEL F2099-FN]
node
110 [Node LABEL F2098-FN]
node
111 [Node LABEL F20-FN]
node
112 [Node LABEL F30BB]
node
113 [Node IF WW00-COETCF = '30004']
node
114 [Node LOOP to END_]
node
115 [Node LOOP (label) to F30BB-FN]
node
116 [Node LABEL F30BG]
node
117 [Node IF FI94-CODARA = '01']
node
118 [Node LOOP to END_]
node
119 [Node LOOP (label) to F30BG-FN]
node
120 [Node LOOP (multiple labels) to ['F90FM', 'F90FM-FN']]
node
121 [Node LOOP (label) to F05]
node
122 [Node LABEL F30BG-FN]
node
123 [Node LABEL F30BL]
node
124 [Node IF FI94-CODARA = '09']
node
125 [Node LOOP to END_]
node
126 [Node LOOP (label) to F30BL-FN]
node
127 [Node LOOP (multiple labels) to ['F90FM', 'F90FM-FN']]
node
128 [Node LOOP (label) to F05]
node
129 [Node LABEL F30BL-FN]
node
130 [Node LABEL F30BQ]
node
131 [Node IF FI94-CODARA = '02' AND FI94-COOPST (1:1) = 'C']
node
132 [Node LOOP to END_]
node
133 [Node LOOP (label) to F30BQ-FN]
node
134 [Node LOOP (multiple labels) to ['F90FM', 'F90FM-FN']]
node
135 [Node LOOP (label) to F05]
node
136 [Node LABEL F30BQ-FN]
node
137 [Node LABEL F30BS]
node
138 [Node IF FI94-CODARA = '02']
node
139 [Node LOOP to END_]
node
140 [Node LOOP (label) to F30BS-FN]
node
141 [Node LABEL F30BU]
node
142 [Node IF FI94-COOPST (1:1) = 'W' OR FI94-COOPST (1:1) = 'G' OR FI94-COOPST (1:1) = 'U']
node
143 [Node LOOP to END_]
node
144 [Node LOOP (label) to F30BU-FN]
node
145 [Node LOOP (multiple labels) to ['F90FM', 'F90FM-FN']]
node
146 [Node LOOP (label) to F05]
node
147 [Node LABEL F30BU-900]
node
148 [Node LOOP (label) to F30BV-FN]
node
149 [Node LABEL F30BU-FN]
node
150 [Node LABEL F30BV]
node
151 [Node LOOP (multiple labels) to ['F90FM', 'F90FM-FN']]
node
152 [Node LOOP (label) to F05]
node
153 [Node LABEL F30BV-FN]
node
154 [Node LABEL F30BS-FN]
node
155 [Node LABEL F30BB-FN]
node
156 [Node LABEL F31BB]
node
157 [Node IF WW00-COETCF NOT = '30004']
node
158 [Node LOOP to END_]
node
159 [Node LOOP (label) to F31BB-FN]
node
160 [Node LOOP (multiple labels) to ['F90FM', 'F90FM-FN']]
node
161 [Node LOOP (label) to F05]
node
162 [Node LABEL F31BB-FN]
node
163 [Node LABEL F9R]
node
164 [Node LABEL F9RBB]
node
165 [Node LABEL F9RNN]
node
166 [Node IF WWBR-YQTMAJ < WWBR-YQTRE9]
node
167 [Node LOOP (label) to F9R-FN]
node
168 [Node LABEL F9ROO]
node
169 [Node LABEL F9ROO-FN]
node
170 [Node LABEL F9RNN-FN]
node
171 [Node LABEL F9RBB-FN]
node
172 [Node LABEL F9RPP]
node
173 [Node IF ZY01-YCOPCB NOT = SPACES AND NOT = 'QC']
node
174 [Node LOOP (multiple labels) to ['F98BX', 'F98BX-FN']]
node
175 [Node LABEL F9RPP-FN]
node
176 [Node LABEL F9R-FN]
node
177 [Node LABEL F9Z99]
node
178 [Node LOOP (label) to F05]
node
179 [Node LABEL F9Z99-FN]
node
180 [Node LABEL F90FB]
node
181 [Node IF IK NOT = IK]
node
182 [Node LOOP to END_]
node
183 [Node LOOP (label) to F90FB-FN]
node
184 [Node LABEL F90FM]
node
185 [Node IF Z201-YCOPCB NOT = SPACES]
node
186 [Node LOOP (multiple labels) to ['F98BX', 'F98BX-FN']]
node
187 [Node LABEL F90FM-FN]
node
188 [Node LABEL F90FB-FN]
node
189 [Node LABEL F90GB]
node
190 [Node LABEL F90GB-FN]
node
191 [Node LABEL F9099-ITER-FN]
node
192 [Node LOOP (label) to F05]
node
193 [Node LABEL F95FI]
node
194 [Node IF FI-FT = '0']
node
195 [Node LOOP to END_]
node
196 [Node LOOP (label) to F95FI-FN]
node
197 [Node IF Z101-YCOPCB = 'GB']
node
198 [Node LOOP (label) to F95FI-FN]
node
199 [Node IF Z101-YCOPCB NOT = SPACES]
node
200 [Node LOOP (multiple labels) to ['F98BX', 'F98BX-FN']]
node
201 [Node LABEL F95FI-FN]
node
202 [Node LABEL F96BB]
node
203 [Node IF W-DA00-YCORET NOT = SPACE]
node
204 [Node LOOP (label) to F20]
node
205 [Node LABEL F96BB-FN]
node
206 [Node LABEL F96EV]
node
207 [Node LABEL F96EV-FN]
node
208 [Node LABEL F98]
node
209 [Node LABEL F98BX]
node
210 [Node LABEL F98BX-FN]
node
211 [Node LABEL F98BY]
node
212 [Node LABEL F98BY-FN]
node
213 [Node LABEL F98-FN]
node
214 [Node LABEL F99EA]
node
215 [Node LOOP (multiple labels) to ['F98BX', 'F98BX-FN']]
node
216 [Node LABEL F99EA-FN]
node
217 [Node LABEL F99ER]
node
218 [Node IF S-SPCB-XCORET NOT = ' ' AND 'GE' AND 'GB' AND 'GK' AND 'GA' AND 'II' AND 'GG']
node
219 [Node LOOP to END_]
node
220 [Node LOOP (label) to F99ER-FN]
node
221 [Node LABEL F99EU]
node
222 [Node LOOP (multiple labels) to ['F98BX', 'F98BX-FN']]
node
223 [Node LABEL F99EU-FN]
node
224 [Node LABEL F99ER-FN]
node
225 [Node 345 END at depth 0]
0 -> 1 [match:1]
1 -> 2 [match:1]
2 -> 3 [match:1]
3 -> 4 [match:1]
4 -> 5 [match:1]
5 -> 6 [match:1]
6 -> 7 [match:1]
7 -> 8 [match:1]
8 -> 9 [match:1]
206 -> 8 [match:1]
8 -> 202 [match:1]
9 -> 10 [match:-1]
206 -> 9 [match:1]
9 -> 202 [match:-1]
10 -> 11 [match:-1]
11 -> 12 [match:-1]
12 -> 13 [match:-1]
13 -> 14 [match:-1]
14 -> 15 [match:-1]
15 -> 16 [match:-1]
16 -> 17 [match:-1]
17 -> 18 [match:-1]
18 -> 19 [match:-1]
19 -> 20 [match:-1]
19 -> 21 [match:-1]
211 -> 20 [match:1]
20 -> 209 [match:-1]
20 -> 21 [match:-1]
21 -> 22 [match:-1]
22 -> 23 [match:-1]
23 -> 24 [match:-1]
23 -> 25 [match:-1]
24 -> 26 [match:-1]
25 -> 28 [match:-1]
26 -> 27 [match:-1]
26 -> 28 [match:-1]
27 -> 92 [match:-1]
28 -> 29 [match:-1]
29 -> 30 [match:-1]
30 -> 31 [match:-1]
30 -> 32 [match:-1]
31 -> 214 [match:-1]
32 -> 33 [match:-1]
32 -> 33 [match:-1]
33 -> 34 [match:-1]
34 -> 35 [match:-1]
35 -> 36 [match:-1]
35 -> 37 [match:-1]
36 -> 214 [match:-1]
37 -> 38 [match:-1]
37 -> 38 [match:-1]
38 -> 39 [match:-1]
39 -> 40 [match:-1]
40 -> 41 [match:-1]
40 -> 42 [match:-1]
41 -> 43 [match:-1]
42 -> 45 [match:-1]
43 -> 44 [match:-1]
43 -> 45 [match:-1]
211 -> 44 [match:1]
44 -> 209 [match:-1]
44 -> 45 [match:-1]
45 -> 46 [match:-1]
46 -> 47 [match:-1]
47 -> 48 [match:-1]
47 -> 49 [match:-1]
48 -> 50 [match:-1]
49 -> 52 [match:-1]
50 -> 51 [match:-1]
50 -> 52 [match:-1]
211 -> 51 [match:1]
51 -> 209 [match:-1]
51 -> 52 [match:-1]
52 -> 53 [match:-1]
53 -> 54 [match:-1]
54 -> 55 [match:-1]
54 -> 56 [match:-1]
55 -> 57 [match:-1]
56 -> 63 [match:-1]
57 -> 58 [match:-1]
170 -> 57 [match:-1]
57 -> 168 [match:-1]
58 -> 59 [match:-1]
59 -> 60 [match:-1]
60 -> 61 [match:-1]
61 -> 62 [match:-1]
176 -> 61 [match:-1]
61 -> 172 [match:-1]
62 -> 63 [match:-1]
63 -> 64 [match:-1]
64 -> 65 [match:-1]
65 -> 66 [match:-1]
66 -> 67 [match:-1]
67 -> 68 [match:-1]
208 -> 67 [match:-1]
67 -> 206 [match:-1]
68 -> 69 [match:-1]
68 -> 70 [match:-1]
211 -> 69 [match:1]
69 -> 209 [match:-1]
69 -> 70 [match:-1]
70 -> 71 [match:-1]
70 -> 71 [match:-1]
71 -> 72 [match:-1]
71 -> 72 [match:-1]
72 -> 73 [match:-1]
72 -> 73 [match:-1]
73 -> 74 [match:-1]
73 -> 74 [match:-1]
74 -> 75 [match:-1]
74 -> 75 [match:-1]
75 -> 76 [match:-1]
76 -> 77 [match:-1]
77 -> 78 [match:-1]
78 -> 79 [match:-1]
78 -> 80 [match:-1]
79 -> 81 [match:-1]
80 -> 85 [match:-1]
81 -> 82 [match:-1]
82 -> 83 [match:-1]
202 -> 82 [match:-1]
82 -> 193 [match:-1]
83 -> 84 [match:-1]
83 -> 85 [match:-1]
84 -> 85 [match:-1]
85 -> 86 [match:-1]
86 -> 87 [match:-1]
87 -> 88 [match:-1]
88 -> 89 [match:-1]
88 -> 90 [match:-1]
89 -> 91 [match:-1]
90 -> 91 [match:-1]
91 -> 92 [match:-1]
92 -> 93 [match:-1]
93 -> 94 [match:-1]
93 -> 95 [match:-1]
94 -> 96 [match:-1]
95 -> 111 [match:-1]
96 -> 97 [match:-1]
97 -> 98 [match:-1]
97 -> 99 [match:-1]
211 -> 98 [match:1]
98 -> 209 [match:-1]
98 -> 100 [match:-1]
99 -> 100 [match:-1]
100 -> 101 [match:-1]
101 -> 102 [match:-1]
101 -> 103 [match:-1]
211 -> 102 [match:1]
102 -> 209 [match:-1]
102 -> 104 [match:-1]
103 -> 104 [match:-1]
104 -> 105 [match:-1]
105 -> 106 [match:-1]
106 -> 107 [match:-1]
107 -> 108 [match:-1]
108 -> 109 [match:-1]
109 -> 110 [match:-1]
110 -> 111 [match:-1]
111 -> 112 [match:-1]
112 -> 113 [match:-1]
113 -> 114 [match:-1]
113 -> 115 [match:-1]
114 -> 116 [match:-1]
115 -> 155 [match:-1]
116 -> 117 [match:-1]
117 -> 118 [match:-1]
117 -> 119 [match:-1]
118 -> 120 [match:-1]
119 -> 122 [match:-1]
120 -> 121 [match:-1]
188 -> 120 [match:-1]
120 -> 184 [match:-1]
121 -> 76 [match:-1]
122 -> 123 [match:-1]
123 -> 124 [match:-1]
124 -> 125 [match:-1]
124 -> 126 [match:-1]
125 -> 127 [match:-1]
126 -> 129 [match:-1]
127 -> 128 [match:-1]
188 -> 127 [match:-1]
127 -> 184 [match:-1]
128 -> 76 [match:-1]
129 -> 130 [match:-1]
130 -> 131 [match:-1]
131 -> 132 [match:-1]
131 -> 133 [match:-1]
132 -> 134 [match:-1]
133 -> 136 [match:-1]
134 -> 135 [match:-1]
188 -> 134 [match:-1]
134 -> 184 [match:-1]
135 -> 76 [match:-1]
136 -> 137 [match:-1]
137 -> 138 [match:-1]
138 -> 139 [match:-1]
138 -> 140 [match:-1]
139 -> 141 [match:-1]
140 -> 154 [match:-1]
141 -> 142 [match:-1]
142 -> 143 [match:-1]
142 -> 144 [match:-1]
143 -> 145 [match:-1]
144 -> 149 [match:-1]
145 -> 146 [match:-1]
188 -> 145 [match:-1]
145 -> 184 [match:-1]
146 -> 76 [match:-1]
147 -> 148 [match:-1]
148 -> 153 [match:-1]
149 -> 150 [match:-1]
150 -> 151 [match:-1]
151 -> 152 [match:-1]
188 -> 151 [match:-1]
151 -> 184 [match:-1]
152 -> 76 [match:-1]
153 -> 154 [match:-1]
154 -> 155 [match:-1]
155 -> 156 [match:-1]
156 -> 157 [match:-1]
157 -> 158 [match:-1]
157 -> 159 [match:-1]
158 -> 160 [match:-1]
159 -> 162 [match:-1]
160 -> 161 [match:-1]
188 -> 160 [match:-1]
160 -> 184 [match:-1]
161 -> 76 [match:-1]
162 -> 163 [match:-1]
163 -> 164 [match:-1]
164 -> 165 [match:-1]
165 -> 166 [match:-1]
166 -> 167 [match:-1]
166 -> 168 [match:-1]
167 -> 176 [match:-1]
168 -> 169 [match:-1]
169 -> 170 [match:-1]
170 -> 171 [match:-1]
171 -> 172 [match:-1]
172 -> 173 [match:-1]
173 -> 174 [match:-1]
173 -> 175 [match:-1]
211 -> 174 [match:1]
174 -> 209 [match:-1]
174 -> 175 [match:-1]
175 -> 176 [match:-1]
176 -> 177 [match:-1]
177 -> 178 [match:-1]
178 -> 76 [match:-1]
179 -> 180 [match:-1]
180 -> 181 [match:-1]
181 -> 182 [match:-1]
181 -> 183 [match:-1]
182 -> 184 [match:-1]
183 -> 188 [match:-1]
184 -> 185 [match:-1]
185 -> 186 [match:-1]
185 -> 187 [match:-1]
211 -> 186 [match:1]
186 -> 209 [match:-1]
186 -> 187 [match:-1]
187 -> 188 [match:-1]
188 -> 189 [match:-1]
189 -> 190 [match:-1]
190 -> 191 [match:-1]
191 -> 192 [match:-1]
192 -> 76 [match:-1]
193 -> 194 [match:-1]
194 -> 195 [match:-1]
194 -> 196 [match:-1]
195 -> 197 [match:-1]
196 -> 201 [match:-1]
197 -> 198 [match:-1]
197 -> 199 [match:-1]
198 -> 201 [match:-1]
199 -> 200 [match:-1]
199 -> 201 [match:-1]
211 -> 200 [match:1]
200 -> 209 [match:-1]
200 -> 201 [match:-1]
201 -> 202 [match:-1]
202 -> 203 [match:1]
203 -> 204 [match:1]
203 -> 205 [match:1]
204 -> 92 [match:-1]
205 -> 206 [match:1]
206 -> 207 [match:1]
207 -> 208 [match:1]
208 -> 209 [match:1]
209 -> 210 [match:1]
210 -> 211 [match:1]
211 -> 212 [match:1]
212 -> 213 [match:1]
213 -> 214 [match:1]
214 -> 215 [match:1]
211 -> 215 [match:1]
215 -> 209 [match:1]
215 -> 216 [match:1]
216 -> 217 [match:1]
217 -> 218 [match:1]
218 -> 219 [match:-1]
218 -> 220 [match:-1]
219 -> 221 [match:1]
220 -> 224 [match:1]
221 -> 222 [match:1]
211 -> 222 [match:1]
222 -> 209 [match:1]
222 -> 223 [match:1]
223 -> 224 [match:1]
224 -> 225 [match:1]

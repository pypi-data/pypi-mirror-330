----------------------------------------------------------------------------
-- xplordb
-- 
-- Copyright (C) 2022  Oslandia / OpenLog
-- This program is free software: you can redistribute it and/or modify
-- it under the terms of the GNU Affero General Public License as published
-- by the Free Software Foundation, either version 3 of the License, or
-- (at your option) any later version.
--
-- This program is distributed in the hope that it will be useful,
-- but WITHOUT ANY WARRANTY; without even the implied warranty of
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
-- GNU Affero General Public License for more details.
-- 
-- You should have received a copy of the GNU Affero General Public License
-- along with this program.  If not, see <https://www.gnu.org/licenses/>.
-- 
-- __authors__ = ["davidms"]
-- __contact__ = "geology@oslandia.com"
-- __date__ = "2022/02/02"
-- __license__ = "AGPLv3"
----------------------------------------------------------------------------

--
-- PostgreSQL database dump
--

-- Dumped from database version 13.5 (Ubuntu 13.5-0ubuntu0.21.10.1)
-- Dumped by pg_dump version 13.5 (Ubuntu 13.5-0ubuntu0.21.10.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: elements; Type: TABLE DATA; Schema: ref; Owner: postgres
--

COPY ref.elements (at_no, bp_k, mp_k, density, at_wt, most_stable_oxidation_state, covalent_radius, at_radius__angstroms, first_ip, specific_heat_capacity, thermal_conductivity, electrical_conductivity, heat_of_fusion, heat_of_vaporization, electro_negativity, "group", "2nd_most_stable_oxidation_state", "3rd_most_stable_oxidation_state", "4th_most_stable_oxidation_state", mg_per_kg_crust, mg_per_l_seawater, pct_human_body_mass, length_of_name, name, symbol, years_since_discovery, family, orbital, metal_or_nonmetal, portugues_name) FROM stdin;
1	20.28	13.81	0.09	1.01	1	0.32	0.79	13.6	0	0.18	0	0.06	0.46	2.2	1	0	0	0	1400	108000	10	8	hydrogen	H	244	Hydrogen	s	M	hidrogÛnio
2	4.22	0.95	0.18	4	0	0.93	0.49	24.59	0	0.15	0	0.02	0.08	0	18	0	0	0	0.01	7e-16	0	6	helium	He	142	Noble gas	s	N	hÚlio
3	1615	453.7	0.53	6.94	1	1.23	2.05	5.39	3.58	84.7	11.7	3	147.1	0.98	1	0	0	0	20	0.18	0	7	lithium	Li	193	Alkali Metal	s	M	lÝtio
4	3243	1560	1.85	9.01	2	0.9	1.4	9.32	1.83	200	25	11.71	297	1.57	2	0	0	0	2.8	0	0	9	beryllium	Be	212	Alkaline Earth	s	M	berÝlio
5	4275	2365	2.34	10.81	3	0.82	1.17	5.3	1.03	27	0	22.6	507.8	2.04	13	0	0	0	10	4.44	0	5	boron	B	202	Boron	p	N	boro
6	5100	3825	2.26	12.01	4	0.77	0.91	11.26	0.71	0	0.07	0	715	2.55	14	2	0	0	200	28	23	6	carbon	C	*	Carbon	p	N	carbono
7	77.34	63.15	1.25	14.01	3	0.75	0.75	14.53	1.04	0.03	0	0.36	2.79	3.04	15	5	4	2	19	50	2.6	8	nitrogen	N	238	Pnictide	p	N	nitrogÛnio
8	90.19	54.8	1.43	16	2	0.73	0.65	13.62	0.92	0.27	0	0.22	3.41	3.44	16	0	0	0	461000	857000	61	6	oxygen	O	236	Chalcogen	p	N	oxigÛnio
9	85	53.55	1.7	19	1	0.72	0.57	17.42	0.82	0.03	0	0.26	3.27	3.98	17	0	0	0	585	1.3	0	8	fluorine	F	144	Halogen	p	N	fl·or
10	27.1	24.55	0.9	20.18	0	0.71	0.51	21.56	1.03	0.05	0	0.34	1.77	0	18	0	0	0	0.01	0	0	4	neon	Ne	112	Noble gas	p	N	ne¶nio
11	1156	371	0.97	22.99	1	1.54	2.23	5.14	1.23	141	20.1	2.6	98.01	0.93	1	0	0	0	0	10800	0.14	6	sodium	Na	203	Alkali Metal	s	M	s¾dio
12	1380	922	1.74	24.31	2	1.36	1.72	7.65	1.02	156	22.4	8.95	127.6	1.31	2	0	0	0	23300	1290	0.03	9	magnesium	Mg	202	Alkaline Earth	s	M	magnÚsio
13	2740	933.5	2.7	26.98	3	1.18	1.62	5.99	0.9	237	37.7	10.7	290.8	1.61	13	0	0	0	82300	0	0	8	aluminum	Al	185	Boron	p	M	alumÝnio
14	2630	1683	2.33	28.09	4	1.11	1.44	8.15	0.7	148	0	50.2	359	1.9	14	2	0	0	282000	2.2	0.03	7	silicon	Si	186	Carbon		N	silÝcio
15	553	317.3	1.82	30.97	5	1.06	1.23	10.49	0.77	0.24	1e-16	0.63	12.4	2.19	15	5	4	0	1050	0.06	1.1	10	phosphorus	P	341	Pnictide	p	N	f¾sforo
16	717.82	392.2	2.07	32.07	6	1.02	1.09	10.36	0.71	0.27	5e-16	1.73	10	2.58	16	4	6	0	350	905	0.2	6	sulfur	S	*	Chalcogen	p	N	enxofre
17	239.18	172.17	3.21	35.45	1	0.99	0.97	12.97	0.48	0.01	0	3.21	10.2	3.16	17	3	5	7	145	19400	0.12	8	chlorine	Cl	236	Halogen	p	N	cloro
18	87.45	83.95	1.78	39.95	0	0.98	0.88	15.76	0.52	0.02	0	1.19	6.51	0	18	0	0	0	3.5	0.45	0	5	argon	Ar	116	Noble gas	p	N	arg¶nio
19	1033	336.8	0.86	39.1	1	2.03	2.77	4.34	0.76	102.5	16.4	2.33	76.9	0.82	1	0	0	0	20900	399	0.2	9	potassium	K	203	Alkali Metal	s	M	potßssio
20	1757	1112	1.55	40.08	2	1.74	2.23	6.11	0.65	200	31.3	8.53	154.67	1	2	0	0	0	41500	412	1.4	7	calcium	Ca	202	Alkaline Earth	s	M	calico
21	3109	1814	2.99	44.96	3	1.44	2.09	6.54	0.57	15.8	1.5	16.11	304.8	1.36	3	0	0	0	22	0	0	8	scandium	Sc	140	Transition Metal	d	M	escÔndio
22	3560	1935	4.54	47.88	4	1.32	2	6.82	0.52	21.9	2.6	18.6	425.2	1.54	4	3	0	0	5650	0	0	8	titanium	Ti	219	Transition Metal	d	M	titÔnio
23	3650	2163	6.11	50.94	5	1.22	1.92	6.74	0.49	30.7	4	22.8	446.7	1.63	5	4	3	2	120	0	0	8	vanadium	V	180	Transition Metal	d	M	vanÔdio
24	2945	2130	7.19	52	3	1.18	1.85	6.77	0.45	93.7	7.9	20	339.5	1.66	6	6	2	0	102	0	0	8	chromium	Cr	213	Transition Metal	d	M	cromo
25	2235	1518	7.44	54.94	4	1.17	1.79	7.44	0.48	7.82	0.5	14.64	219.74	1.55	7	2	7	6	950	0	0	9	manganese	Mn	236	Transition Metal	d	M	manganÛs
26	3023	1808	7.87	55.85	3	1.17	1.72	7.87	0.45	80.2	11.2	13.8	349.5	1.83	8	3	0	0	56300	0	0.01	4	iron	Fe	*	Transition Metal	d	M	ferro
27	3143	1768	8.9	58.93	2	1.16	1.67	7.86	0.42	100	17.9	16.19	373.3	1.88	9	3	0	0	25	0	0	6	cobalt	Co	275	Transition Metal	d	M	cobalto
28	3005	1726	8.9	58.69	2	1.15	1.62	7.64	0.44	90.7	14.6	17.2	377.5	1.91	10	3	0	0	84	0	0	6	nickel	Ni	259	Transition Metal	d	M	nÝquel
29	2840	1356.6	8.96	63.46	2	1.17	1.57	7.73	0.39	401	60.7	13.14	300.5	1.9	11	1	0	0	60	0	0	6	copper	Cu	*	Transition Metal	d	M	cobre
30	1180	692.73	7.13	65.39	2	1.25	1.53	9.39	0.39	116	16.9	7.38	115.3	1.65	12	0	0	0	70	0	0	4	zinc	Zn	760	Transition Metal	d	M	zinco
31	2478	302.92	5.91	69.72	3	1.26	1.81	6	0.37	40.6	1.8	5.59	256.06	1.81	13	0	0	0	19	0	0	7	gallium	Ga	135	Boron	p	M	gßlio
32	3107	1211.5	5.32	72.61	4	1.22	1.52	7.9	0.32	59.9	0	31.8	334.3	2.01	14	0	0	0	1.5	0	0	9	germanium	Ge	124	Carbon	p	M	germÔndio
33	876	1090	5.78	74.92	3	1.2	1.33	9.81	0.33	50	3.8	27.7	32.4	2.16	15	5	0	0	1.8	0	0	7	arsenic	As	760	Pnictide	p	N	arsÛnio
34	958	494	4.79	78.96	4	1.16	1.22	9.75	0.32	2.04	8	5.54	26.32	2.55	16	-2	6	0	0.05	0	0	8	selenium	Se	193	Chalcogen	p	N	selÛnio
35	331.85	265.95	3.12	79.9	1	1.14	1.12	11.81	0.23	0.12	1e-16	5.29	14.73	2.96	17	5	7	0	2.4	67.3	0	7	bromine	Br	184	Halogen	p	N	bromo
36	120.85	116	3.75	83.8	0	1.89	1.03	14	0.25	0.01	0	1.64	9.03	0	18	2	0	0	0	0	0	7	krypton	Kr	112	Noble gas	p	N	cript¶nio
37	961	312.63	1.53	85.47	1	2.16	2.98	4.18	0.36	58.2	47.8	2.34	69.2	0.82	1	0	0	0	90	0.12	0	8	rubidium	Rb	149	Alkali Metal	s	M	rubÝdio
38	1655	1042	2.54	87.62	2	1.91	2.45	5.7	0.3	3.53	5	8.2	136.9	0.95	2	0	0	0	370	7.2	0	9	strontium	Sr	220	Alkaline Earth	s	M	estr¶ntio
39	3611	1795	4.47	88.91	3	1.62	2.27	6.38	0.3	17.2	1.8	17.15	393.3	1.22	3	0	0	0	33	0	0	7	yttrium	Y	182	Transition Metal	d	M	Ýtrio
40	4682	2128	6.51	91.22	4	1.45	2.16	6.34	0.28	22.7	2.3	21	590.5	1.33	4	0	0	0	165	0	0	9	zirconium	Zr	221	Transition Metal	d	M	zirc¶nio
41	5015	2742	8.57	92.91	5	1.34	2.08	6.88	0.27	53.7	6.6	26.9	690.1	1.6	5	3	0	0	20	0	0	7	niobium	Nb	146	Transition Metal	d	M	ni¾bio
42	4912	2896	10.22	95.94	6	1.3	2.01	7.1	0.25	138	17.3	36	590.4	2.16	6	5	4	3	1.2	0.01	0	10	molybdenum	Mo	228	Transition Metal	d	M	molibdÛnio
43	4538	2477	11.5	98	7	1.27	1.95	7.28	0.24	50.6	0	23	502	1.9	7	0	0	0	0	0	0	10	technetium	Tc	73	Transition Metal	d	M	tecnÚcio
44	4425	2610	12.37	101.07	3	1.25	1.89	7.37	0.24	117	14.9	25.52	567.77	2.2	8	4	2	6	0	0	0	9	ruthenium	Ru	166	Transition Metal	d	M	rutÛnio
45	3970	2236	12.41	102.91	3	1.25	1.83	7.46	0.24	150	23	21.76	495.39	2.28	9	2	4	0	0	0	0	7	rhodium	Rh	207	Transition Metal	d	M	r¾dio
46	3240	1825	12	106.42	2	1.28	1.79	8.34	0.24	71.8	10	16.74	393.3	2.2	10	4	0	0	0.02	0	0	9	palladium	Pd	207	Transition Metal	d	M	palßdio
47	2436	1235.08	10.5	107.87	1	1.34	1.75	7.58	0.24	429	62.9	11.3	250.63	1.93	11	0	0	0	0.08	0	0	6	silver	Ag	*	Transition Metal	d	M	prata
48	1040	594.26	8.65	112.41	2	1.41	1.71	8.99	0.23	96.8	14.7	6.07	99.87	1.69	12	0	0	0	0.15	0	0	7	cadmium	Cd	193	Transition Metal	d	M	cßdmio
49	2350	429.78	7.31	114.82	3	1.44	2	5.79	0.23	81.6	3.4	3.26	226.34	1.78	13	0	0	0	0.25	0	0	6	indium	In	86	Boron	p	M	indio
50	2876	505.12	7.31	118.71	4	1.41	1.72	7.34	0.23	66.6	8.7	7.2	290.37	1.96	14	2	0	0	2.3	0	0	3	tin	Sn	*	Carbon	p	M	estanho
51	1860	903.91	6.69	121.76	3	1.4	1.53	8.64	0.21	24.3	2.6	19.83	67.97	2.05	15	5	0	0	0.2	0	0	8	antimony	Sb	410	Pnictide	p	M	antim¶nio
52	1261	722.72	6.24	127.6	4	1.36	1.42	9.01	0.2	2.35	0	17.49	50.63	2.1	16	-2	6	0	0	0	0	9	tellurium	Te	228	Chalcogen	p	N	tel·rio
53	457.5	386.7	4.93	126.9	1	1.33	1.32	10.45	0.15	0.45	0	7.76	20.9	2.66	17	5	7	0	0.45	0.06	0	6	iodine	I	199	Halogen	p	N	iodo
54	165.1	161.39	5.9	131.29	0	1.31	1.24	12.13	0.16	0.01	0	2.3	12.64	0	18	2	4	6	0	0	0	5	xenon	Xe	112	Noble gas	p	N	xen¶nio
55	944	301.54	1.87	132.91	1	2.35	3.34	3.89	0.24	35.9	5.3	2.09	67.74	0.79	1	0	0	0	3	0	0	6	cesium	Cs	150	Alkali Metal	s	M	cÚsio
56	2078	1002	3.59	137.33	2	1.98	2.76	5.21	0.2	18.4	2.8	8.01	140.2	0.89	2	0	0	0	425	0.01	0	6	barium	Ba	202	Alkaline Earth	s	M	bßrio
57	3737	1191	6.15	138.91	3	1.25	2.74	5.58	0.19	13.5	1.9	11.3	399.57	1.1	3	0	0	0	39	0	0	9	lanthanum	La	171	Rare Earth	d	M	lantÔnio
58	3715	1071	6.77	140.12	3	1.65	2.7	5.54	0.19	11.4	1.4	9.2	313.8	1.12	3	4	0	0	66.5	0	0	6	cerium	Ce	207	Rare Earth	f	M	cÚrio
59	3785	1204	6.77	140.91	3	1.65	2.67	5.46	0.19	12.5	1.5	10.04	332.63	1.13	3	4	0	0	9.2	0	0	12	praseodymium	Pr	125	Rare Earth	f	M	praseodÝmio
60	3347	1294	7.01	144.24	3	1.64	2.64	5.53	0.19	16.5	1.6	10.88	283.68	1.14	3	0	0	0	41.5	0	0	9	neodymium	Nd	169	Rare Earth	f	M	neodÝmio
61	3273	1315	7.22	145	3	1.63	2.62	5.55	0	17.9	2	0	0	1.13	3	0	0	0	0	0	0	10	promethium	Pm	69	Rare Earth	f	M	promÚcio
62	2067	1347	2.75	150.36	3	1.62	2.59	5.64	0.2	0	1.1	11.09	191.63	1.17	3	2	0	0	7.05	0	0	8	samarium	Sm	131	Rare Earth	f	M	samßrio
63	1800	1095	5.24	151.97	3	1.85	2.56	5.67	0.18	13.9	1.1	10.46	175.73	1.2	3	2	0	0	2	0	0	8	europium	Eu	109	Rare Earth	f	M	eur¾pio
64	3545	1585	7.9	157.25	3	1.61	2.54	6.15	0.24	10.6	0.8	15.48	311.71	1.2	3	0	0	0	6.2	0	0	10	gadolinium	Gd	124	Rare Earth	f	M	gadolÝnio
65	3500	1629	8.23	158.93	3	1.59	2.51	5.86	0.18	11.1	0.9	0	0	1.2	3	4	0	0	1.2	0	0	7	terbium	Tb	167	Rare Earth	f	M	tÚrbio
66	2840	1685	8.55	162.5	3	1.59	2.49	5.94	0.17	10.7	1.1	11.06	230	1.22	3	0	0	0	5.2	0	0	10	dysprosium	Dy	124	Rare Earth	f	M	dispr¾sio
67	2968	1747	8.8	164.93	3	1.58	2.47	6.02	0.17	16.2	1.1	17.15	251.04	1.23	3	0	0	0	1.3	0	0	7	holmium	Ho	132	Rare Earth	f	M	h¾lmio
68	3140	1802	9.07	167.26	3	1.57	2.45	6.1	0.17	14.3	1.2	17.15	292.88	1.24	3	0	0	0	3.5	0	0	6	erbium	Er	168	Rare Earth	f	M	Úrmio
69	2223	1818	9.32	168.93	3	1.56	2.42	6.18	0.16	16.8	1.3	16.8	191	1.25	3	2	0	0	0.52	0	0	7	thulium	Tm	131	Rare Earth	f	M	t·lio
70	1469	1092	6.97	173.04	3	1.7	2.4	6.25	0.16	34.9	3.7	7.7	128	1.1	3	2	0	0	3.2	0	0	9	ytterbium	Yb	103	Rare Earth	f	M	itÚrbio
71	3668	1936	9.84	174.97	3	1.56	2.25	5.43	0.15	16.4	1.5	18.6	355	1.27	3	0	0	0	0.8	0	0	8	lutetium	Lu	103	Rare Earth	d	M	lutÚcio
72	4875	2504	13.31	178.49	4	1.44	2.16	6.65	0.14	23	3.4	21.76	661.07	1.3	4	0	0	0	3	0	0	7	hafnium	Hf	87	Transition Metal	d	M	hßfrio
73	5730	3293	16.65	180.95	5	1.34	2.09	7.89	0.14	57.5	8.1	36	737	1.5	5	0	0	0	2	0	0	8	tantalum	Ta	208	Transition Metal	d	M	tÔntalo
74	5825	3695	19.3	183.85	6	1.3	2.02	7.98	0.13	174	18.2	35.4	422.58	2.36	6	5	4	3	1.25	0	0	8	tungsten	W	227	Transition Metal	d	M	tungstÛnio
75	5870	3455	21	186.21	7	1.28	1.97	7.88	0.14	47.9	5.8	33.05	707.1	1.9	7	4	6	2	0	0	0	7	rhenium	Re	85	Transition Metal	d	M	rÛnio
76	5300	3300	22.6	190.2	4	1.26	1.92	8.7	0.13	87.6	12.3	29.29	627.6	2.2	8	3	6	8	0	0	0	6	osmium	Os	207	Transition Metal	d	M	¾smio
77	4700	2720	22.6	192.22	4	1.27	1.87	9.1	0.13	147	21.3	26.36	563.58	2.2	9	2	3	6	0	0	0	7	iridium	Ir	207	Transition Metal	d	M	irÝdio
78	4100	2042.1	21.45	195.08	4	1.3	1.83	9	0.13	71.6	9.4	19.66	510.45	2.28	10	2	0	0	0.01	0	0	8	platinum	Pt	275	Transition Metal	d	M	platina
79	3130	1337.58	19.3	196.97	3	1.34	1.79	9.23	0.13	317	48.8	12.36	324.43	2.54	11	1	0	0	0	0	0	4	gold	Au	*	Transition Metal	d	M	ouro
80	629.88	234.31	13.55	200.59	2	1.49	1.76	10.44	0.14	8.34	1	2.29	59.3	2	12	1	0	0	0.09	0	0	7	mercury	Hg	*	Transition Metal	d	M	merc·rio
81	1746	577	11.85	204.38	1	1.48	2.08	6.11	0.13	46.1	5.6	4.27	162.09	2.04	13	3	0	0	0.85	0	0	8	thallium	Tl	149	Boron	p	M	tßlio
82	2023	600.65	11.35	207.2	2	1.47	1.81	7.42	0.13	35.3	4.8	4.77	177.9	2.33	14	4	0	0	0.14	0	0	4	lead	Pb	*	Carbon	p	M	chumbo
83	1837	544.59	9.75	208.98	3	1.46	1.63	7.29	0.12	7.87	0.9	11	179	2.02	15	5	0	0	0.01	0	0	7	bismuth	Bi	257	Pnictide	p	M	bismuto
84	1235	527	9.3	209	4	1.53	1.53	8.42	0	20	0.7	13	120	2	16	2	6	0	0	0	0	8	polonium	Po	112	Chalcogen	p	M	pol¶nio
85	610	575	0	210	1	1.47	1.43	0	0	1.7	0	12	30	2.2	17	3	5	7	0	0	0	8	astatine	At	70	Halogen	p	N	astato
86	211.4	202	9.73	222	0	0	1.34	10.75	0.09	0	0	2.9	16.4	0	18	2	0	0	0	6e-16	0	5	radon	Rn	110	Noble gas	p	N	rad¶nio
87	950	300	0	223	1	0	2.7	0	0	15	0	2.1	64	0.7	1	0	0	0	0	0	0	8	francium	Fr	71	Alkali Metal	s	M	frÔncio
88	1413	973	5	226.03	2	0	2.23	5.28	0.09	18.6	1	8.37	136.82	0.9	2	0	0	0	0	0	0	6	radium	Ra	112	Alkaline Earth	s	M	rßdio
89	3470	1324	10.07	227	3	0	1.88	5.17	0.12	12	0	0	0	1.1	3	0	0	0	0	0	0	8	actinium	Ac	111	Rare Earth	d	M	actÝnio
90	5060	2028	11.72	232.04	4	1.65	1.8	6.01	0.11	54	7.1	15.65	543.92	1.3	3	0	0	0	9.6	0	0	7	thorium	Th	182	Rare Earth	f	M	t¾rio
91	4300	1845	15.4	231.04	5	0	1.61	5.89	0	47	5.6	0	0	1.5	3	4	0	0	0	0	0	12	protactinium	Pa	97	Rare Earth	f	M	protactÝnio
92	4407	1408	18.95	238.03	6	1.42	1.38	6.05	0.12	27.6	3.6	15.48	422.58	1.38	3	5	4	3	2.7	0	0	7	uranium	U	221	Rare Earth	f	M	urÔnio
93	4175	912	20.2	237.05	5	0	1.3	6.19	0	6.3	0.8	0	0	1.36	3	6	4	3	0	0	0	9	neptunium	Np	70	Rare Earth	f	M	net·nio
94	3505	913	19.84	244	4	1.08	1.51	6.06	0.13	6.74	0.7	0	0	1.28	3	6	5	3	0	0	0	9	plutonium	Pu	70	Rare Earth	f	M	plut¶nio
95	2880	1449	13.7	243	3	0	1.84	5.99	0	10	0.7	0	0	1.3	3	6	5	4	0	0	0	9	americium	Am	66	Rare Earth	f	M	amerÝcio
96	0	1620	13.5	247	3	0	0	6.02	0	10	0	0	0	1.3	3	0	0	0	0	0	0	6	curium	Cm	66	Rare Earth	f	M	c·rio
97	0	1620	14	247	3	0	0	6.23	0	10	0	0	0	1.3	3	4	0	0	0	0	0	9	berkelium	Bk	61	Rare Earth	f	M	berquÚlio
98	0	1170	0	251	0	0	0	6.3	0	10	0	0	0	1.3	3	0	0	0	0	0	0	11	californium	Cf	60	Rare Earth	f	M	calif¾rnio
99	0	1170	0	252	3	0	0	6.42	0	10	0	0	0	1.3	3	0	0	0	0	0	0	11	einsteinium	Es	58	Rare Earth	f	M	einstÛnio
100	0	1130	0	257	3	0	0	6.5	0	10	0	0	0	1.3	3	0	0	0	0	0	0	7	fermium	Fm	58	Rare Earth	f	M	fÚrmio
101	0	1800	0	258	3	0	0	6.58	0	10	0	0	0	1.3	3	0	0	0	0	0	0	11	mendelevium	Md	55	Rare Earth	f	M	mendelÚvio
102	0	1100	0	259	3	0	0	6.65	0	10	0	0	0	1.3	3	2	0	0	0	0	0	8	nobelium	No	52	Rare Earth	f	M	nobÚlio
103	0	1900	0	260	3	0	0	0	0	10	0	0	0	0	3	0	0	0	0	0	0	10	lawrencium	Lr	49	Rare Earth	d	M	lawrÛncio
104	0	0	0	261	0	0	0	0	0	0	0	0	0	0	4	0	0	0	0	0	0	13	rutherfordium	Rf	46	Transition Metal	d	M	rutherf¾rdio
105	0	0	0	262	0	0	0	0	0	0	0	0	0	0	5	0	0	0	0	0	0	7	hahnium	Ha	43	Transition Metal	d	M	hÔhnio
106	0	0	0	263	0	0	0	0	0	0	0	0	0	0	6	0	0	0	0	0	0	10	seaborgium	Sg	36	Transition Metal	d	M	
107	0	0	0	262	0	0	0	0	0	0	0	0	0	0	7	0	0	0	0	0	0	7	hassium	Hs	34	Transition Metal	d	M	
108	0	0	0	265	0	0	0	0	0	0	0	0	0	0	8	0	0	0	0	0	0	7	bohrium	Bh		Transition Metal	d	M	b¾hrio
109	0	0	0	266	0	0	0	0	0	0	0	0	0	0	9	0	0	0	0	0	0	10	meitnerium	Mt	28	Transition Metal	d	M	meitnÚrio
110	0	0	0	0	0	0	0	0	0	0	0	0	0	0	10	0	0	0	0	0	0	10	ununnilium	Uun		Transition Metal	d	M	
\.


--
-- PostgreSQL database dump complete
--


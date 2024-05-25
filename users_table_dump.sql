--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    users_name character varying(255),
    email character varying(100),
    location_of_user character varying(255),
    profile_url text NOT NULL,
    estimated_net_worth numeric(12,2),
    estimated_age integer,
    phone_number character varying(20),
    address character varying(255),
    approved character varying(20),
    website character varying(255)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, users_name, email, location_of_user, profile_url, estimated_net_worth, estimated_age, phone_number, address, approved, website) FROM stdin;
3	Jeff Papows	\N	Gloucester, MA	https://www.linkedin.com/in/jeffpapows?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABeeQngBydSqXe-D1qA01daRWPzT7TmWaw8	\N	\N	\N	\N	\N	\N
4	Saranne Winfield	\N	Lebanon, TN	https://www.linkedin.com/in/saranne-winfield-a76b7421?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAASfK_oBaN3G2YX5C1dyCL_8MwdN3sYh_po	\N	\N	\N	\N	\N	southernstarrs.org
5	John McGraw	\N	Las Vegas, NV	https://www.linkedin.com/in/jomcgraw?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAACy3hMB2DvxAwZ3KgibOO0oLxRnaAqBkLo	\N	\N	\N	\N	\N	equestrianlife.com
6	ray thomas	\N	Jackson, NJ	https://www.linkedin.com/in/ray-thomas-b5a87224?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAUcavYBMtuqSrIAUDHuOb-f3ZhmR3PV6gg	\N	\N	\N	\N	\N	synvet.eu
8	Jessica Jones	\N	Village of Garden City, NY	https://www.linkedin.com/in/jessicawjones?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAA5MXEByixJZNfUS7W7zmaoImLSJgHGIDQ	\N	\N	\N	\N	\N	\N
9	Natalia G.	\N	Washington, DC	https://www.linkedin.com/in/natalia-g-47a65a179?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACpG8x4Bq5dIqrqxWazZCe4gcNkJWrnJtMw	\N	\N	\N	\N	\N	\N
10	Julia Conn	\N	Washington, DC	https://www.linkedin.com/in/julia-conn-4b0680203?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADPkAsQBvhrYHbvcPKruC_41mQh63tgQZhg	\N	\N	\N	\N	\N	dogboneperformance.com
11	Celine Halioua	\N	San Francisco, CA	https://www.linkedin.com/in/celinehh?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABmXo_MBYM3BreyMlC1bBGZ9ygnNbL85iow	\N	\N	\N	\N	\N	\N
13	Ray Barnidge 5,500+	\N	Elmer, LA	https://www.linkedin.com/in/wetrs?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAEymZ8BHLL5iuxSVHFD04WlkwvxLrufLRM	\N	\N	\N	\N	\N	\N
14	Lucinda Fanta	\N	Gates Mills, OH	https://www.linkedin.com/in/lucinda-fanta-37b333145?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACMcPU8BZnFcy9YaCQJxefRXnZDHY02fcv0	\N	\N	\N	\N	\N	\N
15	Mauricio Gonzalez	\N	Houston, TX	https://www.linkedin.com/in/mauricio-gonzaleznajera?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAALb9wB3QMfR4osKODA6JB84kdvMeIfQ0Q	\N	\N	\N	\N	\N	\N
17	Michael F. Jorewicz	\N	Houston, TX	https://www.linkedin.com/in/michael-f-jorewicz-25345b1?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAA-oJ8B26MZQZwpcBA9sNdOFuwUQlfjEu0	\N	\N	\N	\N	\N	\N
18	Mary Claiborne	\N	Houston, TX	https://www.linkedin.com/in/mary-claiborne-309ba91a?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAQXjHkBHWAA7qhSQ_Elpi2cowGM_fGiP7w	\N	\N	\N	\N	\N	\N
19	Karina L.	\N	Houston, TX	https://www.linkedin.com/in/krinl11?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAABo5GMBG5gDvHU1rhgUUCtuOoBIci2nymQ	\N	\N	\N	\N	\N	\N
20	Brian Sambirsky	\N	Houston, TX	https://www.linkedin.com/in/briansambirsky?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAABQ0PIB2B9xE7cvbdlbkAe4PSGOk4AvHEU	\N	\N	\N	\N	\N	\N
21	Taft Singletary, MS	\N	Houston, TX	https://www.linkedin.com/in/taft-singletary?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAB7bI6ABs6jOlP3yag9zXtdKnj4BHxcdQvg	\N	\N	\N	\N	\N	\N
22	Justin Dunlap	\N	Houston, TX	https://www.linkedin.com/in/justin-dunlap-52a34b191?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAC0URTIBuTIrd21bzs2xAmbnMDa71xVRovc	\N	\N	\N	\N	\N	jmd185.wixsite.com/website/experience
23	Dustin Watson	\N	Baltimore, MD	https://www.linkedin.com/in/dustinwatson?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAEO0oYBJzatipbRpG6NkEyRdS3iu4Gs284	\N	\N	\N	\N	\N	inplace-design.com
25	Melinda Genitempo	\N	Houston, TX	https://www.linkedin.com/in/melindagenitempo?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAGcGlIBMTh7baPNq9IM2B4LfII582RN16g	\N	\N	\N	\N	\N	\N
26	Andrea Allison	\N	Houston, TX	https://www.linkedin.com/in/andreameekapps?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAv7YJUBxA2UkkReDtRtizJNSwDHrG2jov4	\N	\N	\N	\N	\N	\N
27	Robert Lilljedahl	\N	Houston, TX	https://www.linkedin.com/in/robert-lilljedahl-9a15726?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAEmpgkB2NRBj00oHS5knvb88xm4bD0NZ4U	\N	\N	\N	\N	\N	\N
29	Sorell Long	\N	Houston, TX	https://www.linkedin.com/in/sorell?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAA2ZiIBOIZstCAqqnxn2-9k_DJMNkp7Aqc	\N	\N	\N	\N	\N	careers.chevron.com
30	Chari Hust, BSN	\N	Houston, TX	https://www.linkedin.com/in/chari-hust-bsn-3a592639?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAglSK0BwnbkrtJfp3YKR9JVbQE2iZTDHFo	\N	\N	\N	\N	\N	\N
31	Erin McFarlane	\N	Houston, TX	https://www.linkedin.com/in/erin-mcfarlane?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAPt-DYBalqk-e4jMtDt2nq9RlyrCsvMY1E	\N	\N	\N	\N	\N	\N
32	Laura Manning Stokes	\N	Kemah, TX	https://www.linkedin.com/in/lauramanningstokes?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAECnIIB7dznF4C_dJnWTo5_DMFxXPZoAcs	\N	\N	\N	\N	\N	\N
33	Jordyn (Cooper) Ensell	\N	Houston, TX	https://www.linkedin.com/in/jordynensell?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABLTYyAB5WtPls-Ef4aoPNl2CNm-BfmderI	\N	\N	\N	\N	\N	\N
35	Natalia G.	\N	Washington, DC	https://www.linkedin.com/in/natalia-g-47a65a179/	\N	\N	\N	\N	\N	\N
36	Lucinda Fanta	\N	Gates Mills, OH	https://www.linkedin.com/in/lucinda-fanta-37b333145/	\N	\N	\N	\N	\N	\N
37	Don Bielak	\N	Philadelphia, PA	https://www.linkedin.com/in/don-bielak-193bb9a/	\N	\N	\N	\N	\N	monetran.com/
38	Jessica Jones	\N	Village of Garden City, NY	https://www.linkedin.com/in/jessicawjones/	\N	\N	\N	\N	\N	\N
39	Jeff Papows	\N	Gloucester, MA	https://www.linkedin.com/in/jeffpapows/	\N	\N	\N	\N	\N	\N
40	Emi Dawson	\N	Pittsburgh, PA	https://www.linkedin.com/in/emiadawson/	\N	\N	\N	\N	\N	\N
41	Regina Y.	\N	Cambridge, MA	https://www.linkedin.com/in/reginazye/	\N	\N	\N	\N	\N	\N
43	Devin Jopp	\N	Vienna, VA	https://www.linkedin.com/in/devinjopp?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAACrPD0BDwsFYfJl7COWZmXIFGAk-NJ9xMI	\N	\N	\N	\N	\N	\N
44	Lou Jacobs	\N	Buffalo, NY	https://www.linkedin.com/in/loujacobs?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABEKezcB3udQ1-M7a6bV7kvy28I9NXwZYb4	\N	\N	\N	\N	\N	\N
45	Katherine Wheeler	\N	Lexington, KY	https://www.linkedin.com/in/katherine-wheeler-7b14b915?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAMZfDUBKp14zyTQ4qm5_6232OcwGfjlT6I	\N	\N	\N	\N	\N	dappleup.com
46	Joy Ditto	\N	Washington, DC	https://www.linkedin.com/in/joy-ditto?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAADNn_cBCqSRkqVznCmyB9tOVWoxoRuKVS8	\N	\N	\N	\N	\N	joydittoconsulting.com
48	Victoria (Torie) Ludwin	\N	Houston, TX	https://www.linkedin.com/in/victoria-ludwin?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAHe-b8B-HdEsn8yPcMbq2COSzZBc1a1X28	\N	\N	\N	\N	\N	\N
49	Annette (Luther) Zylberman	\N	Houston, TX	https://www.linkedin.com/in/annette-zylberman-cpa?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAt4mpsBeMci0t1gdYRhXjkTrXdwglIxvls	\N	\N	\N	\N	\N	\N
50	Lana Claire Ives	\N	Darien, CT	https://www.linkedin.com/in/lana-claire-ives-47627459?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAxRvJoBIQorB7g5iC37V4BVdh_ws1phcPY	\N	\N	\N	\N	\N	\N
61	\N	\N	\N	https://www.linkedin.com/in/crystalshepard?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAA3vGHUBDgIkQi0la9arFTEuH6WRoHpCIzs	\N	\N	\N	\N	\N	\N
62	\N	\N	\N	https://www.linkedin.com/in/samantha-kate-johnson-2502591ab?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADD7GxwBTNSZRnY_9pouLHmz6sc-G225Z9k	\N	\N	\N	\N	\N	\N
63	\N	\N	\N	https://www.linkedin.com/in/marketingdireccionsofiagambara?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAA4BsywBm2fnsVBF4b9rLcBB3zOPRNGOFyM	\N	\N	\N	\N	\N	\N
64	\N	\N	\N	https://www.linkedin.com/in/judy-onomivbori-539a97?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAApAz0BKjVBoPujjXU7oNa7HRv_EKhGf8c	\N	\N	\N	\N	\N	\N
65	\N	\N	\N	https://www.linkedin.com/in/lorichampion?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAACB_n8BA_Xv7yP6tZFRmy3VwZXaBDIZOHU	\N	\N	\N	\N	\N	\N
66	\N	\N	\N	https://www.linkedin.com/in/alex-de-aguiar-reuter-082a0b1a?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAQQoqIBMG8yC3OlRSMjBX5IVijruH2FAbY	\N	\N	\N	\N	\N	\N
67	\N	\N	\N	https://www.linkedin.com/in/jeremy-robinson-rp1texas?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABwVvIsB4bN-Lsou1kKpk6x08RMBoSIxUb0	\N	\N	\N	\N	\N	\N
68	\N	\N	\N	https://www.linkedin.com/in/sharath-k-chandra?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABuXbLsB2g98xkLGvUQ4WZYNruMKaWe6pcY	\N	\N	\N	\N	\N	\N
69	\N	\N	\N	https://www.linkedin.com/in/emily-frost-37894455?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAu1HQwB1HPRu1A3CNtErtFRuYFpJNZbdac	\N	\N	\N	\N	\N	\N
70	\N	\N	\N	https://www.linkedin.com/in/janicejamailgarvis?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAMaY0UByNb0QL4QlJS_w0GoULv6FcG0JS8	\N	\N	\N	\N	\N	\N
71	\N	\N	\N	https://www.linkedin.com/in/adil-khan-dmseo?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAC1QYlQBwXg7V3v7aDOZdDjlOW2nYXWeSXs	\N	\N	\N	\N	\N	\N
72	\N	\N	\N	https://www.linkedin.com/in/amal-al-saadi-21993528?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAXVQfUBX07VwnOamrphRDH6OsTopjK0070	\N	\N	\N	\N	\N	\N
73	\N	\N	\N	https://www.linkedin.com/in/meganoliviaebel?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAdfQvgBQeOz27Q7RdEMv2WQkp_cXsLwzGQ	\N	\N	\N	\N	\N	\N
74	\N	\N	\N	https://www.linkedin.com/in/henry-morgan-iii-48691b39?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAglGeYBJGvj7uFQ6JF5FpE62Sogn527IGk	\N	\N	\N	\N	\N	\N
75	\N	\N	\N	https://www.linkedin.com/in/stephanie-kim-631b821ba?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADMTPQUBOT4c4yvC7Pw1RfTXdVHxBXT3Ez4	\N	\N	\N	\N	\N	\N
76	\N	\N	\N	https://www.linkedin.com/in/tina-metting-bsc-csm-b776723?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAChwwsBoSZMUHBmbR3Og7UuIsTufjojOUo	\N	\N	\N	\N	\N	\N
77	\N	\N	\N	https://www.linkedin.com/in/joseph-kellum?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACWxL_IB43YlECV8M4tJh3VtDeULAkEW4HQ	\N	\N	\N	\N	\N	\N
78	\N	\N	\N	https://www.linkedin.com/in/genevieve-blanchard?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAECg934BYfhX2Bcau9AM7L_q_Di8BUIc99w	\N	\N	\N	\N	\N	\N
79	\N	\N	\N	https://www.linkedin.com/in/katherine-breunig-06581212?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAKcns0Bq373suoqGVlrlbKB7GAc0-LuVFA	\N	\N	\N	\N	\N	\N
80	\N	\N	\N	https://www.linkedin.com/in/chandler-hopper-933255113?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABxVw_cBeE8ug3_xqcIVRQAeeqsqQLcw2xM	\N	\N	\N	\N	\N	\N
81	\N	\N	\N	https://www.linkedin.com/in/jmeyrat?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAD59mgBk_ifAxc52LYRyLsjZFZ5ImJx1J4	\N	\N	\N	\N	\N	\N
82	\N	\N	\N	https://www.linkedin.com/in/jamie-anderson-om?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABPAMicBC3Xe201x228VhkwP75WkfwTx_28	\N	\N	\N	\N	\N	\N
83	\N	\N	\N	https://www.linkedin.com/in/laurenahogan?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAxEMhwBZPH7RD6-DdWuRwGjbmYpGlPQ4MQ	\N	\N	\N	\N	\N	\N
84	\N	\N	\N	https://www.linkedin.com/in/ericseversontalentinnovator?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAC2HDMBSJjy5PW1T7ac5RblJHR8fVIxUzY	\N	\N	\N	\N	\N	\N
85	\N	\N	\N	https://www.linkedin.com/in/javier-oliver-83269444?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAlbAKYBa-HAj7HDLnEXQO0wVtdjX-Fm-vQ	\N	\N	\N	\N	\N	\N
86	\N	\N	\N	https://www.linkedin.com/in/bernard-uechtritz-b7045314?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAALp38QBNlF8_XgLy6K3f0_mF7dR-qH8t2U	\N	\N	\N	\N	\N	\N
87	\N	\N	\N	https://www.linkedin.com/in/jacquelinepotwora?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADLjY1MBo0H9odfRUeC1q6bbAtbARa1IOWE	\N	\N	\N	\N	\N	\N
88	\N	\N	\N	https://www.linkedin.com/in/alexandrabgamez?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABaC_rQBpmDgJCkgNLc8MJAkt7dMDZcMyUg	\N	\N	\N	\N	\N	\N
89	\N	\N	\N	https://www.linkedin.com/in/hailey-johns-827a3a292?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAEb9Ex8Byd5BxP_jnhZyNrHklM86qC18OvA	\N	\N	\N	\N	\N	\N
90	\N	\N	\N	https://www.linkedin.com/in/livvanlanen?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAA_OfV8BqC5U9doq57ZwvZSIBZYC7wKJwO8	\N	\N	\N	\N	\N	\N
91	\N	\N	\N	https://www.linkedin.com/in/bruce-birdsong-97ab157?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAFpLC4BmAB3ZysNB0axL9yT_y6ST81d5DA	\N	\N	\N	\N	\N	\N
92	\N	\N	\N	https://www.linkedin.com/in/community-katie?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABafmwwBr7Gk84bsN2Q7E-Gdpkat4_Q9PgA	\N	\N	\N	\N	\N	\N
93	\N	\N	\N	https://www.linkedin.com/in/anastasia-bobilev-phd?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAC0y3OIB3GmqHSQLhvh4XpfGVfCDRPwRqKQ	\N	\N	\N	\N	\N	\N
94	\N	\N	\N	https://www.linkedin.com/in/paige-browning-otr-otd-12b51911b?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAB3MenMBLuHO9T72FVytuElBGeYSB0TWlPk	\N	\N	\N	\N	\N	\N
95	\N	\N	\N	https://www.linkedin.com/in/benjamin-dever-mendenhall-3ba2a1213?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADX4Ov4BTT7zfPCAHKAnPfwKh5GzZvBMiLs	\N	\N	\N	\N	\N	\N
52	Wendy Davis	\N	Houston, TX	https://www.linkedin.com/in/wendy-davis-865a5646?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAnEGk0BxDVlCJ1dmYZZ0jJg-pomwyLcKQ0	\N	\N	\N	\N	\N	aaacooper.com
53	Janine Iannarelli	\N	Houston, TX	https://www.linkedin.com/in/janine-iannarelli-778130?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAAEw0wBI9o8JtLNVZtC1afIFRzUTrL8ooo	\N	\N	\N	\N	\N	\N
55	Jean Huynh	\N	Houston, TX	https://www.linkedin.com/in/jeanhuynh?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACF3bRIBmqmS9c9NVHesMFxBbcG2Ze6-UGk	\N	\N	\N	\N	\N	\N
56	Michael Newhouse	\N	Houston, TX	https://www.linkedin.com/in/michael-newhouse-b5b0974?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAC5TrcBUuEoQt-xCZutMBzmTmFjlfJg2c8	\N	\N	\N	\N	\N	\N
57	Cori Willett	\N	Houston, TX	https://www.linkedin.com/in/cori-willett-01321035?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAdT-Q8BE3goFO-z2QikLMPN5a5lfvw-3GU	\N	\N	\N	\N	\N	\N
58	Alison Sewell	\N	Houston, TX	https://www.linkedin.com/in/alison-sewell-250a90a6?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABaVslwBM09h6hnmEpLMf4P5xbA1S6LA9KU	\N	\N	\N	\N	\N	alisonsewell.com/
59	Carolina L. Wetherall	\N	Houston, TX	https://www.linkedin.com/in/carolina-l-wetherall-a505a258?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAwweVwBzDJRYqSfTWKMzTBloAqN4-wLMlI	\N	\N	\N	\N	\N	\N
96	\N	\N	\N	https://www.linkedin.com/in/axelrebollar?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACnWO0IBrTweZJ8k3eptnt-hOkty8YD6WzU	\N	\N	\N	\N	\N	\N
97	\N	\N	\N	https://www.linkedin.com/in/catherine-koltun?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAArCxHYBIoAld2Li4hKay0s_noHLZmSvwxA	\N	\N	\N	\N	\N	\N
98	\N	\N	\N	https://www.linkedin.com/in/victoriaguajardo?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADTrztYBkbC9LGG8iksZa6iY-dfrB-6ZeD8	\N	\N	\N	\N	\N	\N
99	\N	\N	\N	https://www.linkedin.com/in/diyachandra?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACtdOmkBiUycVAwXez76sj4NzaYf6zX1fCU	\N	\N	\N	\N	\N	\N
100	\N	\N	\N	https://www.linkedin.com/in/shannon-hogue?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABt2bpIBi4LjECi38tmhUyIA22GQ1krJ_-U	\N	\N	\N	\N	\N	\N
101	\N	\N	\N	https://www.linkedin.com/in/drmarykelly?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAEuGR4BryoO7a7SgQHXnI7ACEykR6P2bzY	\N	\N	\N	\N	\N	\N
102	\N	\N	\N	https://www.linkedin.com/in/haley-lewis-043ba3111?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABweUnMByafJZ76pUsdgLtAnrBiCv8PvRzU	\N	\N	\N	\N	\N	\N
103	\N	\N	\N	https://www.linkedin.com/in/trisha-porzycki?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACLotCcBiOMMzwy93lELJ8E6VZvnmEtQwRk	\N	\N	\N	\N	\N	\N
104	\N	\N	\N	https://www.linkedin.com/in/cynthiaminchillo?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAK1BSsBYh_dImMhNcGEGAL6fRNQlkmq0z4	\N	\N	\N	\N	\N	\N
105	\N	\N	\N	https://www.linkedin.com/in/ahmedyazdani?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAC-GrHQBgwRLYzBdqWkMY11x-ZuKnF8SduY	\N	\N	\N	\N	\N	\N
106	\N	\N	\N	https://www.linkedin.com/in/colton-valentine?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACP44joByWz5qdcGn4G0Fmv-XLfkwpgSVn8	\N	\N	\N	\N	\N	\N
107	\N	\N	\N	https://www.linkedin.com/in/elizabethmblake?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABgm6VoBNGgFbhA42lfHPkPYGBf7ZGz09LM	\N	\N	\N	\N	\N	\N
108	\N	\N	\N	https://www.linkedin.com/in/reya-resendiz?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADciQ8UBs6cp-CcMveVJKzIDt-UfvIxsZZQ	\N	\N	\N	\N	\N	\N
109	\N	\N	\N	https://www.linkedin.com/in/mandyoram?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAPkz7MBoklPvE1NgNaFyXWG7BagsXdp5xE	\N	\N	\N	\N	\N	\N
110	\N	\N	\N	https://www.linkedin.com/in/kevinjxu?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABIUBSwBPQmhB1kaknR-qiSrIR6IqSRV2Rc	\N	\N	\N	\N	\N	\N
111	\N	\N	\N	https://www.linkedin.com/in/amanda-rose-leblanc?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAbeJbMBTq_COYwSwqHX0q90MHh4Vw3Vdq4	\N	\N	\N	\N	\N	\N
112	\N	\N	\N	https://www.linkedin.com/in/krystina-sterne-7822a532?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAbOSBIB4VGlQ1f8rMhywN3s0xTuAFaasYY	\N	\N	\N	\N	\N	\N
113	\N	\N	\N	https://www.linkedin.com/in/nicole-o-hagen-sandoval?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAABVgtABxtENq_kRUnr1hBvGqnrpCepSrcs	\N	\N	\N	\N	\N	\N
114	\N	\N	\N	https://www.linkedin.com/in/michael-kornman-717a1a2?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAACBsIMBmjabk3fy9peXA9o-Wmmxbfvhy68	\N	\N	\N	\N	\N	\N
115	\N	\N	\N	https://www.linkedin.com/in/hannahklinedinst?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAB0H78oB6mflw8wh-lqhAR1OBqyCOT7BVeY	\N	\N	\N	\N	\N	\N
116	\N	\N	\N	https://www.linkedin.com/in/fanna-easter-cpdt-ka-kpa-ctp-csat-cdbc-28b8105a?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAyUEosBHWmsY0ctM8X2hqiSCAWjWxVIcI0	\N	\N	\N	\N	\N	\N
117	\N	\N	\N	https://www.linkedin.com/in/daniel-peel-47590121?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAASVRVkBkhmcc-SPrig5ueCgoJvGGgcr3ew	\N	\N	\N	\N	\N	\N
118	\N	\N	\N	https://www.linkedin.com/in/james-glew?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABeainIBzbFBRd3z_XfuCjGOAXuZXMeg9Uk	\N	\N	\N	\N	\N	\N
119	\N	\N	\N	https://www.linkedin.com/in/snapprod?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAAdEEwBWfcGAb5iWtaBaHAFxeJ84zPAXag	\N	\N	\N	\N	\N	\N
120	\N	\N	\N	https://www.linkedin.com/in/anna-ramundo-63037232?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAbRDAQBUIgEAwWMSS3hjU4xExLIpHfnvY0	\N	\N	\N	\N	\N	\N
121	\N	\N	\N	https://www.linkedin.com/in/noahgraeme?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAxBeIsBKJm1EijBtNMcwph4Zwn8UhrbTfU	\N	\N	\N	\N	\N	\N
122	\N	\N	\N	https://www.linkedin.com/in/april-mccarra-dcis-7867535?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAEAEZYBKeo7uGZ8b3lHhGHgcQavTsNsY10	\N	\N	\N	\N	\N	\N
123	\N	\N	\N	https://www.linkedin.com/in/melaniegraf?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAxEJ6ABoWGeVca3phTtk1iMWte79w1ENTA	\N	\N	\N	\N	\N	\N
124	\N	\N	\N	https://www.linkedin.com/in/aerithspaulding?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABYCRgMBbe5rL8ZB8iSDX0fGcRxTTAA5vho	\N	\N	\N	\N	\N	\N
125	\N	\N	\N	https://www.linkedin.com/in/brookemrtn?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABZWNXkB5X7HVBQJx3ihBDoUFK6bWoDnZPc	\N	\N	\N	\N	\N	\N
126	\N	\N	\N	https://www.linkedin.com/in/terrycooke?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAAMVCMBZvCN13oJhHEuA6ePEsFbtK6UXF0	\N	\N	\N	\N	\N	\N
127	\N	\N	\N	https://www.linkedin.com/in/gesingleton?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAAVVJMBsJPIi26Sc8dUk6cflI5XDlAdyHY	\N	\N	\N	\N	\N	\N
128	\N	\N	\N	https://www.linkedin.com/in/marc-brutten-b06022110?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABvEdbYBv557wXvLjXXxd_cAaOw-jw_ta_0	\N	\N	\N	\N	\N	\N
129	\N	\N	\N	https://www.linkedin.com/in/jordynnwynn?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAmJ9uMBr1vpAwoLNCQ9BguT3lb9IwDoYFQ	\N	\N	\N	\N	\N	\N
130	\N	\N	\N	https://www.linkedin.com/in/tvisha-gangwani?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABhZ7t0BBOCIXrYBvdOk0GNmPWB0Lyleru8	\N	\N	\N	\N	\N	\N
131	\N	\N	\N	https://www.linkedin.com/in/ashcasselman?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAEzJVQB7XEXa4bAUa_yYYL2m6jzJ8zIP6o	\N	\N	\N	\N	\N	\N
132	\N	\N	\N	https://www.linkedin.com/in/jessica-beyer-harrell-1b891130?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAaKxNwBuv0XztiaHpJZRTxFsTeqdIL_gUA	\N	\N	\N	\N	\N	\N
133	\N	\N	\N	https://www.linkedin.com/in/callie-mirsky?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAA3RkvcBKRw12ZICd-x_mfrdMaHd-hPencI	\N	\N	\N	\N	\N	\N
134	\N	\N	\N	https://www.linkedin.com/in/nancy-stratton-45b94a35?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAdvxgcBW4fCjie9WR3p4GzZqSShdHLageM	\N	\N	\N	\N	\N	\N
135	\N	\N	\N	https://www.linkedin.com/in/jwc2021?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAtEzxUB6DsDiFs2OZSKMqZwaqrwRYZI1Pg	\N	\N	\N	\N	\N	\N
136	\N	\N	\N	https://www.linkedin.com/in/lisafalzone?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAEuin8BMrtp4SgErES7ri8yXd5hMcRq1A0	\N	\N	\N	\N	\N	\N
137	\N	\N	\N	https://www.linkedin.com/in/nicolesnell?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAFPdSkB_z3maxvmhAdr1fPpMCOR18J7uuA	\N	\N	\N	\N	\N	\N
138	\N	\N	\N	https://www.linkedin.com/in/sunnysaurabh?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAADb6a0BT283O4lR8FHnElsNoCFFRnmbt3w	\N	\N	\N	\N	\N	\N
139	\N	\N	\N	https://www.linkedin.com/in/ashleyterrell949?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAwadT4BV7WRA-pvuiTtgYcaO-3LaMZgXfo	\N	\N	\N	\N	\N	\N
140	\N	\N	\N	https://www.linkedin.com/in/kassyperry?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAABTURwBrS46rGOhnFo6JL94qQONexQtr64	\N	\N	\N	\N	\N	\N
141	\N	\N	\N	https://www.linkedin.com/in/eddelfs?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAACBhFMBKvBNVeXKjYr6TUb0Nuu01D041fU	\N	\N	\N	\N	\N	\N
142	\N	\N	\N	https://www.linkedin.com/in/saigopal-nelaturi?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAACiHKEBcRZumStXRTM6iLcyQ78K_AOv0Uo	\N	\N	\N	\N	\N	\N
143	\N	\N	\N	https://www.linkedin.com/in/kayla-wells?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACH4qYsBvHUNuYWz_-gvw1wsQ3aFfygcl_I	\N	\N	\N	\N	\N	\N
144	\N	\N	\N	https://www.linkedin.com/in/jennylesser?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAHT05UB1WpjxEAUo8b9_mEmiinrCNgrNRg	\N	\N	\N	\N	\N	\N
145	\N	\N	\N	https://www.linkedin.com/in/lauren-hammond?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAD-uF-YBe_T9XJEhRdb_SEWG7oZnLczHXEk	\N	\N	\N	\N	\N	\N
146	\N	\N	\N	https://www.linkedin.com/in/simcha-lipton?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAA2smJ0BsvkJVv1ECIhOCtxXmlKMmONqDEM	\N	\N	\N	\N	\N	\N
147	\N	\N	\N	https://www.linkedin.com/in/mhworth?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAYIuZsBxz2Z-feqH2n4yoZV6C-gRPMidJI	\N	\N	\N	\N	\N	\N
148	\N	\N	\N	https://www.linkedin.com/in/lwatts?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAAZsGMBSa9VFhTXXvl4k9xTw8uMdnCejhQ	\N	\N	\N	\N	\N	\N
149	\N	\N	\N	https://www.linkedin.com/in/jamesboskovic?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAtwdZ0BzCO47NfpAaVoLAoHWhvlIX6iIL4	\N	\N	\N	\N	\N	\N
150	\N	\N	\N	https://www.linkedin.com/in/jolinemann?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABTCDigBF2qv2YbGodfGVc3GlzDEAJLVowI	\N	\N	\N	\N	\N	\N
151	\N	\N	\N	https://www.linkedin.com/in/mary-davis-lakefield-rnc-ph-d-51863377?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABBKAiQB0EpfpGpwcrqNK94i-BH36GsengI	\N	\N	\N	\N	\N	\N
152	\N	\N	\N	https://www.linkedin.com/in/claire-stratton-484a60149?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACPt8KQB1GEgnD_VGO5SFpa3sfWA7p4VuRI	\N	\N	\N	\N	\N	\N
153	\N	\N	\N	https://www.linkedin.com/in/moummarnawafleh?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAC5KKSYBJRdg2z1D0uCeNkFiu-zqUoiroxw	\N	\N	\N	\N	\N	\N
154	\N	\N	\N	https://www.linkedin.com/in/rbenadada?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAXXClcByWwrDu_QXcaiF6tHZY7MzzV0P0M	\N	\N	\N	\N	\N	\N
155	\N	\N	\N	https://www.linkedin.com/in/mayamarkovich?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAFSGJABaXM9RMlRrhuWfonE3ZiliG-S8U0	\N	\N	\N	\N	\N	\N
156	\N	\N	\N	https://www.linkedin.com/in/whitneyhischier?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAF__A0BAEHfNCxeJfgy5s0cN7gZWUR9UGc	\N	\N	\N	\N	\N	\N
157	\N	\N	\N	https://www.linkedin.com/in/debbie-c-164a92?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAAo31wBVluFumbaitPIf4Izjut5oWRb6x8	\N	\N	\N	\N	\N	\N
158	\N	\N	\N	https://www.linkedin.com/in/rodriguez-bea?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAEFTn9oBRvIZAjDzvu3sA7_ff2fxHGc65xo	\N	\N	\N	\N	\N	\N
159	\N	\N	\N	https://www.linkedin.com/in/elizabeth-goodwin-welborn-8322708?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAF2U6YB0OWu4yCgy7g8liQwSSBY3trdqEI	\N	\N	\N	\N	\N	\N
160	\N	\N	\N	https://www.linkedin.com/in/victoriayoung?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAEcT68BtStDEtOwJemgQTa4_5jS8_VeSYo	\N	\N	\N	\N	\N	\N
161	\N	\N	\N	https://www.linkedin.com/in/miriguo?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAEg9yQBYOrKZHS8XKPsZGlYK6XV-wcA8Yo	\N	\N	\N	\N	\N	\N
162	\N	\N	\N	https://www.linkedin.com/in/barrymccardel?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAK1q3YBTed1DkWQoi88AeyXdWza_oZLaIc	\N	\N	\N	\N	\N	\N
163	\N	\N	\N	https://www.linkedin.com/in/grace-rankin?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABylvcsBu73MINtqLVgotZIskNANww390LI	\N	\N	\N	\N	\N	\N
164	\N	\N	\N	https://www.linkedin.com/in/jenlaloup?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAGuiTMBz2XhLNROQ87qmSm36U8jKV5p_cI	\N	\N	\N	\N	\N	\N
165	\N	\N	\N	https://www.linkedin.com/in/shaurya-singh-2a71b81b7?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADJlrp8BNP0TiRBVSAtyjYdh-C8z8h7OR2A	\N	\N	\N	\N	\N	\N
166	\N	\N	\N	https://www.linkedin.com/in/ariel-ganz?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAsZRIkB1LaU1zc_GiTcPS-3tJKlkws-HPk	\N	\N	\N	\N	\N	\N
167	\N	\N	\N	https://www.linkedin.com/in/danielaristimuno?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAMZwssBi3YcCa57diw7Q1KoBYEnWLgglqM	\N	\N	\N	\N	\N	\N
168	\N	\N	\N	https://www.linkedin.com/in/audreycui?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAC1lCB0BmZjv6-_cidCFWVZbvAaWWV4Cki0	\N	\N	\N	\N	\N	\N
169	\N	\N	\N	https://www.linkedin.com/in/ryan-kavanaugh-952615183?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACtW8A4BWW7P9GBReQlUEGDdF9GsuLy5cFc	\N	\N	\N	\N	\N	\N
170	\N	\N	\N	https://www.linkedin.com/in/dakota-xentaras-06131165?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAA3ADAkBUcW8YsmPL8P4FCTQlg93BGzdCUA	\N	\N	\N	\N	\N	\N
171	\N	\N	\N	https://www.linkedin.com/in/bradley-thomason-583a1b6?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAE39nMBNpqYt90BWveeka4_6ALi2jM4ndA	\N	\N	\N	\N	\N	\N
172	\N	\N	\N	https://www.linkedin.com/in/romavanderwalt?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAmluTQBNKnDnkjWc-hruhU15GBoJNgs2Hk	\N	\N	\N	\N	\N	\N
173	\N	\N	\N	https://www.linkedin.com/in/grace-kulawiak-granda-ms-3a16a08?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAGGdCkBscM-twAd8Ebd3jo2BlNTjDTi7hc	\N	\N	\N	\N	\N	\N
174	\N	\N	\N	https://www.linkedin.com/in/joshzollinger?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAFEat0B21bP8PRs8v6AZGXPrgAhmDgmryM	\N	\N	\N	\N	\N	\N
175	\N	\N	\N	https://www.linkedin.com/in/ahmad-zafar-6a753a156?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACV0Vl8BBiK9CMFjbCnsb0HRU5mvR47TaD8	\N	\N	\N	\N	\N	\N
176	\N	\N	\N	https://www.linkedin.com/in/elizabethmgore?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABKVoHAB2BNqDGNqw8YLmxmDSrrAizPU4b8	\N	\N	\N	\N	\N	\N
177	\N	\N	\N	https://www.linkedin.com/in/linda-gacsko-29286678?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABCAMA4B9JdQ5Ny-Aq7mN-PyAJLxOwm0KG8	\N	\N	\N	\N	\N	\N
178	\N	\N	\N	https://www.linkedin.com/in/ahmedgaballah?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAADvyDkBQ1W8ssoWQtCfO3cdTiDXU18IfwI	\N	\N	\N	\N	\N	\N
179	\N	\N	\N	https://www.linkedin.com/in/annie-portland?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAu4EXwBHDypBh1i2c40Jv6yTMTUlpeMJbk	\N	\N	\N	\N	\N	\N
180	\N	\N	\N	https://www.linkedin.com/in/samantha-n-welch?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAD1nEXYB_GoC7Qim3OdOjVbE8gO6Zc--vU0	\N	\N	\N	\N	\N	\N
181	\N	\N	\N	https://www.linkedin.com/in/davidjsnodgrass?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAAIUaABupl5_Y1Ka-bLg5y3OwMLpQCXMYg	\N	\N	\N	\N	\N	\N
182	\N	\N	\N	https://www.linkedin.com/in/sydney-glickson?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACwP28kBmzr092Y6mb9DQD3_EFR2Z3ohbII	\N	\N	\N	\N	\N	\N
183	\N	\N	\N	https://www.linkedin.com/in/stephen-m-apatow-759529b?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAIJDvUBNfe0uxES_NTC8TJjMgsmvhZAbgo	\N	\N	\N	\N	\N	\N
184	\N	\N	\N	https://www.linkedin.com/in/almiraali8?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACGR8psBYsIqxWq1WgMLDaONvWHPDUsq9ig	\N	\N	\N	\N	\N	\N
185	\N	\N	\N	https://www.linkedin.com/in/molly-kaster?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACOwF78BpuXEw9D2wXGhI8_tBDi53_ebry0	\N	\N	\N	\N	\N	\N
186	\N	\N	\N	https://www.linkedin.com/in/tyvachon?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAPbxIcBF7nMf1OhqPzzusc9TPHvy96UXQA	\N	\N	\N	\N	\N	\N
187	\N	\N	\N	https://www.linkedin.com/in/claudeatam?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAEs_eQB-hjtTuZ39G3DB5rmPSYXvy6puu0	\N	\N	\N	\N	\N	\N
188	\N	\N	\N	https://www.linkedin.com/in/mattgerber?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAAGqhcBF701kJy7VKn2d1HblcPIHmnWv4U	\N	\N	\N	\N	\N	\N
189	\N	\N	\N	https://www.linkedin.com/in/bethjcarey?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAYI9DIBnecZ9_IVV5GEL1qjDj2g1bxbM70	\N	\N	\N	\N	\N	\N
190	\N	\N	\N	https://www.linkedin.com/in/omer-davidi-9685321b?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAQr8eABhCqbtSEro7_O3TI6MGogVgoUDGg	\N	\N	\N	\N	\N	\N
191	\N	\N	\N	https://www.linkedin.com/in/celine-tien-70828698?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABSvjHgBdoZYTZjlaQlSK9aKXntHdq3q-Z8	\N	\N	\N	\N	\N	\N
192	\N	\N	\N	https://www.linkedin.com/in/megan-kerby-3a3633254?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAD690WsBNDrponYN3Lyz5EDBwWWJvHDLa5w	\N	\N	\N	\N	\N	\N
193	\N	\N	\N	https://www.linkedin.com/in/maroliu?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAANpZCIBrvCV2uGN_9NJE-I9X6G5G976zKI	\N	\N	\N	\N	\N	\N
194	\N	\N	\N	https://www.linkedin.com/in/irenaking?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAB1n6dsBSpLDn539Iz_0CsjZF_p8z40KbXU	\N	\N	\N	\N	\N	\N
195	\N	\N	\N	https://www.linkedin.com/in/rose-xi?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAnmLTkBz6aeKUY5C9rmgQw1OiA7UvjoRDY	\N	\N	\N	\N	\N	\N
196	\N	\N	\N	https://www.linkedin.com/in/scottatomlinson?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAFK6JsBKOFcIZ8sT7Iv7oWFMj_E1t3x5PI	\N	\N	\N	\N	\N	\N
197	\N	\N	\N	https://www.linkedin.com/in/devinjopp/	\N	\N	\N	\N	\N	\N
198	\N	\N	\N	https://www.linkedin.com/in/thomas-a-duckenfield-iii-2095831/	\N	\N	\N	\N	\N	\N
199	\N	\N	\N	https://www.linkedin.com/in/cclingman/	\N	\N	\N	\N	\N	\N
200	\N	\N	\N	https://www.linkedin.com/in/cinthiaane?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAADkjAQBNTIc3oSIW3ZHD-usMZcqecFVZNM	\N	\N	\N	\N	\N	\N
201	\N	\N	\N	https://www.linkedin.com/in/williamdanton?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAJvcHMBBqrpuI7IK-Mx1m54X3gwyVaXtT8	\N	\N	\N	\N	\N	\N
1	Saranne Winfield	\N	Lebanon, TN	https://www.linkedin.com/in/saranne-winfield-a76b7421/	\N	\N	\N	\N	\N	\N
28	Rita Mounir	ritou.mounir@gmail.com	Houston, TX	https://www.linkedin.com/in/ritamounir?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAACOmGTUBxvxbRwsePly4dBgMklpds-TCmfU	\N	\N	\N	\N	\N	\N
2	Russell Fomby	\N	Gainesville, TX	https://www.linkedin.com/in/russell-fomby-93298a24?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAUgvLYBd3yeqtk0XyWRzuGsabTk2ewxQgo	\N	\N	\N	\N	\N	kdequestrian.com
34	Laura Urbanelli	\N	Houston, TX	https://www.linkedin.com/in/laura-urbanelli-77938788?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABKQn40BZejxaAUwNhRVKhvB4BijeBr1ehw	\N	\N	\N	\N	\N	\N
7	Don Bielak	\N	Philadelphia, PA	https://www.linkedin.com/in/don-bielak-193bb9a?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAH1HL8BDzzk9g6T9Q5IObHjbGV6rdOLeT4	\N	\N	\N	\N	\N	monetran.com/
51	Robin Williams	\N	Houston, TX	https://www.linkedin.com/in/robinwilliams2?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAQgIBABYEAhiCy3NF1TMMeo_tiGA3hdIgU	\N	\N	\N	\N	\N	\N
12	Riesa Lakin	\N	City of New York, NY	https://www.linkedin.com/in/riesa-lakin-0217053?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAACjZdkB5yfux6qVrrvPlPsKWHQPHZ3Kl58	\N	\N	\N	\N	\N	\N
42	Natalie Mamou (McMahon)	\N	San Francisco Bay, CA	https://www.linkedin.com/in/natalie-mamou-mcmahon-7363ba59?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAxW9poByP8jxxEEEe9ynKmq6pk_QKR0La0	\N	\N	\N	\N	\N	\N
16	Sierra Patterson, P.G.	\N	Charlotte, NC	https://www.linkedin.com/in/sierra-patterson-p-g-06809a206?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADRWfNABSpHrYRQbSVk31dxaCo82D_vdsK4	\N	\N	\N	\N	\N	\N
54	Christopher Noessel	\N	San Francisco, CA	https://www.linkedin.com/in/chrisnoessel?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAAAZYYBa4Bwjvv1f3ALR7vgiwQLcThIV7A	\N	\N	\N	\N	\N	\N
24	Ana Saunders	\N	Houston, TX	https://www.linkedin.com/in/anasaunders?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABq1T-gBxzRIXY8DaL6wfpLq6lRqT29T9UY	\N	\N	\N	\N	\N	\N
47	Brianna Byrd	\N	Houston, TX	https://www.linkedin.com/in/brianna-byrd-9760651b1?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADFO3SoB_MtbHRuj4LoaXsY-YRODYvY0Zl4	\N	\N	\N	\N	\N	\N
60	Hannah Byatt	\N	Houston, TX	https://www.linkedin.com/in/hannah-byatt-12a394b8?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAABj5GLIBdh-RG7YHwFSi-iFxm9KSFsqan9I	\N	\N	\N	\N	\N	\N
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 201, true);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_profile_url_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_profile_url_key UNIQUE (profile_url);


--
-- PostgreSQL database dump complete
--


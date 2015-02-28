# -*- coding: utf-8 -*-
"""
Unit tests for pyjstat

"""

from pyjstat import pyjstat
import unittest
import json
from collections import OrderedDict


class TestPyjstat(unittest.TestCase):
    """ Unit tests for pyjstat """

    def setUp(self):
        """ Test data extracted from json-stat.org site """

        self.oecd_data = ('{"oecd":{"label":"Unemployment rate OECD countries'
                          '2003-2014","source":"Economic Outlook No 92 - '
                          'December 2012 - OECD Annual Projections","updated":'
                          '"2012-11-27","value":[5.943826289,5.39663128,'
                          '5.044790587,4.789362794,4.379649386,4.249093453,'
                          '5.592226603,5.230660289,5.099422942,5.224336088,'
                          '5.50415003,5.462866231,4.278559338,4.939707755,'
                          '5.152160612,4.727182858,4.399730726,3.813933625,'
                          '4.776912506,4.391591645,4.143587245,4.351345785,'
                          '4.695491708,4.745323313,8.158333333,8.4,'
                          '8.483333333,8.266666667,7.466666667,7.016666667,'
                          '7.891892855,8.283171959,7.175138783,7.381153404,'
                          '7.689552898,7.735442636,7.594616751,7.167833951,'
                          '6.748691501,6.307841105,6.049842626,6.146014664,'
                          '8.284689299,7.988900419,7.453609598,7.32358421,'
                          '7.169741525,6.88122705,9.5433848,10.00149582,'
                          '9.224422554,7.773166282,7.150623348,7.787221805,'
                          '10.80236438,8.121579077,7.104778251,6.477468723,'
                          '6.78101031,6.780198936,7.818066527,8.323638425,'
                          '7.922330988,7.142271671,5.316363283,4.391669598,'
                          '6.675050668,7.273107122,6.723482523,6.936394665,'
                          '7.242148075,7.135151601,5.344516646,5.516904324,'
                          '4.793715416,3.868296418,3.669496447,3.326692683,'
                          '5.821647379,7.191696186,7.313112408,7.544640558,'
                          '7.357364231,7.255659852,10.03010116,9.661753538,'
                          '7.899232972,5.905173373,4.659913473,5.601684952,'
                          '13.87805579,16.83438817,12.4576855,9.873121257,'
                          '9.116309666,8.74566981,9.017860131,8.80435787,'
                          '8.368797468,7.702632855,6.850344695,6.368216471,'
                          '8.269856093,8.381534292,7.774845319,7.722836877,'
                          '7.962718148,7.757742455,8.503978378,8.8650811,'
                          '8.882978134,8.835277292,8.009145174,7.384897537,'
                          '9.129199553,9.315864403,9.202432489,9.877166456,'
                          '10.66140443,10.91985917,9.134738857,9.829230121,'
                          '10.69442137,9.694756306,8.310233377,7.188163108,'
                          '7.429105355,6.757338631,5.752587233,5.28775372,'
                          '5.524081118,5.565600014,9.712526535,10.49281197,'
                          '9.849833119,8.890878396,8.276300402,7.653084476,'
                          '9.460314273,12.53058153,17.65238747,23.5737508,'
                          '26.6534591,27.2364419,5.860132523,6.096400087,'
                          '7.185491402,7.451740837,7.35706148,7.851089777,'
                          '10.0153875,11.14448405,10.92071597,11.12538821,'
                          '11.09958634,10.76358386,3.352836045,3.06335905,'
                          '2.590345651,2.878830234,2.301867378,2.990597714,'
                          '7.241470693,7.55861225,7.058807671,6.138731401,'
                          '5.393148124,5.128315309,4.739670964,4.539966682,'
                          '4.341850838,4.415526325,4.571302023,6.024123088,'
                          '11.81229736,13.62078809,14.51224844,14.79227286,'
                          '14.73886731,14.61076214,13.28016732,12.85704871,'
                          '11.29834866,10.47596715,9.147672881,7.728344307,'
                          '9.476560711,8.33683595,7.110513831,6.8731402,'
                          '7.359377644,6.93094611,8.444973801,7.996760207,'
                          '7.708360512,6.777043598,6.110290905,6.774113796,'
                          '7.800833899,8.41234985,8.438703909,10.55546863,'
                          '11.42167502,11.7584873,5.25125,4.717099486,'
                          '4.424423923,4.129376275,3.84841253,3.979750388,'
                          '5.068375853,5.058985674,4.592622773,4.399496241,'
                          '4.355894653,4.286733019,3.562065618,3.67219364,'
                          '3.734708533,3.450431799,3.233335111,3.15974989,'
                          '3.643064158,3.715763348,3.405129308,3.378067785,'
                          '3.618601827,3.397535556,3.304883869,3.710506994,'
                          '4.099797561,4.242014975,4.182611437,4.14500326,'
                          '5.431987487,5.778771292,5.627283477,6.078760003,'
                          '6.589474092,6.658818611,2.998805894,3.695332444,'
                          '3.540173119,3.550553518,3.672170595,3.949416134,'
                          '5.43621902,5.373117407,5.240905522,5.036393758,'
                          '4.990182757,4.897580596,3.975713818,4.894207123,'
                          '5.113659881,4.20994586,3.475695941,3.018534226,'
                          '3.68444758,4.383579198,4.343866431,5.163411369,'
                          '5.801548283,6.10348765,4.76074516,4.018968583,'
                          '3.807106599,3.840522581,3.655294639,4.160280272,'
                          '6.146341463,6.537348623,6.509125435,6.938443309,'
                          '6.568824155,6.048820957,4.04172726,4.186831741,'
                          '4.382939676,3.392420144,2.498729296,2.565344859,'
                          '3.107969091,3.521797592,3.212318473,3.098584692,'
                          '3.098584692,3.003021166,19.61702787,18.97466246,'
                          '17.74593227,13.84039072,9.601554043,7.117494731,'
                          '8.166610723,9.622661542,9.648757987,10.05073744,'
                          '10.49463234,10.66450371,6.276549712,6.666642728,'
                          '7.597516675,7.637987286,7.99012509,7.607584033,'
                          '9.484363464,10.81324061,12.7097409,15.52457602,'
                          '16.93137173,16.62982306,17.55389647,18.22108629,'
                          '16.25634386,13.3725907,11.14262294,9.507520125,'
                          '12.02516939,14.37913326,13.54138898,13.69591839,'
                          '13.5763623,12.97187212,6.682102697,6.291982582,'
                          '6.516689478,5.945157013,4.816202781,4.368899066,'
                          '5.856004508,7.240345922,8.164977774,8.529917685,'
                          '9.708595873,9.847243093,11.03816292,10.54622939,'
                          '9.156961086,8.511101588,8.264570818,11.33829871,'
                          '18.01195661,20.06321219,21.63712759,25.04773498,'
                          '26.89014696,26.78073067,6.56574156,7.373480411,'
                          '7.652096974,7.053667613,6.127066505,6.183935584,'
                          '8.305635992,8.372715009,7.504247076,7.651519753,'
                          '7.912693788,7.604124855,4.033356027,4.31699694,'
                          '4.329724566,3.941659077,3.57509152,3.341272685,'
                          '4.257833072,4.44955058,3.949110999,3.863659425,'
                          '4.109877511,3.999499419,10.82310834,10.58802629,'
                          '10.40296232,10.01247258,10.06182773,10.74264555,'
                          '13.74762357,11.65601928,9.605142332,9.014001387,'
                          '9.320782097,8.651402638,5.019884066,4.768990278,'
                          '4.852538715,5.450636437,5.355104552,5.708223236,'
                          '7.62507775,7.861627732,8.078635307,8.027613742,'
                          '8.275155581,8.036560522,5.986539203,5.523039996,'
                          '5.076780521,4.617465075,4.619105436,5.800444743,'
                          '9.275245924,9.627692959,8.94612643,8.091574662,'
                          '7.810715126,7.514930043,8.68886389,8.942669403,'
                          '8.941482912,8.233837469,7.409607055,7.436710115,'
                          '9.371745367,9.891824566,9.978460373,11.11907575,'
                          '11.9135905,11.99849464,6.971079892,6.859814025,'
                          '6.629153129,6.100565063,5.656171098,5.982685271,'
                          '8.157564657,8.320563893,7.953121271,7.970392182,'
                          '8.15379125,8.004598637],'
                          '"status":{"10":"e","11":"e","22":"e","23":"e",'
                          '"34":"e",'
                          '"35":"e","46":"e","47":"e","58":"e","59":"e",'
                          '"70":"e",'
                          '"71":"e","82":"e","83":"e","94":"e","95":"e",'
                          '"106":"e",'
                          '"107":"e","118":"e","119":"e","130":"e","131":"e",'
                          '"142":"e","143":"e","154":"e","155":"e","166":"e",'
                          '"167":"e","178":"e","179":"e","190":"e","191":"e",'
                          '"202":"e","203":"e","214":"e","215":"e","226":"e",'
                          '"227":"e","238":"e","239":"e","250":"e","251":"e",'
                          '"262":"e","263":"e","274":"e","275":"e","286":"e",'
                          '"287":"e","298":"e","299":"e","310":"e","311":"e",'
                          '"322":"e","323":"e","334":"e","335":"e","346":"e",'
                          '"347":"e","358":"e","359":"e","370":"e","371":"e",'
                          '"382":"e","383":"e","394":"e","395":"e","406":"e",'
                          '"407":"e","418":"e","419":"e","430":"e","431":"e"},'
                          '"dimension":{"id":["concept","area","year"],'
                          '"size":[1,36,12],"role":{"time":["year"],"geo":'
                          '["area"],'
                          '"metric":["concept"]},"concept":{"label":'
                          '"Selected indicator","category":{"label":'
                          '{"UNR":"Unemployment rate"},"unit":{"UNR":'
                          '{"type":"ratio","base":"Per cent","symbol":"%",'
                          '"multiplier":0}}}},"year":{"label":"2003-2014",'
                          '"category":{"index":{"2003":0,"2004":1,"2005":2,'
                          '"2006":3,'
                          '"2007":4,"2008":5,"2009":6,"2010":7,"2011":8,'
                          '"2012":9,'
                          '"2013":10,"2014":11}}},"area":{"label":'
                          '"OECD countries,'
                          'EU15 and total","category":{"index":{"AU":0,"AT":1,'
                          '"BE":2,"CA":3,"CL":4,"CZ":5,"DK":6,"EE":7,"FI":8,'
                          '"FR":9,"DE":10,"GR":11,"HU":12,"IS":13,"IE":14,'
                          '"IL":15,"IT":16,"JP":17,"KR":18,"LU":19,"MX":20,'
                          '"NL":21,"NZ":22,"NO":23,"PL":24,"PT":25,"SK":26,'
                          '"SI":27,"ES":28,"SE":29,"CH":30,"TR":31,"UK":32,'
                          '"US":33,"EU15":34,"OECD":35},"label":{"AU":'
                          '"Australia",'
                          '"AT":"Austria","BE":"Belgium","CA":"Canada",'
                          '"CL":"Chile",'
                          '"CZ":"Czech Republic","DK":"Denmark","EE":'
                          '"Estonia",'
                          '"FI":"Finland","FR":"France","DE":"Germany",'
                          '"GR":"Greece","HU":"Hungary","IS":"Iceland",'
                          '"IE":"Ireland","IL":"Israel","IT":"Italy",'
                          '"JP":"Japan",'
                          '"KR":"Korea","LU":"Luxembourg","MX":"Mexico",'
                          '"NL":"Netherlands","NZ":"New Zealand",'
                          '"NO":"Norway",'
                          '"PL":"Poland","PT":"Portugal",'
                          '"SK":"Slovak Republic",'
                          '"SI":"Slovenia","ES":"Spain","SE":"Sweden",'
                          '"CH":"Switzerland","TR":"Turkey",'
                          '"UK":"United Kingdom",'
                          '"US":"United States","EU15":'
                          '"Euro area (15 countries)",'
                          '"OECD":"Total"},"child":{"EU15":["AT","BE","DE",'
                          '"DK",'
                          '"ES","FI","FR","GR","IE","IT","LU","NL","PT","SE",'
                          '"UK"],'
                          '"OECD":["EU15","AU","CA","CL","CZ","DK","EE","HU",'
                          '"IS",'
                          '"IL","JP","KR","MX","NO","NZ","PL","SK","SI","CH",'
                          '"TR",'
                          '"US"]}}}}},"canada":{"label":"Population by sex '
                          'and age '
                          'group. Canada. 2012","source":"Statistics Canada, '
                          'CANSIM,'
                          'table 051-0001","updated":"2012-09-27","value":'
                          '[34880.5'
                          ',17309.1,17571.3,100.0,100.0,100.0,1928.8,988.7,'
                          '940.1,'
                          '5.5,5.7,5.3,1857.1,955.0,902.1,5.3,5.5,5.1,1877.3,'
                          '964.7,'
                          '912.6,5.4,5.6,5.2,2163.0,1108.2,1054.7,6.2,6.4,6.0,'
                          '2441.1,1254.2,1186.9,7.0,7.2,6.8,2452.3,1246.8,'
                          '1205.5,'
                          '7.0,7.2,6.9,2406.3,1203.5,1202.8,6.9,7.0,6.8,'
                          '2307.2,'
                          '1155.2,1152.0,6.6,6.7,6.6,2384.6,1199.4,1185.2,6.8,'
                          '6.9,'
                          '6.7,2681.3,1350.1,1331.2,7.7,7.8,7.6,2703.2,1352.3,'
                          '1350.9,7.7,7.8,7.7,2428.5,1199.0,1229.5,7.0,6.9,'
                          '7.0,'
                          '2063.0,1010.2,1052.8,5.9,5.8,6.0,1645.1,797.9,'
                          '847.2,4.7,'
                          '4.6,4.8,1190.7,563.8,626.8,3.4,3.3,3.6,924.1,'
                          '418.9,505.2,'
                          '2.6,2.4,2.9,718.8,303.6,415.2,2.1,1.8,2.4,451.0,'
                          '164.1,'
                          '286.9,1.3,0.9,1.6,257.1,73.2,183.9,0.7,0.4,1.0],'
                          '"status":'
                          '["a"],"dimension":{"id":["country","year","age",'
                          '"concept","sex"],"size":[1,1,20,2,3],"role":{'
                          '"time":'
                          '["year"],"geo":["country"],"metric":["concept"]},'
                          '"concept":{"label":"Population and %","category":'
                          '{"index":{"POP":0,"PERCENT":1},"label":{"POP":'
                          '"Persons '
                          '(thousands)","PERCENT":"% of total of each group"},'
                          '"unit":{"POP":{"type":"count","base":"person",'
                          '"symbol":"","multiplier":3},"PERCENT":{"type":'
                          '"ratio",'
                          '"base":"Per cent","symbol":"%","multiplier":0}}}},'
                          '"year":{"label":"Year","category":{"index":'
                          '{"2012":0}}},'
                          '"country":{"label":"Country","category":{"label":'
                          '{"CA":"Canada"}}},"age":{"label":"Age group",'
                          '"category":'
                          '{"index":["T","4","9","14","19","24","29","34",'
                          '"39","44",'
                          '"49","54","59","64","69","74","79","84","89",'
                          '"older"],'
                          '"label":{"T":"Total","4":"0 to 4","9":"5 to 9",'
                          '"14":'
                          '"10 to 14","19":"15 to 19","24":"20 to 24","29":'
                          '"25 to 29","34":"30 to 34","39":"35 to 39","44":'
                          '"40 to 44","49":"45 to 49","54":"50 to 54","59":'
                          '"55 to 59","64":"60 to 64","69":"65 to 69","74":'
                          '"70 to 74","79":"75 to 79","84":"80 to 84","89":'
                          '"85 to 89","older":"90 and older"}}},"sex":{'
                          '"label":"Sex","category":{"index":["T","M","F"],'
                          '"label":'
                          '{"T":"Total","M":"Male","F":"Female"}}}}}}')
        self.oecd_datasets = json.loads(self.oecd_data,
                                        object_pairs_hook=OrderedDict)
        self.ons_data = ('{"ST1117EWla" : { "value" : { "0" : 195074, '
                         '"1" : 96699, "2" : 98375, "3" : 1524, "4" : 747, '
                         '"5" : 777, "6" : 1350, "7" : 676, "8" : 674, '
                         '"9" : 1158, "10" : 598, "11" : 560, "12" : 1041, '
                         '"13" : 547, "14" : 494, "15" : 825, "16" : 406, '
                         '"17" : 419, "18" : 818, "19" : 399, "20" : 419, '
                         '"21" : 629, "22" : 319, "23" : 310, "24" : 540, '
                         '"25" : 266, "26" : 274, "27" : 518, "28" : 259, '
                         '"29" : 259, "30" : 468, "31" : 263, "32" : 205, '
                         '"33" : 554, "34" : 271, "35" : 283, "36" : 620, '
                         '"37" : 322, "38" : 298, "39" : 714, "40" : 374, '
                         '"41" : 340, "42" : 753, "43" : 410, "44" : 343, '
                         '"45" : 956, "46" : 514, "47" : 442, "48" : 1194, '
                         '"49" : 578, "50" : 616, "51" : 1815, "52" : 869, '
                         '"53" : 946, "54" : 2526, "55" : 1187, "56" : 1339, '
                         '"57" : 4749, "58" : 2129, "59" : 2620, "60" : 7326, '
                         '"61" : 3226, "62" : 4100, "63" : 12383, '
                         '"64" : 5174, "65" : 7209, "66" : 16063, '
                         '"67" : 7278, "68" : 8785, "69" : 17536, '
                         '"70" : 8253, "71" : 9283, "72" : 17373, '
                         '"73" : 8070, "74" : 9303, "75" : 13634, '
                         '"76" : 6829, "77" : 6805, "78" : 11274, '
                         '"79" : 6050, "80" : 5224, "81" : 9381, "82" : 5070, '
                         '"83" : 4311, "84" : 7836, "85" : 4375, "86" : 3461, '
                         '"87" : 6531, "88" : 3674, "89" : 2857, "90" : 5397, '
                         '"91" : 3058, "92" : 2339, "93" : 4584, "94" : 2664, '
                         '"95" : 1920, "96" : 3640, "97" : 2128, "98" : 1512, '
                         '"99" : 3286, "100" : 2027, "101" : 1259, '
                         '"102" : 2652, "103" : 1618, "104" : 1034, '
                         '"105" : 2350, "106" : 1437, "107" : 913, '
                         '"108" : 1980, "109" : 1176, "110" : 804, '
                         '"111" : 1759, "112" : 973, "113" : 786, '
                         '"114" : 1500, "115" : 825, "116" : 675, '
                         '"117" : 1306, "118" : 767, "119" : 539, '
                         '"120" : 1268, "121" : 750, "122" : 518, '
                         '"123" : 1093, "124" : 601, "125" : 492, '
                         '"126" : 1081, "127" : 603, "128" : 478, '
                         '"129" : 870, "130" : 475, "131" : 395, '
                         '"132" : 904, "133" : 502, "134" : 402, '
                         '"135" : 826, "136" : 426, "137" : 400, '
                         '"138" : 809, "139" : 428, "140" : 381, '
                         '"141" : 746, "142" : 389, "143" : 357, '
                         '"144" : 690, "145" : 346, "146" : 344, '
                         '"147" : 630, "148" : 303, "149" : 327, '
                         '"150" : 644, "151" : 270, "152" : 374, '
                         '"153" : 642, "154" : 292, "155" : 350, '
                         '"156" : 578, "157" : 251, "158" : 327, '
                         '"159" : 622, "160" : 276, "161" : 346, '
                         '"162" : 575, "163" : 222, "164" : 353, '
                         '"165" : 561, "166" : 223, "167" : 338, '
                         '"168" : 620, "169" : 218, "170" : 402, '
                         '"171" : 649, "172" : 243, "173" : 406, '
                         '"174" : 584, "175" : 180, "176" : 404, '
                         '"177" : 734, "178" : 276, "179" : 458, '
                         '"180" : 591, "181" : 213, "182" : 378, '
                         '"183" : 653, "184" : 225, "185" : 428, '
                         '"186" : 677, "187" : 230, "188" : 447, '
                         '"189" : 694, "190" : 207, "191" : 487, '
                         '"192" : 640, "193" : 224, "194" : 416, '
                         '"195" : 583, "196" : 206, "197" : 377, '
                         '"198" : 568, "199" : 212, "200" : 356, '
                         '"201" : 497, "202" : 184, "203" : 313, '
                         '"204" : 470, "205" : 194, "206" : 276, '
                         '"207" : 411, "208" : 152, "209" : 259, '
                         '"210" : 357, "211" : 134, "212" : 223, '
                         '"213" : 389, "214" : 177, "215" : 212, '
                         '"216" : 370, "217" : 159, "218" : 211, '
                         '"219" : 371, "220" : 156, "221" : 215, '
                         '"222" : 291, "223" : 87, "224" : 204, '
                         '"225" : 285, "226" : 111, "227" : 174, '
                         '"228" : 231, "229" : 118, "230" : 113, '
                         '"231" : 204, "232" : 94, "233" : 110, '
                         '"234" : 161, "235" : 85, "236" : 76, '
                         '"237" : 145, "238" : 71, "239" : 74, '
                         '"240" : 142, "241" : 53, "242" : 89, '
                         '"243" : 147, "244" : 83, "245" : 64, '
                         '"246" : 88, "247" : 41, "248" : 47, '
                         '"249" : 74, "250" : 31, "251" : 43, "252" : 68, '
                         '"253" : 37, "254" : 31, "255" : 64, "256" : 34, '
                         '"257" : 30, "258" : 234, "259" : 101, "260" : 133 },'
                         ' "label" : "Sex by single year of age (non-UK born '
                         'short-term residents)", "updated" : "08/08/2014 '
                         '16:39:07", "source" : "Office for National '
                         'Statistics", "dimension" : { "id" : [ "2011CMLADH", '
                         '"CL_0000304", "CL_0000035", "Att_000001", '
                         '"CL_0000137" ], "size" : [ 1, 87, 3, 1, 1 ], '
                         '"role" : { "time" : [ "CL_0000137" ], '
                         '"geo" : [ "2011CMLADH" ], '
                         '"metric" : [ "Att_000001" ] }, '
                         '"2011CMLADH" : { "category" : { '
                         '"index" : { "K04000001" : 0 }, '
                         '"label" : { "K04000001" : "England and Wales" } }, '
                         '"label" : "2011 Census merged local authority '
                         'district hierarchy"},"CL_0000304" : { '
                         '"category" : { "index" : { "CI_0000487" : 82, '
                         '"CI_0000488" : 81, "CI_0000485" : 10, '
                         '"CI_0000486" : 83, "CI_0000389" : 48, '
                         '"CI_0000388" : 42, "CI_0000489" : 1, '
                         '"CI_0000387" : 43, "CI_0000386" : 44, '
                         '"CI_0000385" : 40, "CI_0000501" : 17, '
                         '"CI_0000480" : 6, "CI_0000384" : 38, '
                         '"CI_0000383" : 39, "CI_0000382" : 31, '
                         '"CI_0000483" : 8, "CI_0000381" : 36, '
                         '"CI_0000484" : 84, "CI_0000380" : 34, '
                         '"CI_0000481" : 7, "CI_0000303" : 85, '
                         '"CI_0000239" : 49, "CI_0000272" : 29, '
                         '"CI_0000400" : 67, "CI_0000401" : 68, '
                         '"CI_0000235" : 41, "CI_0000402" : 65, '
                         '"CI_0000271" : 25, "CI_0000403" : 66, '
                         '"CI_0000404" : 63, "CI_0000497" : 18, '
                         '"CI_0000498" : 19, "CI_0000499" : 16, '
                         '"CI_0000398" : 60, "CI_0000397" : 58, '
                         '"CI_0000399" : 70, "CI_0000408" : 79, '
                         '"CI_0000394" : 54, "CI_0000407" : 78, '
                         '"CI_0000393" : 55, "CI_0000406" : 62, '
                         '"CI_0000396" : 59, "CI_0000490" : 2, '
                         '"CI_0000405" : 64, "CI_0000395" : 56, '
                         '"CI_0000491" : 3, "CI_0000492" : 4, '
                         '"CI_0000390" : 47, "CI_0000510" : 12, '
                         '"CI_0000392" : 50, "CI_0000409" : 80, '
                         '"CI_0000391" : 46, "CI_0000410" : 74, '
                         '"CI_0000316" : 71, "CI_0000411" : 75, '
                         '"CI_0000225" : 53, "CI_0000509" : 15, '
                         '"CI_0000508" : 14, "CI_0000222" : 57, '
                         '"CI_0000507" : 11, "CI_0000504" : 20, '
                         '"CI_0000317" : 73, "CI_0000216" : 51, '
                         '"CI_0000217" : 52, "CI_0000259" : 37, '
                         '"CI_0000326" : 69, "CI_0000424" : 9, '
                         '"CI_0000253" : 33, "CI_0000252" : 32, '
                         '"CI_0000422" : 5, "CI_0000474" : 72, '
                         '"CI_0000371" : 24, "CI_0000372" : 23, '
                         '"CI_0000373" : 22, "CI_0000374" : 21, '
                         '"CI_0000375" : 30, "CI_0000376" : 28, '
                         '"CI_0000377" : 26, "CI_0000473" : 76, '
                         '"CI_0000378" : 27, "CI_0002762" : 0, '
                         '"CI_0000379" : 35, "CI_0002763" : 86, '
                         '"CI_0000334" : 61, "CI_0000332" : 77, '
                         '"CI_0000432" : 13, "CI_0000241" : 45 }, '
                         '"label" : { "CI_0000487" : "Age 81", '
                         '"CI_0000488" : "Age 80", "CI_0000485" : "Age 9", '
                         '"CI_0000486" : "Age 82", "CI_0000389" : "Age 47", '
                         '"CI_0000388" : "Age 41", '
                         '"CI_0000489" : "Age under 1", '
                         '"CI_0000387" : "Age 42", "CI_0000386" : "Age 43", '
                         '"CI_0000385" : "Age 39", "CI_0000480" : "Age 5", '
                         '"CI_0000501" : "Age 16", "CI_0000384" : "Age 37", '
                         '"CI_0000383" : "Age 38", "CI_0000382" : "Age 30", '
                         '"CI_0000381" : "Age 35", "CI_0000483" : "Age 7", '
                         '"CI_0000484" : "Age 83", "CI_0000380" : "Age 33", '
                         '"CI_0000481" : "Age 6", "CI_0000239" : "Age 48", '
                         '"CI_0000303" : "Age 84", "CI_0000272" : "Age 28", '
                         '"CI_0000400" : "Age 66", "CI_0000235" : "Age 40", '
                         '"CI_0000401" : "Age 67", "CI_0000402" : "Age 64", '
                         '"CI_0000271" : "Age 24", "CI_0000403" : "Age 65", '
                         '"CI_0000404" : "Age 62", "CI_0000497" : "Age 17", '
                         '"CI_0000498" : "Age 18", "CI_0000499" : "Age 15", '
                         '"CI_0000398" : "Age 59", "CI_0000397" : "Age 57", '
                         '"CI_0000399" : "Age 69", "CI_0000394" : "Age 53", '
                         '"CI_0000408" : "Age 78", "CI_0000393" : "Age 54", '
                         '"CI_0000407" : "Age 77", "CI_0000490" : "Age 1", '
                         '"CI_0000406" : "Age 61", "CI_0000396" : "Age 58", '
                         '"CI_0000405" : "Age 63", "CI_0000395" : "Age 55", '
                         '"CI_0000491" : "Age 2", "CI_0000492" : "Age 3", '
                         '"CI_0000390" : "Age 46", "CI_0000510" : "Age 11", '
                         '"CI_0000392" : "Age 49", "CI_0000391" : "Age 45", '
                         '"CI_0000409" : "Age 79", "CI_0000410" : "Age 73", '
                         '"CI_0000316" : "Age 70", "CI_0000225" : "Age 52", '
                         '"CI_0000411" : "Age 74", "CI_0000509" : "Age 14", '
                         '"CI_0000508" : "Age 13", "CI_0000507" : "Age 10", '
                         '"CI_0000222" : "Age 56", "CI_0000504" : "Age 19", '
                         '"CI_0000317" : "Age 72", "CI_0000216" : "Age 50", '
                         '"CI_0000217" : "Age 51", "CI_0000259" : "Age 36", '
                         '"CI_0000326" : "Age 68", "CI_0000424" : "Age 8", '
                         '"CI_0000253" : "Age 32", "CI_0000252" : "Age 31", '
                         '"CI_0000422" : "Age 4", "CI_0000371" : "Age 23", '
                         '"CI_0000474" : "Age 71", "CI_0000372" : "Age 22", '
                         '"CI_0000373" : "Age 21", "CI_0000374" : "Age 20", '
                         '"CI_0000375" : "Age 29", "CI_0000376" : "Age 27", '
                         '"CI_0000377" : "Age 25", "CI_0000473" : "Age 75", '
                         '"CI_0000378" : "Age 26", '
                         '"CI_0002762" : "All categories: Age", '
                         '"CI_0000379" : "Age 34", '
                         '"CI_0002763" : "Age 85 and over", '
                         '"CI_0000334" : "Age 60", "CI_0000332" : "Age 76", '
                         '"CI_0000432" : "Age 12", '
                         '"CI_0000241" : "Age 44" } }, '
                         '"label" : "Age (T087A)"},"CL_0000035" : { '
                         '"category" : { "index" : { "CI_0000071" : 1, '
                         '"CI_0000070" : 2, "CI_0000121" : 0 }, "label" : { '
                         '"CI_0000071" : "Males", "CI_0000070" : "Females", '
                         '"CI_0000121" : "All categories: Sex" } }, '
                         '"label" : "Sex (T003A)"},"CL_0000137" : { '
                         '"category" : { "index" : { "CI_0000001" : 0 }, '
                         '"label" : { "CI_0000001" : "2011" } }, '
                         '"label" : "Time"},"Att_000001" : { "category" : { '
                         '"index" : { "Segment_1" : 0 }, "unit" : { '
                         '"Segment_1" : { "unit" : "Number", '
                         '"base" : "Person", '
                         '"label" : "All non-UK born short-term residents", '
                         '"type" : "Count", "multiplier" : "Units" } } }, '
                         '"label" : "Measures"} }}}')
        self.ons_datasets = json.loads(self.ons_data,
                                       object_pairs_hook=OrderedDict)

    def test_check_input(self):
        """ Test pyjstat check_input() """

        self.assertRaises(ValueError, pyjstat.check_input, 'name')
        self.assertTrue(pyjstat.check_input('label') is None)
        self.assertTrue(pyjstat.check_input('id') is None)

    def test_get_dim_index_with_index(self):
        """ Test pyjstat get_dim_index() using id as parameter """

        dim = self.oecd_datasets['oecd']['dimension']['id'][2]
        dims_df = pyjstat.get_dim_index(self.oecd_datasets['oecd'], dim)
        self.assertTrue(dims_df.iloc[0]['id'] == '2003')
        self.assertTrue(dims_df.iloc[-1]['index'] == 11)

    def test_get_dim_index_with_label(self):
        """ Test pyjstat get_dim_index() using label as parameter """

        dim = self.oecd_datasets['oecd']['dimension']['id'][0]
        dims_df = pyjstat.get_dim_index(self.oecd_datasets['oecd'], dim)
        self.assertTrue(dims_df.iloc[0]['id'] == 'UNR')
        self.assertTrue(dims_df.iloc[-1]['index'] == 0)

    def test_get_dim_label_with_label(self):
        """ Test pyjstat get_dim_label() using label as parameter """

        dim = self.oecd_datasets['oecd']['dimension']['id'][0]
        dims_df = pyjstat.get_dim_label(self.oecd_datasets['oecd'], dim)
        self.assertTrue(dims_df.iloc[0]['id'] == 'UNR')
        self.assertTrue(dims_df.iloc[-1]['label'] == 'Unemployment rate')

    def test_get_dim_label_with_index(self):
        """ Test pyjstat get_dim_label() using id as parameter """

        dim = self.oecd_datasets['oecd']['dimension']['id'][2]
        dims_df = pyjstat.get_dim_label(self.oecd_datasets['oecd'], dim)
        self.assertTrue(dims_df.iloc[0]['id'] == '2003')
        self.assertTrue(dims_df.iloc[-1]['label'] == '2014')

    def test_get_dimensions_by_label(self):
        """ Test pyjstat get_dimensions() using label as parameter """

        dimensions, dim_names = pyjstat.get_dimensions(
            self.oecd_datasets['oecd'], 'label')
        self.assertTrue(dim_names[2] == '2003-2014')
        self.assertTrue(dimensions[0].iloc[0]['label'] == 'Unemployment rate')

    def test_get_dimensions_by_index(self):
        """ Test pyjstat get_dimensions() using id as parameter """

        dimensions, dim_names = pyjstat.get_dimensions(
            self.oecd_datasets['oecd'], 'index')
        self.assertTrue(dim_names[2] == 'year')
        self.assertTrue(dimensions[0].iloc[0]['index'] == 0)

    def test_get_df_row(self):
        """ Test pyjstat get_df_row() """

        dimensions = pyjstat.get_dimensions(self.oecd_datasets['oecd'],
                                            'label')
        first_row = ['Unemployment rate', 'Australia', '2003']
        categories = pyjstat.get_df_row(dimensions[0])
        self.assertTrue(set(first_row) == set(next(categories)))

    def test_get_values(self):
        """ Test pyjstat get_values() """

        values = pyjstat.get_values(self.oecd_datasets['oecd'])
        first_four_values = [5.943826289, 5.39663128, 5.044790587, 4.789362794]
        last_four_values = [7.953121271, 7.970392182, 8.15379125, 8.004598637]
        self.assertTrue(set(first_four_values) == set(values[:4]))
        self.assertTrue(set(last_four_values) == set(values[-4:]))

        ons_values = pyjstat.get_values(self.ons_datasets['ST1117EWla'])
        first_four_ons_values = [195074, 96699, 98375, 1524]
        last_four_ons_values = [30, 234, 101, 133]
        self.assertTrue(set(first_four_ons_values) == set(ons_values[:4]))
        self.assertTrue(set(last_four_ons_values) == set(ons_values[-4:]))

    def test_uniquify(self):
        """ Test pyjstat uniquify() """

        input_list = [1, 4, 5, 5, 3]
        output_list = [1, 4, 5, 3]
        self.assertTrue(set(input_list) == set(output_list))

    def test_from_json_stat_with_label(self):
        """ Test pyjstat from_json_stat() using label as parameter """

        results = pyjstat.from_json_stat(self.oecd_datasets)
        line_thirty = ['Unemployment rate', 'Belgium', 2009, 7.891892855]
        dimensions = pyjstat.get_dimensions(self.oecd_datasets['oecd'],
                                            'label')
        self.assertTrue(len(results) == 2)
        self.assertTrue(set(results[0].columns.values[:-1]) ==
                        set(dimensions[1]))
        self.assertTrue(set(results[0].iloc[30].values) ==
                        set(line_thirty))

    def test_from_json_stat_with_id(self):
        """ Test pyjstat from_json_stat() using id as parameter"""

        results = pyjstat.from_json_stat(self.oecd_datasets, naming='id')
        line_thirty = ['UNR', 'BE', 2009, 7.891892855]
        dimensions = pyjstat.get_dimensions(self.oecd_datasets['oecd'], 'id')
        self.assertTrue(len(results) == 2)
        self.assertTrue(set(results[0].columns.values[:-1]) ==
                        set(dimensions[1]))
        self.assertTrue(set(results[0].iloc[30].values) ==
                        set(line_thirty))

    def test_to_json_stat(self):
        """ Test pyjstat to_json_stat()"""

        results = pyjstat.from_json_stat(self.oecd_datasets)
        json_data = json.loads(pyjstat.to_json_stat(results),
                               object_pairs_hook=OrderedDict)
        self.assertTrue(json_data[0]["dataset1"]["dimension"]
                        ["Selected indicator"]["label"] ==
                        "Selected indicator")
        self.assertTrue(json_data[0]["dataset1"]["dimension"]["size"][1] == 36)
        self.assertTrue(json_data[1]["dataset2"]["dimension"]["id"][2] ==
                        "Age group")
        self.assertTrue(json_data[0]["dataset1"]["value"][-1],
                        results[0][-1:]['value'])
        results[0].columns = ['a', 'a', 'b', 'value']
        self.assertRaises(ValueError, pyjstat.to_json_stat, results)

    def test_from_to_json_stat_as_dict(self):
        """ Test pyjstat nested from-to json_stat using dict of dicts as input
        """

        results = pyjstat.from_json_stat(self.oecd_datasets)
        json_data = json.loads(pyjstat.to_json_stat(results, output='dict'),
                               object_pairs_hook=OrderedDict)
        data_df = pyjstat.from_json_stat(json.loads(json.dumps(json_data),
                                                    object_pairs_hook=
                                                    OrderedDict))
        line_thirty = ['Unemployment rate', 'Belgium', 2009, 7.891892855]
        dimensions = pyjstat.get_dimensions(self.oecd_datasets['oecd'],
                                            'label')
        self.assertTrue(len(data_df) == 2)
        self.assertTrue(set(data_df[0].columns.values[:-1]) ==
                        set(dimensions[1]))
        self.assertTrue(set(data_df[0].iloc[30].values) ==
                        set(line_thirty))

    def test_from_to_json_stat_as_list(self):
        """ Test pyjstat nested from-to json_stat using list of dicts as input
        """

        results = pyjstat.from_json_stat(self.oecd_datasets)
        json_data = json.loads(pyjstat.to_json_stat(results),
                               object_pairs_hook=OrderedDict)
        data_df = pyjstat.from_json_stat(json.loads(json.dumps(json_data),
                                                    object_pairs_hook=
                                                    OrderedDict))
        line_thirty = ['Unemployment rate', 'Belgium', 2009, 7.891892855]
        dimensions = pyjstat.get_dimensions(self.oecd_datasets['oecd'],
                                            'label')
        self.assertTrue(len(data_df) == 2)
        self.assertTrue(set(data_df[0].columns.values[:-1]) ==
                        set(dimensions[1]))
        self.assertTrue(set(data_df[0].iloc[30].values) ==
                        set(line_thirty))

    def test_from_to_json_stat_no_loads(self):
        """ Test pyjstat nested from-to json_stat using list of dicts as input
        """

        results = pyjstat.from_json_stat(self.oecd_datasets)
        json_data = json.loads(pyjstat.to_json_stat(results),
                               object_pairs_hook=OrderedDict)
        data_df = pyjstat.from_json_stat(json_data)
        line_thirty = ['Unemployment rate', 'Belgium', 2009, 7.891892855]
        dimensions = pyjstat.get_dimensions(self.oecd_datasets['oecd'],
                                            'label')
        self.assertTrue(len(data_df) == 2)
        self.assertTrue(set(data_df[0].columns.values[:-1]) ==
                        set(dimensions[1]))
        self.assertTrue(set(data_df[0].iloc[30].values) ==
                        set(line_thirty))

    def test_generate_df_with_label(self):
        """ Test pyjstat generate_df() using label as parameter"""

        data_df = pyjstat.generate_df(self.oecd_datasets['oecd'], 'label')
        line_thirty = ['Unemployment rate', 'Belgium', 2009, 7.891892855]
        dimensions = pyjstat.get_dimensions(self.oecd_datasets['oecd'],
                                            'label')
        self.assertTrue(set(data_df.columns.values[:-1]) ==
                        set(dimensions[1]))
        self.assertTrue(set(data_df.iloc[30].values) ==
                        set(line_thirty))

    def test_generate_df_with_id(self):
        """ Test pyjstat generate_df() using id as parameter"""

        data_df = pyjstat.generate_df(self.oecd_datasets['oecd'], 'id')
        line_thirty = ['UNR', 'BE', 2009, 7.891892855]
        dimensions = pyjstat.get_dimensions(self.oecd_datasets['oecd'], 'id')
        self.assertTrue(set(data_df.columns.values[:-1]) ==
                        set(dimensions[1]))
        self.assertTrue(set(data_df.iloc[30].values) ==
                        set(line_thirty))


if __name__ == '__main__':
    unittest.main()

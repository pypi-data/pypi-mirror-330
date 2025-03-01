from flask import Flask ,render_template ,request ,redirect ,url_for ,flash ,jsonify #line:1
from datetime import datetime #line:2
# from .app import (setup_driver ,select_department ,click_proceed_button ,click_challan_vehicle_tab ,enter_challan_number ,submit_captcha ,click_view_link ,extract_table_data )#line:12
import time #line:13

import base64 #line:1
import time #line:2
import requests #line:3
import json #line:4
from selenium import webdriver #line:5
from selenium .webdriver .chrome .service import Service #line:6
from selenium .webdriver .chrome .options import Options #line:7
from webdriver_manager .chrome import ChromeDriverManager #line:8
from selenium .webdriver .common .by import By #line:9
from selenium .webdriver .support .ui import Select #line:10
from selenium .webdriver .support .ui import WebDriverWait #line:11
from selenium .webdriver .support import expected_conditions as EC #line:12
import pandas as pd #line:13
from datetime import datetime #line:14
import os #line:15
STATE_DEPARTMENTS ={'AS':'6~ASVC01','CH':'27~CHVC01','CG':'18~CGVC01','DL':'26~DLVC01','DL2':'26~DLVC02','GJ':'17~GJVC01','GJ2':'17~GJVC02','HR':'14~HRVC01','HP':'5~HPVC01','JK':'12~JKVC01','JK2':'12~JKVC02','KA':'3~KAVC01','KL':'4~KLVC01','KL2':'4~KLVC02','MP':'23~MPVC01','MH':'1~MHVC01','MH2':'1~MHVC03','MN':'25~MNVC01','MN2':'25~MNVC02','ML':'21~MLVC01','OD':'11~ODVC01','RJ':'9~RJVC01','TN':'10~TNVC01','TR':'20~TRVC01','UK':'15~UKVC02','UK2':'15~UKVC01','UP':'13~UPVC01','WB':'16~WBVC01',}#line:47
def setup_driver ():#line:49
    O00000O0000O0OOO0 =Options ()#line:50
    O00000O0000O0OOO0 .add_argument ('--start-maximized')#line:51
    O00000O0000O0OOO0 .add_experimental_option ('excludeSwitches',['enable-logging'])#line:52
    O00000O0000O0OOO0 .add_argument ('--ignore-certificate-errors')#line:53
    O00000O0000O0OOO0 .add_argument ('--ignore-ssl-errors')#line:54
    O0OO00OOOO00OO000 =Service (ChromeDriverManager ().install ())#line:55
    return webdriver .Chrome (service =O0OO00OOOO00OO000 ,options =O00000O0000O0OOO0 )#line:56
def select_department (O000OOO00OOOO000O ,OO0O00OOOOOO0OO00 ):#line:58
    try :#line:59
        OOO0O000OO00O000O =WebDriverWait (O000OOO00OOOO000O ,10 )#line:60
        O0OO0OOOOOOO00OO0 =OOO0O000OO00O000O .until (EC .presence_of_element_located ((By .ID ,"fstate_code")))#line:61
        O0O00O0O0000O0OO0 =Select (O0OO0OOOOOOO00OO0 )#line:62
        if OO0O00OOOOOO0OO00 in STATE_DEPARTMENTS :#line:64
            O0O00O0O0000O0OO0 .select_by_value (STATE_DEPARTMENTS [OO0O00OOOOOO0OO00 ])#line:65
            time .sleep (1 )#line:66
            return True #line:67
        return False #line:68
    except Exception as OO0O0OOOOO0O0OOO0 :#line:69
        print (f"Error selecting department: {str(OO0O0OOOOO0O0OOO0)}")#line:70
        return False #line:71
def click_proceed_button (OO0OOOO000O0OOOO0 ):#line:73
    try :#line:74
        O0O00O0O0O0OO0OO0 =WebDriverWait (OO0OOOO000O0OOOO0 ,10 )#line:75
        OO00000OOOOOOO0OO =O0O00O0O0O0OO0OO0 .until (EC .element_to_be_clickable ((By .ID ,"payFineBTN")))#line:76
        OO00000OOOOOOO0OO .click ()#line:77
        return True #line:78
    except Exception as OO0OOO0O00OOO000O :#line:79
        print (f"Error clicking proceed button: {str(OO0OOO0O00OOO000O)}")#line:80
        return False #line:81
def click_challan_vehicle_tab (O0OO0000O0O00OOO0 ):#line:83
    try :#line:84
        OOO0O0O0O0O0OOOOO =WebDriverWait (O0OO0000O0O00OOO0 ,10 )#line:85
        OOOO0O0OO00O00O0O =["//div[@class='col-6 p-0 mainmenu']//a[contains(.,'Challan/Vehicle No.')]","//a[contains(text(),'Challan/Vehicle No.')]","//a[contains(@href,'#police')]"]#line:91
        for OOOOOO00O0000O0OO in OOOO0O0OO00O00O0O :#line:93
            try :#line:94
                OO0000OO0OOO00OOO =OOO0O0O0O0O0OOOOO .until (EC .element_to_be_clickable ((By .XPATH ,OOOOOO00O0000O0OO )))#line:95
                OO0000OO0OOO00OOO .click ()#line:96
                time .sleep (2 )#line:97
                if O0OO0000O0O00OOO0 .find_element (By .ID ,"challan_no").is_displayed ():#line:100
                    return {"status":True ,"message":"Successfully clicked challan tab"}#line:101
            except Exception :#line:103
                continue #line:104
        raise Exception ("Could not find or click the Challan/Vehicle tab")#line:106
    except Exception as O00O0000OO0O0O00O :#line:108
        O000OOO0O00O00OO0 =f"Error clicking Challan/Vehicle tab: {str(O00O0000OO0O0O00O)}"#line:109
        print (O000OOO0O00O00OO0 )#line:110
        return {"status":False ,"message":O000OOO0O00O00OO0 }#line:111
def submit_captcha (O000OOOOOO0OO0OOO ):#line:113
    try :#line:114
        O00000O0OO0000OOO =O000OOOOOO0OO0OOO .find_elements (By .CSS_SELECTOR ,"img[alt='CAPTCHA Image']")[1 ]#line:115
        print (O00000O0OO0000OOO .get_attribute ('src'))#line:116
        OO0OOOO00000OOO00 =O000OOOOOO0OO0OOO .execute_script (f"""
                var canvas = document.createElement('canvas');
                var img = arguments[0];
                canvas.width = img.naturalWidth;
                canvas.height = img.naturalHeight;
                canvas.getContext('2d').drawImage(img, 0, 0);
                return canvas.toDataURL('image/png').substring(22); // Extract base64 part
            """,O00000O0OO0000OOO )#line:125
        print (f"base64 captcha image: "+OO0OOOO00000OOO00 )#line:128
        O000OOO0OOOOOO000 ='https://api.apitruecaptcha.org/one/gettext'#line:130
        OOO00O0O00O00O0OO ={'userid':'anshulstartups@gmail.com','apikey':'WczhL1HGgcRhrXFGxMAV','data':OO0OOOO00000OOO00 }#line:135
        O00O0O0O0OOOOOO00 =requests .post (url =O000OOO0OOOOOO000 ,json =OOO00O0O00O00O0OO )#line:136
        OOO00O0O00O00O0OO =O00O0O0O0OOOOOO00 .json ()#line:137
        print (OOO00O0O00O00O0OO )#line:138
        O000OO0000O0OO000 =WebDriverWait (O000OOOOOO0OO0OOO ,10 ).until (EC .presence_of_element_located ((By .CSS_SELECTOR ,"input#fcaptcha_code_police")))#line:142
        O000OO0000O0OO000 .clear ()#line:143
        O000OO0000O0OO000 .send_keys (OOO00O0O00O00O0OO ['result'])#line:144
        time .sleep (1 )#line:145
        O00O0O00OOO00O0O0 =WebDriverWait (O000OOOOOO0OO0OOO ,10 ).until (EC .element_to_be_clickable ((By .CSS_SELECTOR ,"button[onclick='submitpoliceForm()']")))#line:150
        O00O0O00OOO00O0O0 .click ()#line:151
        time .sleep (1 )#line:152
        return True #line:153
    except Exception as OOOO00O0OOOO00OOO :#line:154
        print (f"Failed to submit captcha: {str(OOOO00O0OOOO00OOO)}")#line:155
        return False #line:156
def enter_challan_number (O0000OOOOOOO000O0 ,OOOOO00OO000OO000 ):#line:158
    try :#line:159
        OOOO0OO000O0O0OOO =WebDriverWait (O0000OOOOOOO000O0 ,10 )#line:160
        OOO00O000O00000O0 =OOOO0OO000O0O0OOO .until (EC .presence_of_element_located ((By .ID ,"challan_no")))#line:161
        OOO00O000O00000O0 .clear ()#line:162
        OOO00O000O00000O0 .send_keys (OOOOO00OO000OO000 )#line:163
        time .sleep (1 )#line:164
        return True #line:165
    except Exception as OOOO0OO0OOOOO0OO0 :#line:166
        print (f"Error entering challan number: {str(OOOO0OO0OOOOO0OO0)}")#line:167
        return False #line:168
def click_view_link (O0O0OO00O0OO00O00 ):#line:170
    try :#line:171
        O0OOOOOO0O000000O =WebDriverWait (O0O0OO00O0OO00O00 ,10 )#line:172
        OO0OO0O0000000O0O =O0OOOOOO0O000000O .until (EC .presence_of_element_located ((By .CLASS_NAME ,"viewDetlink")))#line:174
        O0O0OO00O0OO00O00 .execute_script ("arguments[0].click();",OO0OO0O0000000O0O )#line:175
        time .sleep (2 )#line:176
        return True #line:177
    except Exception as O000OOOOOO00O0OO0 :#line:178
        print (f"Error clicking view link: {str(O000OOOOOO00O0OO0)}")#line:179
        return False #line:180
def extract_table_data (OO0OO00O0OO0OO0O0 ):#line:182
    try :#line:183
        O0OO0OOOO0O0O0O00 =WebDriverWait (OO0OO00O0OO0OO0O0 ,20 )#line:184
        O0000O0O0OO00O000 =O0OO0OOOO0O0O0O00 .until (EC .presence_of_all_elements_located ((By .TAG_NAME ,"table")))#line:185
        print (f"Found {len(O0000O0O0OO00O000)} tables")#line:186
        OOOOO00OO00O0O0OO ={"case_details":{},"current_status":{},"offence_details":[],"proposed_fine":"","all_tables":[]}#line:195
        for OOO0O0O0O00O0O0OO ,O0O0000OOOOO000OO in enumerate (O0000O0O0OO00O000 ):#line:198
            OO0O0OO00OO00OO00 ={"index":OOO0O0O0O00O0O0OO ,"title":"","headers":[],"rows":[]}#line:204
            try :#line:207
                O0O00O00O0000O0OO =OO0OO00O0OO0OO0O0 .execute_script ("return arguments[0].previousElementSibling",O0O0000OOOOO000OO )#line:208
                if O0O00O00O0000O0OO :#line:209
                    OO0O0OO00OO00OO00 ["title"]=O0O00O00O0000O0OO .text .strip ()#line:210
            except :#line:211
                pass #line:212
            OOO0000000OO0OOO0 =O0O0000OOOOO000OO .find_elements (By .TAG_NAME ,"th")#line:215
            if OOO0000000OO0OOO0 :#line:216
                OO0O0OO00OO00OO00 ["headers"]=[O0O0000OOOO00O0OO .text .strip ()for O0O0000OOOO00O0OO in OOO0000000OO0OOO0 ]#line:217
            OOOO0OO0OO00000O0 =O0O0000OOOOO000OO .find_elements (By .TAG_NAME ,"tr")#line:220
            for O0OOO0O000O0000OO in OOOO0OO0OO00000O0 :#line:221
                OO000OO0O0OO0O0OO =O0OOO0O000O0000OO .find_elements (By .TAG_NAME ,"td")#line:222
                if OO000OO0O0OO0O0OO :#line:223
                    OOOOOO00O00O0OOOO =[O0O0OO00O0O00OO00 .text .strip ()for O0O0OO00O0O00OO00 in OO000OO0O0OO0O0OO ]#line:224
                    if any (OOOOOO00O00O0OOOO ):#line:225
                        OO0O0OO00OO00OO00 ["rows"].append (OOOOOO00O00O0OOOO )#line:226
            OOOOO00OO00O0O0OO ["all_tables"].append (OO0O0OO00OO00OO00 )#line:228
            print (f"\nTable {OOO0O0O0O00O0O0OO + 1}:")#line:231
            print ("-"*50 )#line:232
            if OO0O0OO00OO00OO00 ["title"]:#line:233
                print (f"Title: {OO0O0OO00OO00OO00['title']}")#line:234
            if OO0O0OO00OO00OO00 ["headers"]:#line:235
                print (f"Headers: {' | '.join(OO0O0OO00OO00OO00['headers'])}")#line:236
            for O0OOO0O000O0000OO in OO0O0OO00OO00OO00 ["rows"]:#line:237
                print (" | ".join (O0OOO0O000O0000OO ))#line:238
        for O0O0000OOOOO000OO in O0000O0O0OO00O000 :#line:244
            OOOO0OO0OO00000O0 =O0O0000OOOOO000OO .find_elements (By .TAG_NAME ,"tr")#line:245
            for O0OOO0O000O0000OO in OOOO0OO0OO00000O0 :#line:246
                OO000OO0O0OO0O0OO =O0OOO0O000O0000OO .find_elements (By .TAG_NAME ,"td")#line:247
                if len (OO000OO0O0OO0O0OO )==2 :#line:248
                    OOO0O0O000OOOOO00 =OO000OO0O0OO0O0OO [0 ].text .strip ().rstrip ('.').replace ('  ',' ').replace (' ','_').lower ()#line:249
                    OOOOO0000O000OO00 =OO000OO0O0OO0O0OO [1 ].text .strip ()#line:250
                    if OOO0O0O000OOOOO00 .startswith ("registration")or OOO0O0O000OOOOO00 .startswith ("challan")or OOO0O0O000OOOOO00 .startswith ("name")or OOO0O0O000OOOOO00 .startswith ("place"):#line:252
                        if OOOOO0000O000OO00 :#line:253
                            OOOOO00OO00O0O0OO ["case_details"][OOO0O0O000OOOOO00 ]=OOOOO0000O000OO00 #line:254
                    elif OOO0O0O000OOOOO00 .startswith ("received")or OOO0O0O000OOOOO00 .startswith ("verified")or OOO0O0O000OOOOO00 .startswith ("allocated"):#line:255
                        if OOOOO0000O000OO00 :#line:256
                            OOOOO00OO00O0O0OO ["current_status"][OOO0O0O000OOOOO00 ]=OOOOO0000O000OO00 #line:257
        OO0O0OO0O00O00O00 =None #line:260
        for O0O0000OOOOO000OO in O0000O0O0OO00O000 :#line:261
            OO0O0OOOO000000O0 =O0O0000OOOOO000OO .find_elements (By .TAG_NAME ,"th")#line:262
            OOOOO0O00O0OO0000 =[OO0OOOOO00OO0OO00 .text .strip ().lower ()for OO0OOOOO00OO0OO00 in OO0O0OOOO000000O0 ]#line:263
            if any (O00O000O00OOO0000 in OOOOO0O00O0OO0000 for O00O000O00OOO0000 in ["offence","act","section"]):#line:264
                OO0O0OO0O00O00O00 =O0O0000OOOOO000OO #line:265
                break #line:266
        if OO0O0OO0O00O00O00 :#line:268
            OOO0000000OO0OOO0 =OO0O0OO0O00O00O00 .find_elements (By .TAG_NAME ,"th")#line:270
            OO0O0OOOO000000O0 =[O0OO00000OO00OOOO .text .strip ().lower ().replace (' ','_')for O0OO00000OO00OOOO in OOO0000000OO0OOO0 if O0OO00000OO00OOOO .text .strip ()]#line:271
            OOOO0OO0OO00000O0 =OO0O0OO0O00O00O00 .find_elements (By .TAG_NAME ,"tr")#line:274
            for O0OOO0O000O0000OO in OOOO0OO0OO00000O0 :#line:276
                OO000OO0O0OO0O0OO =O0OOO0O000O0000OO .find_elements (By .TAG_NAME ,"td")#line:277
                if OO000OO0O0OO0O0OO and len (OO000OO0O0OO0O0OO )>0 and "Proposed Fine"in O0OOO0O000O0000OO .text :#line:280
                    OOOOO00OO00O0O0OO ["proposed_fine"]=OO000OO0O0OO0O0OO [-1 ].text .strip ()#line:281
                elif OO000OO0O0OO0O0OO and len (OO000OO0O0OO0O0OO )>0 and len (OO0O0OOOO000000O0 )>0 :#line:284
                    O0OOOOOOO0000O0OO ={}#line:285
                    for OOO0O0O0O00O0O0OO ,OOO0OO000O0OOO000 in enumerate (OO000OO0O0OO0O0OO ):#line:286
                        if OOO0O0O0O00O0O0OO <len (OO0O0OOOO000000O0 ):#line:287
                            OOOOO0000O000OO00 =OOO0OO000O0OOO000 .text .strip ()#line:288
                            if OOOOO0000O000OO00 :#line:289
                                O0OOOOOOO0000O0OO [OO0O0OOOO000000O0 [OOO0O0O0O00O0O0OO ]]=OOOOO0000O000OO00 #line:290
                    if O0OOOOOOO0000O0OO and len (O0OOOOOOO0000O0OO )>1 :#line:292
                        OOOOO00OO00O0O0OO ["offence_details"].append (O0OOOOOOO0000O0OO )#line:293
        if not OOOOO00OO00O0O0OO ["case_details"]:#line:296
            del OOOOO00OO00O0O0OO ["case_details"]#line:297
        if not OOOOO00OO00O0O0OO ["current_status"]:#line:298
            del OOOOO00OO00O0O0OO ["current_status"]#line:299
        if not OOOOO00OO00O0O0OO ["offence_details"]:#line:300
            del OOOOO00OO00O0O0OO ["offence_details"]#line:301
        if not OOOOO00OO00O0O0OO ["proposed_fine"]:#line:302
            del OOOOO00OO00O0O0OO ["proposed_fine"]#line:303
        print ("\nExtracted data as JSON:")#line:306
        print (json .dumps (OOOOO00OO00O0O0OO ,indent =2 ,ensure_ascii =False ))#line:307
        return OOOOO00OO00O0O0OO #line:309
    except Exception as OO0O000000O000OOO :#line:311
        print (f"Error extracting table data: {str(OO0O000000O000OOO)}")#line:312
        import traceback #line:313
        traceback .print_exc ()#line:314
        return None #line:315
def read_challan_numbers (OO0O0OOOO0O00O000 ):#line:318
    try :#line:319
        if not os .path .exists (OO0O0OOOO0O00O000 ):#line:321
            print (f"Input file {OO0O0OOOO0O00O000} not found!")#line:322
            return []#line:323
        O0OOO0OO0O0OOO00O =pd .read_excel (OO0O0OOOO0O00O000 ,engine ='openpyxl')#line:326
        if 'challan_no'not in O0OOO0OO0O0OOO00O .columns :#line:329
            print ("Error: Column 'challan_no' not found in Excel file!")#line:330
            print (f"Available columns: {', '.join(O0OOO0OO0O0OOO00O.columns)}")#line:331
            return []#line:332
        OOOOO00000OOOOO00 =str (O0OOO0OO0O0OOO00O ['challan_no'].iloc [0 ]).strip ()#line:335
        print (f"Processing first challan number: {OOOOO00000OOOOO00}")#line:336
        return [OOOOO00000OOOOO00 ]#line:337
    except Exception as OO0O0O000OOOO0OOO :#line:339
        print (f"Error reading Excel: {str(OO0O0O000OOOO0OOO)}")#line:340
        print ("Please ensure you have installed required packages:")#line:341
        print ("pip install pandas openpyxl")#line:342
        return []#line:343
def save_to_excel (OOO0O0O0OO0OOO0OO ):#line:345
    try :#line:346
        if not OOO0O0O0OO0OOO0OO :#line:347
            print ("No data to save!")#line:348
            return False #line:349
        OOOOOOO0O00OOO000 =pd .DataFrame (OOO0O0O0OO0OOO0OO )#line:352
        OO0OOOOO0OO000OO0 =datetime .now ().strftime ("%Y%m%d_%H%M%S")#line:355
        with open (f"challan_results_{OO0OOOOO0OO000OO0}.json",'w',encoding ='utf-8')as OO00O000O00000O00 :#line:363
            json .dump (OOO0O0O0OO0OOO0OO ,OO00O000O00000O00 ,indent =2 ,ensure_ascii =False )#line:364
        print (f"Results also saved to challan_results_{OO0OOOOO0OO000OO0}.json")#line:365
        return True #line:367
    except Exception as OO0O0OO00O00000O0 :#line:369
        print (f"Error saving to Excel: {str(OO0O0OO00O00000O0)}")#line:370
        print ("Please ensure you have installed required packages:")#line:371
        print ("pip install pandas openpyxl")#line:372
        return False #line:373
def automate_virtual_court (challan_no =None ):#line:375
    try :#line:377
        import openpyxl #line:378
    except ImportError :#line:379
        print ("Required package 'openpyxl' not found!")#line:380
        print ("Please install it using: pip install openpyxl")#line:381
        return #line:382
    OO00OO00000OOO000 =setup_driver ()#line:384
    OOOOOO00OOO0O000O =[]#line:385
    try :#line:387
        print (f"\nProcessing challan number: {challan_no}")#line:396
        OO00OO00000OOO000 .get ("https://vcourts.gov.in/virtualcourt/index.php")#line:398
        select_department (OO00OO00000OOO000 ,'HR')#line:401
        time .sleep (1 )#line:402
        click_proceed_button (OO00OO00000OOO000 )#line:403
        time .sleep (2 )#line:404
        click_challan_vehicle_tab (OO00OO00000OOO000 )#line:407
        time .sleep (2 )#line:408
        enter_challan_number (OO00OO00000OOO000 ,challan_no )#line:409
        submit_captcha (OO00OO00000OOO000 )#line:411
        time .sleep (10 )#line:412
        click_view_link (OO00OO00000OOO000 )#line:415
        time .sleep (10 )#line:416
        O00OO0O0O0OOO0O00 =extract_table_data (OO00OO00000OOO000 )#line:418
        if O00OO0O0O0OOO0O00 :#line:419
            OOOO00OO0000OO00O ={'challan_no':challan_no }#line:423
            for O00O00000OOO0000O ,O0O000000O00O000O in O00OO0O0O0OOO0O00 .get ('case_details',{}).items ():#line:426
                OOOO00OO0000OO00O [f"case_{O00O00000OOO0000O}"]=O0O000000O00O000O #line:427
            for O00O00000OOO0000O ,O0O000000O00O000O in O00OO0O0O0OOO0O00 .get ('current_status',{}).items ():#line:430
                OOOO00OO0000OO00O [f"status_{O00O00000OOO0000O}"]=O0O000000O00O000O #line:431
            if O00OO0O0O0OOO0O00 .get ('proposed_fine'):#line:434
                OOOO00OO0000OO00O ['proposed_fine']=O00OO0O0O0OOO0O00 ['proposed_fine']#line:435
            if O00OO0O0O0OOO0O00 .get ('offence_details')and len (O00OO0O0O0OOO0O00 ['offence_details'])>0 :#line:438
                for O00O00000OOO0000O ,O0O000000O00O000O in O00OO0O0O0OOO0O00 ['offence_details'][0 ].items ():#line:439
                    OOOO00OO0000OO00O [f"offence_{O00O00000OOO0000O}"]=O0O000000O00O000O #line:440
            OOOO00OO0000OO00O ['full_data_json']=json .dumps (O00OO0O0O0OOO0O00 ,ensure_ascii =False )#line:443
            OOOOOO00OOO0O000O .append (OOOO00OO0000OO00O )#line:445
        save_to_excel (OOOOOO00OOO0O000O )#line:453
        time .sleep (5 )#line:454
    except Exception as OOOOO00O00OO00000 :#line:456
        print (f"Error occurred: {str(OOOOO00O00OO00000)}")#line:457
        import traceback #line:458
        traceback .print_exc ()#line:459
    finally :#line:460
        input ("Press Enter to close the browser...")#line:461
        OO00OO00000OOO000 .quit ()#line:462

app =Flask (__name__ )#line:15
@app .route ('/search',methods =['GET','POST'])#line:17
def search_challan ():#line:18
    if request .method =='GET':#line:19
        O0OOO000O0O000O0O =request .args .get ('challan')#line:20
        if O0OOO000O0O000O0O :#line:21
            try :#line:22
                O0O00O00000O00OO0 =setup_driver ()#line:23
                O0O00O00000O00OO0 .get ("https://vcourts.gov.in/virtualcourt/index.php")#line:25
                O0O0000O0OOO000OO =select_department (O0O00O00000O00OO0 ,'HR')#line:28
                if not O0O0000O0OOO000OO :#line:29
                    return jsonify ({"error":"Failed to select department"}),500 #line:30
                time .sleep (1 )#line:32
                O00000O00O0OO0OOO =click_proceed_button (O0O00O00000O00OO0 )#line:33
                if not O00000O00O0OO0OOO :#line:34
                    return jsonify ({"error":"Failed to proceed"}),500 #line:35
                time .sleep (2 )#line:37
                O000O000O00O0000O =click_challan_vehicle_tab (O0O00O00000O00OO0 )#line:40
                if not O000O000O00O0000O .get ("status"):#line:41
                    return jsonify ({"error":O000O000O00O0000O .get ("message")}),500 #line:42
                time .sleep (2 )#line:44
                enter_challan_number (O0O00O00000O00OO0 ,O0OOO000O0O000O0O )#line:45
                submit_captcha (O0O00O00000O00OO0 )#line:47
                time .sleep (4 )#line:48
                click_view_link (O0O00O00000O00OO0 )#line:51
                time .sleep (1 )#line:52
                O0O0OOOO00OO00OO0 =extract_table_data (O0O00O00000O00OO0 )#line:54
                O0O00O00000O00OO0 .quit ()#line:57
                if O0O0OOOO00OO00OO0 :#line:59
                    return jsonify (O0O0OOOO00OO00OO0 )#line:61
                else :#line:62
                    return jsonify ({"error":"No data found for the given challan number"}),404 #line:63
            except Exception as OOOO0OOOO000O0O0O :#line:65
                return jsonify ({"error":str (OOOO0OOOO000O0O0O )}),500 #line:66
            finally :#line:67
                if 'driver'in locals ():#line:68
                    O0O00O00000O00OO0 .quit ()#line:69
if __name__ =='__main__':#line:74
    app .run (debug =True )#line:75

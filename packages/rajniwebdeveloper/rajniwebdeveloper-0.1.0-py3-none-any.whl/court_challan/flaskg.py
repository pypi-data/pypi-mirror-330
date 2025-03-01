from flask import Flask ,render_template ,request ,redirect ,url_for ,flash ,jsonify #line:1
from datetime import datetime #line:2
from app import (setup_driver ,select_department ,click_proceed_button ,click_challan_vehicle_tab ,enter_challan_number ,submit_captcha ,click_view_link ,extract_table_data )#line:12
import time #line:13
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

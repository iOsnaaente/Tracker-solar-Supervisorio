import dearpygui.dearpygui    as dpg
from datetime import datetime as dt 
from registry import * 
from themes   import * 

def add_image_loaded( img_path ):
    w, h, c, d = dpg.load_image( img_path )
    with dpg.texture_registry() as reg_id : 
        return dpg.add_static_texture( w, h, d, parent = reg_id )

def change_font():
    with dpg.font_registry( id = 'fonts' ):
            dpg.add_font( PATH + '\\fonts\\verdana.ttf', 14, default_font=True, parent='fonts')

def convert_to_timestamp(dates):
    ts = []
    date_format = '%m/%d/%y %H:%M'
    for d in dates:
        d = dt.strptime(d, date_format)
        ts.append(dt.timestamp(d))
    return ts

#import   inspect 
#print(inspect.stack())

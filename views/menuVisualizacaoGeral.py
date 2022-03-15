import dearpygui.dearpygui as dpg 
import datetime            as dt
import math 

from registry              import * 

SUN_DATA.update_date() 

# FUNCTIONS 
def get_semi_circle_points( center, radius, angle_i, angle_f, segments = 360, closed = False ):
    points_close = [[ center[0], center[1]-radius ] ,  center, [ center[0] + radius, center[1] ] ] 
    angles = [ ((angle_f - angle_i)/segments)*n for n in range(segments) ] 
    points =  [ [ center[0] + radius*math.cos(ang), center[1] - radius*math.sin(ang) ] for ang in angles ] 
    if closed: 
        points_close.extend( points )
        return points_close 
    else:      
        return points 

def draw_sun_trajetory( draw_id, parent_id, all_day = False, extremes = False ):
    # Ponto central, dimensões da tela e Raio 
    width, height = dpg.get_item_width( draw_id ), dpg.get_item_height( draw_id )
    center        = [ width//2, height//2 ]
    r             =   width//2 - 20 if width+20 <= height else height//2 - 20
    id_link       = draw_id*100

    # DESENHO DA LINHA DE NASCER DO SOL E POR DO SOL 
    azi = SUN_DATA.get_pos_from_date( SUN_DATA.rising )[1]
    alt = SUN_DATA.get_pos_from_date( SUN_DATA.sunset )[1] # [ alt , azi ]

    # PEGA OS ANGULOS NOS PONTOS DA TRAJETÓRIA DO SOL 
    dots = SUN_DATA.trajetory(100, all_day )
    # PONTOS DE ACORDO COM Azimute - Altitude 
    dots = [ [ x - math.pi/2 ,  y ] for x, y, _ in dots ]
    dots = [ [ center[0] + math.cos(x)*r, center[1] + math.sin(x)*math.cos(y)*r ] for x, y in dots ]

    # DESENHO DO SOL NA SUA POSIÇÃO 
    sun = [  SUN_DATA.azi - math.pi/2, SUN_DATA.alt ] 
    sun = [ center[0] + math.cos(sun[0])*r, center[1] + math.sin(sun[0])*math.cos(sun[1])*r ]
    
    dpg.draw_line(     parent = draw_id, tag = id_link+1 , p1     = [center[0] - r, center[1]]              , p2     = [center[0] + r, center[1]]                                          , color = COLOR['gray'](155)  , thickness = 1 )
    dpg.draw_line(     parent = draw_id, tag = id_link+2 , p1     = center                                  , p2     = [center[0] + r*math.cos(azi-math.pi/2), center[1] + r*math.sin(azi-math.pi/2)], color = COLOR['orange'](155), thickness = 2 )
    dpg.draw_line(     parent = draw_id, tag = id_link+3 , p1     = center                                  , p2     = [center[0] + r*math.cos(alt-math.pi/2), center[1] + r*math.sin(alt-math.pi/2)], color = COLOR['gray'](200)  , thickness = 2 )
    dpg.draw_circle(   parent = draw_id, tag = id_link+4 , center = center                                  , radius = r                                                                   , color = COLOR['white'](200) , fill      = COLOR['white'](10 ), thickness = 3 )
    dpg.draw_circle(   parent = draw_id, tag = id_link+5 , center = center                                  , radius = 3                                                                   , color = COLOR['white'](200) , fill      = COLOR['white'](255), thickness = 2 )
    dpg.draw_text(     parent = draw_id, tag = id_link+6 , pos    = [center[0] -(r +20), center[1] -10 ]    , text   = 'W'                                                                 , color = COLOR['white'](200) , size      = 20 )
    dpg.draw_text(     parent = draw_id, tag = id_link+7 , pos    = [center[0] +(r +5) , center[1] -10 ]    , text   = 'E'                                                                 , color = COLOR['white'](200) , size      = 20 )
    dpg.draw_text(     parent = draw_id, tag = id_link+8 , pos    = [center[0] -10     , center[1] -(r +25)], text   = 'N'                                                                 , color = COLOR['white'](255) , size      = 20 )
    dpg.draw_polyline( parent = draw_id, tag = id_link+9 , points = dots                                    , color  = COLOR['red'](155)                                                    , thickness = 2                   , closed    = False )
    for n, p in enumerate(dots):
        dpg.draw_circle( parent = draw_id, tag = id_link+(12+n) , center = p     , radius = 2  , color = [n*4, 255-n*2, n*2, 255]                              ) 
    dpg.draw_line(       parent = draw_id, tag = id_link+10     , p1     = center, p2     = sun, color = COLOR['yellow'](200)    , thickness = 2               )
    dpg.draw_circle(     parent = draw_id, tag = id_link+11     , center = sun   , radius = 10 , color = COLOR['yellow'](155)    , fill = COLOR['yellow'](255) )

def update_sun_trajetory( draw_id, parent_id, all_day = False ): 
    # Ponto central, dimensões da tela e Raio 
    width, height = dpg.get_item_width( draw_id ), dpg.get_item_height( draw_id )
    w, h          = dpg.get_item_width( 'mainWindow' ) , dpg.get_item_height('mainWindow' )
    center        = [ width//2, height//2 ]
    r             = width//2 - 20 if width+20 <= height else height//2 - 20
    id_link       = draw_id*100
    
    # DESENHO DA LINHA DE NASCER DO SOL E POR DO SOL 
    azi = SUN_DATA.get_pos_from_date( SUN_DATA.rising )[1]
    alt = SUN_DATA.get_pos_from_date( SUN_DATA.sunset )[1] # [ alt , azi ]
    
    # PEGA OS ANGULOS NOS PONTOS DA TRAJETÓRIA DO SOL 
    dots = SUN_DATA.trajetory(100, all_day )
    dots = [ [ x - math.pi/2 ,  y ] for x, y, _ in dots ]
    dots = [ [ center[0] + math.cos(x)*r, center[1] + math.sin(x)*math.cos(y)*r ] for x, y in dots ]
    
    # DESENHO DO SOL NA SUA POSIÇÃO 
    sun = [  SUN_DATA.azi - math.pi/2, SUN_DATA.alt ] 
    sun = [ center[0] + math.cos(sun[0])*r, center[1] + math.sin(sun[0])*math.cos(sun[1])*r ]
    
    # DESENHO ESTÁTICO
    dpg.configure_item( id_link+1 , p1     = [center[0] - r, center[1]], p2     = [center[0] + r, center[1]]                                           )
    dpg.configure_item( id_link+2 , p1     = center                    , p2     = [center[0] + r*math.cos(azi-math.pi/2), center[1] + r*math.sin(azi-math.pi/2)] )
    dpg.configure_item( id_link+3 , p1     = center                    , p2     = [center[0] + r*math.cos(alt-math.pi/2), center[1] + r*math.sin(alt-math.pi/2)] )
    dpg.configure_item( id_link+4 , center = center                    , radius = r      )
    dpg.configure_item( id_link+5 , center = center                    , radius = 3      )
    dpg.configure_item( id_link+6 , pos    = [center[0] - (r + 20), center[1] -10 ]      )
    dpg.configure_item( id_link+7 , pos    = [center[0] + (r +  5), center[1] -10 ]      )
    dpg.configure_item( id_link+8 , pos    = [center[0] - 10 , center[1] - (r + 25) ]    )
    dpg.configure_item( id_link+9 , points = dots                                        )
    dpg.configure_item( id_link+10, p1     = center                    , p2     = sun    )
    dpg.configure_item( id_link+11, center = sun                                         )
    for n, p in enumerate(dots):
        dpg.configure_item( id_link+(12+n) , center = p )

def att_sunpos_graphs( ):
    last_date = SUN_DATA.date
    if not dpg.get_value( HORA_MANUAL ): SUN_DATA.set_date( dt.datetime.utcnow() )  
    else:                                SUN_DATA.set_date( dt.datetime( dpg.get_value(YEAR), dpg.get_value(MONTH), dpg.get_value(DAY), dpg.get_value(HOUR), dpg.get_value(MINUTE), dpg.get_value(SECOND) ) )    
    
    azi_alt = SUN_DATA.trajetory( 50, all_day = False )
    SUN_DATA.set_date( last_date )

    AZI = [] 
    ALT = [] 
    PTI = [] 
    for azi, alt, tim in azi_alt: 
        AZI.append( math.degrees(azi - math.pi) if azi > math.pi else math.degrees(azi + math.pi) )
        ALT.append( math.degrees(alt) if alt < math.pi else 0  )
        PTI.append( int( dt.datetime.timestamp( tim )) ) 
    
    azi, alt  = [math.degrees(SUN_DATA.azi)], [math.degrees(SUN_DATA.alt)]
    time_scrt = [math.degrees(dt.datetime.timestamp( last_date ))]
    
    SUN_DATA.set_date( last_date )

    dpg.configure_item (22_13, x    = PTI      , y    = AZI     )
    dpg.configure_item (22_14, x    = time_scrt, y    = azi )
    dpg.set_axis_limits(22_11, ymin = PTI[0]   , ymax = PTI[-1] )
    dpg.configure_item (22_23, x    = PTI      , y    = ALT     )
    dpg.configure_item (22_24, x    = time_scrt, y    = alt )
    dpg.set_axis_limits(22_21, ymin = PTI[0]   , ymax = PTI[-1] )


# MAIN FUNCTIONS 
def init_visualizacaoGeral( windows : dict ):
    # POSIÇÂO DO SOL 
    with dpg.window( label = 'Posição solar' , tag = 21_0, pos      = [50,50], width    = 500  , height      = 500 , no_move  = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar= True ) as Posicao_sol_VG:
        windows["Visualizacao geral"].append( Posicao_sol_VG )
        w, h = dpg.get_item_width(2_1_0), dpg.get_item_height(2_1_0)
        dpg.add_drawlist   ( tag      = 21_1_0, width     = w-20  , height = h-50, label = 'Solar')
        draw_sun_trajetory ( draw_id = 2_1_1_0, parent_id = 2_1_0 )

    # VISOR DAS POSIÇÔES DO SOL - USAR GRÀFICOS - MESMO DO TOOLTIP 
    with dpg.window( label = 'Atuação'       , tag = 22_0, no_move  = True   , no_resize = True, no_collapse = True, no_close = True ) as Atuacao_VG:
        windows["Visualizacao geral"].append( Atuacao_VG )
        dpg.add_text('Área para a atução da posição dos paineis solares')
        with dpg.group( horizontal = True ): 
            with dpg.plot( tag = 2_2_1_0, label = 'Azimute do dia', height = 312, width = 478, anti_aliased = True ): 
                dpg.add_plot_legend()
                dpg.add_plot_axis( dpg.mvXAxis, label = 'Hora [h]'  , tag = 2_2_1_1, parent = 2_2_1_0, time = True ) # X
                dpg.add_plot_axis( dpg.mvYAxis, label = 'Angulo [º]', tag = 2_2_1_2, parent = 2_2_1_0 ) # Y 
                dpg.set_axis_limits_auto( 2_2_1_1 )
                dpg.set_axis_limits     ( 2_2_1_2, -5, 370 )
                dpg.add_line_series     ( [], [], tag = 2_2_1_3, label = 'Rota diária', parent = 2_2_1_2 )
                dpg.add_scatter_series  ( [], [], tag = 2_2_1_4, label = 'Ponto atual', parent = 2_2_1_2 ) 
       
            with dpg.plot( tag = 2_2_2_0, label = 'Altitude do dia', height = 312, width = 478, anti_aliased = True ): 
                dpg.add_plot_axis( dpg.mvXAxis, label = 'Hora [h]'  , tag = 2_2_2_1, parent = 2_2_2_0, time = True ) # X
                dpg.add_plot_axis( dpg.mvYAxis, label = 'Angulo [º]', tag = 2_2_2_2, parent = 2_2_2_0 ) # Y 
                dpg.set_axis_limits_auto( 2_2_2_1 )
                dpg.set_axis_limits     ( 2_2_2_2, -5, 100 )
                dpg.add_plot_legend()
                dpg.add_line_series     ( [], [], tag = 2_2_2_3, label = 'Rota diária', parent = 2_2_2_2 )
                dpg.add_scatter_series  ( [], [], tag = 2_2_2_4, label = 'Ponto atual', parent = 2_2_2_2 ) 
            
            att_sunpos_graphs( ) 
        
    # CONFIGURAÇÔES DE TEMPO - USAR WINDOW NO HOUR_MANUAL 
    with dpg.window( label = 'Painel de log' , tag = 23_0, no_move  = True   , no_resize = True, no_collapse = True, no_close = True, no_title_bar = True ) as Painel_log_VG:
        windows["Visualizacao geral"].append( Painel_log_VG )
        
        dpg.add_text( default_value = 'Informações gerais do sistema')
        
        with dpg.child_window( tag = 23_00, autosize_x = True, height = 170, menubar = True):
            with dpg.menu_bar( tag = 23_01, label = 'menubar para datetime',):
                dpg.add_menu_item( tag = 23_02, label = 'Hora automática', callback = lambda s, d, u : dpg.set_value(HORA_MANUAL, False), shortcut = 'A data e hora de calculo é definida automaticamente de acordo com a hora do controlador local')
                dpg.add_menu_item( tag = 23_03, label = 'Hora manual'    , callback = lambda s, d, u : dpg.set_value(HORA_MANUAL, True) , shortcut = 'A data e hora de calculo é definida pela entrada do operador no supervisório' )

            with dpg.child_window( tag = 23_10):
                #Informações gerais do sistema - Automático 
                dpg.add_text( default_value = 'Hora automática')
                dpg.add_drag_floatx( tag = 23_1, label = 'Ano/Mes/Dia Auto'  , size = 3, format = '%.0f', speed = 0.1 , min_value = 1   , max_value = 3000   , no_input = True )
                dpg.add_drag_floatx( tag = 23_2, label = 'Hora/Min/Sec Auto' , size = 3, format = '%.0f', speed = 0.1 , no_input  = True                                                                             )
                dpg.add_drag_int   ( tag = 23_3, label = 'Valor no dia'      , format = '%.0f'          , speed = 0.1 , min_value = 0   , max_value = 26*3600, no_input = True, source = TOT_SECONDS, enabled = False)
                dpg.add_drag_int   ( tag = 23_4, label = 'Dia Juliano'       , format = '%.0f'          , speed = 0.1 , min_value = 0   , max_value = 366    , no_input = True, source = JULIANSDAY , enabled = False)
           
            with dpg.child_window( tag = 23_20):
                # Informações gerais do sistema - Manual  
                dpg.add_text( default_value = 'Hora manual')
                dpg.add_input_floatx( tag = 23_6, label = 'Ano/Mes/Dia Manual' , size = 3, default_value = [2020, 12, 25], format='%.0f', min_value = 1, max_value = 3000 )
                dpg.add_input_floatx( tag = 23_7, label = 'Hora/Min/Sec Manual', size = 3, default_value = [20, 30, 10]  , format='%.0f', min_value = 1, max_value = 60   )
                dpg.add_drag_int    ( tag = 23_8, label = 'Valor no dia'       , format = '%.0f', speed = 0.1 , min_value = 0, max_value = 24*3600, no_input = True, source = TOT_SECONDS, enabled = False )
                dpg.add_drag_int    ( tag = 23_9, label = 'Dia Juliano'        , format = '%.0f', speed = 0.1 , min_value = 0, max_value = 366    , no_input = True, source = JULIANSDAY , enabled = False )

            dpg.hide_item( 23_20 ) if dpg.get_value(HORA_MANUAL) == False else dpg.hide_item( 2_3_1_0 )
        
        dpg.add_spacer( height = 5 )
        with dpg.child_window( tag = 2_3_3_0, autosize_x = True, autosize_y = True ): 
            # Definições de longitude e latitude local
            with dpg.child_window  ( height = 90 ):
                dpg.add_text       ( default_value = 'Definições de longitude e latitude local')
                dpg.add_input_float( label = 'Latitude' , tag = 2_3_10, min_value = -90, max_value = 90, format = '%3.8f', indent=0.01, source = LATITUDE , callback = lambda sender, data, user : SUN_DATA.set_latitude( data ) )
                dpg.add_spacer     ( )
                dpg.add_input_float( label = 'Longitude', tag = 2_3_11, min_value = -90, max_value = 90, format = '%3.8f', indent=0.01, source = LONGITUDE, callback = lambda sender, data, user : SUN_DATA.set_longitude( data ) )
            
            dpg.add_spacer( height = 5 )
            with dpg.child_window( height = 150 ): 
                # Informações do sol 
                dpg.add_text       ( default_value = 'Informacoes do sol')
                dpg.add_drag_float ( label = 'Azimute'      , tag = 23_12, format='%4.2f', speed=1, no_input= True, source = AZIMUTE )
                dpg.add_spacer     ( )
                dpg.add_drag_float ( label = 'Altitude'     , tag = 23_13, format='%4.2f', speed=1, no_input= True, source = ZENITE )
                dpg.add_spacer     ( )
                dpg.add_drag_float ( label = 'Elevação (m)' , tag = 23_14, format='%4.0f', speed=1, no_input= True, source = ALTITUDE )
                dpg.add_spacer     ( )
                dpg.add_drag_floatx( label = 'Horas de sol' , tag = 23_15, size = 3, format='%.0f', no_input= True )
            
            dpg.add_spacer( height = 5 )
            with dpg.child_window( height = 200 ):
                # Posições de interesse
                dpg.add_text       ( default_value = "Posicoes de interesse", )
                dpg.add_text       ( default_value = 'Nascer do sol (hh/mm/ss)')
                dpg.add_drag_floatx( tag = 2_3_16, size = 3, format='%.0f', speed=1, no_input= True, callback = lambda sender, data, user : dpg.set_value( H_SUNRISE     , data.extend([0]))  )
                dpg.add_spacer     ( )
                dpg.add_text       ( default_value = 'Culminante (hh/mm/ss)'   )
                dpg.add_drag_floatx( tag = 2_3_17, size = 3, format='%.0f', speed=1, no_input= True, callback = lambda sender, data, user : dpg.set_value( H_SUNSET      , data.extend([0]))  )
                dpg.add_spacer     ( )
                dpg.add_text       ( default_value = 'Por do sol (hh/mm/ss)'   )
                dpg.add_drag_floatx( tag = 2_3_18, size = 3, format='%.0f', speed=1, no_input= True, callback = lambda sender, data, user : dpg.set_value( H_CULMINANT, data.extend([0]))  )

    dpg.hide_item( 21_0 )
    dpg.hide_item( 22_0 )
    dpg.hide_item( 23_0 )

def resize_visualizacaoGeral( ):
    # get the main_window dimension 
    w , h  = dpg.get_item_width( 'mainWindow' ), dpg.get_item_height( 'mainWindow' ) 
    
    dpg.configure_item( 21_0    , width = w*2/3   , height    = h*3/5       , pos = [10 , 25 ]               ) # DRAWING 
    dpg.configure_item( 22_0    , width = w*2/3   , height    = (h*2/5)-35  , pos = [10 , (h*3/5)+30 ]       ) # SUNPATH
    dpg.configure_item( 23_0    , width = w/3 -20 , height    =  h - 30     , pos = [ w*2/3 +15, 25 ]        ) # LOG 
    
    # get the child_window_window dimension 
    w1, h1 = dpg.get_item_width( 21_0 ), dpg.get_item_height( 21_0 ) 
    dpg.configure_item( 21_10  , width = w1-20       , height    = h1-50                                        ) # DRAWLIST
    update_sun_trajetory(     draw_id = 2_1_1_0    , parent_id = 2_1_0                                        ) # DRAWING 

    # SUNPATH ATT CHILD_WINDOW 
    dpg.configure_item( 22_10  , width = (w/3)-15    , height    = (h*2/5)*0.8 , pos = [ 5            , 20 ]    ) # GIRO
    dpg.configure_item( 22_20  , width = (w/3)-15    , height    = (h*2/5)*0.8 , pos = [ (w*2/3)//2 +5, 20 ]    ) # ELEVAÇÃO 

def render_visualizacaoGeral( ):
    global TOT_SECONDS , JULIANSDAY, HORA_MANUAL
    global HOUR, MINUTE, SECOND
    global YEAR, MONTH , DAY

    # Horário automático 
    if dpg.get_value( HORA_MANUAL ) == False :
        SUN_DATA.update_date()
        dpg.set_value( 23_1, value = [ dpg.get_value(YEAR), dpg.get_value(MONTH) , dpg.get_value(DAY)   ] )  # DIA ATUTOMÁTICO 
        dpg.set_value( 23_2, value = [ dpg.get_value(HOUR), dpg.get_value(MINUTE), dpg.get_value(SECOND)] )  # HORA AUTOMÁTICA
        dpg.hide_item( 23_2_0 )
        dpg.show_item( 23_1_0 )

    # Horário manual 
    else:        
        yearm, monthm, daym     = dpg.get_value( 23_6 )[:-1]
        hourm, minutem, secondm = dpg.get_value( 23_7 )[:-1]
        try:
            data = dt.datetime( int(yearm), int(monthm), int(daym), int(hourm), int(minutem), int(secondm) )
            dt.datetime.timestamp( data )
            SUN_DATA.set_date( data )
            SUN_DATA.update()
            dpg.set_value(YEAR  , yearm  )
            dpg.set_value(MONTH , monthm )
            dpg.set_value(DAY   , daym   ) 
            dpg.set_value(HOUR  , hourm  )
            dpg.set_value(MINUTE, minutem)
            dpg.set_value(SECOND, secondm)
        except:
            pass 

        # Total de segundos no dia
        dpg.set_value( 23_9, SUN_DATA.dia_juliano   )                              # DIA JULIANO
        dpg.set_value( 23_8, SUN_DATA.total_seconds)                               # TOTAL DE SEGUNDOS 
        
        dpg.hide_item( 23_1_0 )
        dpg.show_item( 23_2_0 )
        
    # Setar o Azimute, Altitude e Elevação
    dpg.set_value( 23_12, math.degrees( SUN_DATA.azi) )                            #  AZIMUTE               
    dpg.set_value( 23_13, math.degrees( SUN_DATA.alt) )                            #  ALTITUDE               
    dpg.set_value( 23_14, SUN_DATA.altitude           )                            #  ELEVAÇÃO

    # Seta as horas do sol calculando as horas minutos e segundos de segundos totais 
    diff_sunlight = (SUN_DATA.sunset - SUN_DATA.rising).seconds
    dpg.set_value( 2_3_15, [diff_sunlight//3600, (diff_sunlight//60)%60 , diff_sunlight%60 ] )

    # Setar as informações de Nascer do sol, Culminante (ponto mais alto) e Por do sol
    dpg.set_value( 23_16, [ SUN_DATA.rising.hour+SUN_DATA.utc_local , SUN_DATA.rising.minute , SUN_DATA.rising.second  ] ) # 'Nascer do sol'
    dpg.set_value( 23_17, [ SUN_DATA.transit.hour+SUN_DATA.utc_local, SUN_DATA.transit.minute, SUN_DATA.transit.second ] ) # 'Culminante'   
    dpg.set_value( 23_18, [ SUN_DATA.sunset.hour+SUN_DATA.utc_local , SUN_DATA.sunset.minute , SUN_DATA.sunset.second  ] ) # 'Por do sol'      

    update_sun_trajetory( draw_id = 21_1_0 , parent_id = 21_0 )
    att_sunpos_graphs()
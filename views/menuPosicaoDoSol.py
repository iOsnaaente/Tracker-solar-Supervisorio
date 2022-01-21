from dearpygui.dearpygui    import *

from registry               import *
from numpy                  import array
import math 

IMG       =  PATH + '\\img\\Tracker_nobg.png'
AZI_Angle = math.degrees(get_value( MG_Angle ) ) 
ALT_Angle = math.degrees(get_value( ME_Angle ) ) 
center    = 0
radius    = 0

# FUNÇÕES        
def draw_semi_circle( parent : Union[str, int], id : Union[str, int], center : list, radius : float, angle_i : float , angle_f : float, color : list, segments : int = 360, closed : bool = False, thickness : int = 1 ):
        angles = [ ((angle_f - angle_i)/segments)*n for n in range(segments) ] 
        points = [ [ center[0] + radius*math.cos(ang), center[1] - radius*math.sin(ang) ] for ang in angles ]
        draw_id = draw_polyline ( parent = parent, id = id, points = points, color= color, closed = closed, thickness= thickness )

def circle_angles( angle_initial : float , range_arc : float , points_number : int, convert_to_radians : bool = True ):
    if convert_to_radians: 
        angle_initial = math.radians(angle_initial)
        range_arc = math.radians(range_arc)
    dif_dom = range_arc / points_number if points_number > 0 else 0 
    dom     = [ angle_initial+(i*dif_dom) for i in range(points_number)]
    points  = [ [math.cos(angle), math.sin(angle)] for angle in dom ]
    return points

ROT_X = lambda angle_to_rotate : array([ [ 1, 0, 0 ], [ 0, math.cos(angle_to_rotate), -math.sin(angle_to_rotate) ], [ 0, math.sin(angle_to_rotate),  math.cos(angle_to_rotate) ]])
ROT_Y = lambda angle_to_rotate : array([ [ math.cos(angle_to_rotate), 0, -math.sin(angle_to_rotate) ],[ 0, 1, 0 ],[ math.sin(angle_to_rotate), 0, math.cos(angle_to_rotate) ]])
ROT_Z = lambda angle_to_rotate : array([ [ math.cos(angle_to_rotate), -math.sin(angle_to_rotate), 0 ],[ math.sin(angle_to_rotate), math.cos(angle_to_rotate) , 0 ],[ 0, 0, 1 ]])

def rotate_x( angles_to_convert : list , angle_to_rotate : float, convert_to_3D : bool = False, convert_to_radians : bool = False ): 
    global ROT_X
    if convert_to_radians:  angle_to_rotate = math.radians( angle_to_rotate )
    if convert_to_3D:
        angles_to_convert = array([ [x,y,0] for x, y in angles_to_convert ])
        angles_converted = [ angles.dot(ROT_X(angle_to_rotate)) for angles in angles_to_convert ]
        angles_converted = [ [x,y] for x, y, _ in angles_converted ]
    else:
        angles_to_convert = array( angles_to_convert ) 
        angles_converted = [ angles.dot(ROT_X(angle_to_rotate)) for angles in angles_to_convert ]
    return angles_converted 

def rotate_y( angles_to_convert : list, angle_to_rotate : float, convert_to_3D : bool = False, convert_to_radians : bool = False ): 
    global ROT_Y
    if convert_to_radians:  angle_to_rotate = math.radians( angle_to_rotate )        
    if convert_to_3D:
        angles_to_convert = array([ [x,y,0] for x, y in angles_to_convert ])
        angles_converted = [ angles.dot(ROT_Y(angle_to_rotate)) for angles in angles_to_convert ]
        angles_converted = [ [x,y] for x, y, _ in angles_converted ]
        return angles_converted
    else:
        angles_to_convert = array( angles_to_convert ) 
        angles_converted = [ angles.dot(ROT_Y(angle_to_rotate)) for angles in angles_to_convert ]
        return angles_converted 

def rotate_z( angles_to_convert : list, angle_to_rotate : float, convert_to_3D : bool = False, convert_to_radians : bool = False ): 
    global ROT_Z
    if convert_to_radians:  angle_to_rotate = math.radians( angle_to_rotate )              
    if convert_to_3D:
        angles_to_convert = array([ [x,y,0] for x, y in angles_to_convert ])
        angles_converted = [ angles.dot(ROT_Z(angle_to_rotate)) for angles in angles_to_convert ]
        angles_converted = [ [x,y] for x, y, _ in angles_converted ]
        return angles_converted
    else:
        angles_to_convert = array( angles_to_convert ) 
        angles_converted = [ angles.dot(ROT_Z(angle_to_rotate)) for angles in angles_to_convert ]
        return angles_converted 

def ellipse_points( rmax : float, rmin : float, z_axis : bool = False  ): 
    c_angles = circle_angles( 0, 360, 180, convert_to_radians=True ) 
    if z_axis:  c_rotated = rotate_x( c_angles, (math.pi/2-2*math.atan(rmin/rmax )), False )
    else:       c_rotated = rotate_x( c_angles, (math.pi/2-2*math.atan(rmin/rmax )), True  )
    return c_rotated 

def draw_solar_sphere( parent : Union[int, str], id : Union[int, str], center : list, rmax : float, rmin : float, thickness : int = 20 ): 
    e_points_naked   = ellipse_points( rmax = rmax, rmin = rmin)
    c_points_naked   = circle_angles( 0, 180, 180, convert_to_radians = True)
    e_points_ajusted = [ [center[0]+e_x*rmax, center[1]+e_y*rmax] for e_x, e_y in e_points_naked ]
    c_points_ajusted = [ [center[0]+c_x*rmax, center[1]+c_y*rmax] for c_x, c_y in c_points_naked ]
    draw_polyline( parent = parent, id = id  , points = e_points_ajusted, closed = True , thickness = thickness ) 
    draw_polyline( parent = parent, id = id+1, points = c_points_ajusted, closed = False, thickness = thickness )
    
def draw_ecliptica( parent : Union[int, str], id : Union[int, str], center : list , angle_sunrise : float, angle_culminant : float , radius : Union[float, int], draw_sun : bool = False, complete : bool = False, some_z : float = 0      ):
    culminant   = 90-angle_culminant
    sunrise     = angle_sunrise

    if   sunrise <= 90 : range_arc = (90-sunrise)*2
    elif sunrise >= 270: range_arc = 180+(360-sunrise)*2 
    else               : range_arc = 180 

    if complete:  c_angles = circle_angles( 0          , 360      , 100, convert_to_radians = True ) 
    else:         c_angles = circle_angles( 180, 180, 100, convert_to_radians = True ) 

    c_rotated = rotate_x( c_angles, culminant, True, True )
    #c_rotated = rotate_y( c_rotated, sunrise, True, True )
    c_rotated = rotate_z( c_rotated, some_z, True, True )

    c_points_ajusted = [[center[0]+c_x*radius, center[1]+c_y*radius] for c_x, c_y in c_rotated  ]
    if complete:    draw_polyline( parent = parent, id = id, points = c_points_ajusted, closed=True , color = [255,223,0,255] )
    else:           draw_polyline( parent = parent, id = id, points = c_points_ajusted, closed=False, color = [255,223,0,255] )

def init_posicaoDoSol( windows : dict ):
    with window( label = 'Posição do Sol', id = 3_1_0, no_move  = True, no_resize = True, no_collapse = True, no_close = True, no_title_bar= True ) as Posicao_sol_PS:
        windows["Posicao do sol"].append( Posicao_sol_PS )
        
        w, h   = get_item_width( Posicao_sol_PS ), get_item_height( Posicao_sol_PS)
        center = [ w*0.35, h*0.75 ] 
        radius = 500 
        
        add_drawlist( id = 3_1_1_0, width = w*0.9, height = h*0.9, pos = [w*0.025, h*0.025] )
        draw_solar_sphere( 3_1_1_0, 3_1_1_1, center, radius, radius/5, thickness = 20 )
        draw_ecliptica   ( 3_1_1_0, 3_1_1_3, center, 178   , 42      , radius         )
        draw_circle( parent= 3_1_1_0, id = 3_1_1_4, radius = radius/10, center=[100,100], color=[255,220,0,255], fill=[255,230,5,255] )
        
        track_image = add_image_loaded( IMG )
        draw_image( track_image, (0,0),(1,1), id = 'track_image', )

        draw_text  (parent = 3_1_1_0, id = 3_1_1_5, text=str(get_value(MG_Angle)), pos= [w*0.8, h*0.1], size=15)
        draw_text  (parent = 3_1_1_0, id = 3_1_1_6, text=str(get_value(ME_Angle)), pos= [w*0.8, h*0.2], size=15)

def resize_posicaoDoSol():
    global center
    global radius 

    w0, h0     =  get_item_width( 1_0 ), get_item_height( 1_0 ) 
    rmax, rmin =  w0*0.34, h0*0.12 
    center     = [w0*0.375, h0*0.75 - rmin] 
    radius     =  rmax

    configure_item( 3_1_0  , width = w0-15 , height = h0 -35, pos = [ 10, 25]            )
    configure_item( 3_1_1_0, width = w0*0.9, height = h0*0.9, pos = [w0*0.025, h0*0.025] )

    sunrise = 360-( get_value(sunrise_azi) + 270)
    if sunrise < 0 : sunrise += 360 
    culminant = get_value( culminant_alt )

    e_points_naked   = ellipse_points( rmax = rmax, rmin = rmin)
    c_points_naked   = circle_angles( 180, 180, 180, convert_to_radians = True)
    e_points_ajusted = [ [center[0]+e_x*rmax, center[1]+e_y*rmax] for e_x, e_y in e_points_naked ]
    c_points_ajusted = [ [center[0]+c_x*rmax, center[1]+c_y*rmax] for c_x, c_y in c_points_naked ]
    
    configure_item( 3_1_1_1, points = e_points_ajusted, thickness = 20  ) 
    configure_item( 3_1_1_2, points = c_points_ajusted, thickness = 20  )

    delete_item   ( 3_1_1_3 )
    draw_ecliptica( 3_1_1_0, 3_1_1_3, center , sunrise, culminant , radius, draw_sun = True )

    configure_item( 'track_image', pmin = [center[0]-w0*0.08, center[1]-h0*0.2], pmax =  [center[0]+w0*0.12, center[1]])
    configure_item( 3_1_1_5, text = str(sunrise)  , pos = [w0*0.8, h0*0.1] )
    configure_item( 3_1_1_6, text = str(culminant), pos = [w0*0.8, h0*0.2] )
    
def render_posicaoDoSol():
    global center
    global radius  

    AZI_Angle = 90 - get_value(MG_Angle)
    if AZI_Angle < 0 : AZI_Angle = 360 + AZI_Angle
    ALT_Angle = get_value(ME_Angle)

    if   sunrise <= 90 : range_arc = (90-sunrise)*2
    elif sunrise >= 270: range_arc = 180+(360-sunrise)*2
    else               : range_arc = 180

    AZI_Angle = AZI_Angle*(AZI_Angle/range_arc)
    culminant = get_value( culminant_alt )

    sun_pos = array( [[math.cos(AZI_Angle), math.sin(AZI_Angle), 1]] )
    sun_pos = rotate_x(sun_pos, culminant, False, False)[0]

    configure_item( 3_1_1_4, radius = (radius/15), center = [center[0]-radius*math.cos(AZI_Angle), center[1]-radius*math.sin(AZI_Angle)] )

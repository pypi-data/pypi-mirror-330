def get_excelcolumn_letter(column_int):
    start_index = 0   #  it can start either at 0 or at 1
    letter = ''
    while column_int > 25 + start_index:   
        letter += chr(65 + int((column_int-start_index)/26) - 1)
        column_int = column_int - (int((column_int-start_index)/26))*26
    letter += chr(65 - start_index + (int(column_int)))
    return letter


def write_inputs(ws, sensor_loc):
    ws.write(0, 0, 'Is sensor Space Based?')
    if sensor_loc == 'space':
        ws.write(0, 1, 'Yes')
    else:
        ws.write(0, 1, 'No')
    ws.write(0, 3, 'Phase Angle (Deg)')
    ws.write(0, 4, 0)
    
    ws.write(1, 3, 'Elevation Angle (Deg)')
    ws.write(1, 4, 90)
    
    ws.write(0, 6, 'Object Reflectivity (0-1)')
    ws.write(0, 7, 0.1)
    
    ws.write(1, 6, 'k (for extinction factor calc)')
    ws.write(1, 7, 0.116)
    
    ws.write(0, 9, 'X (Air Mass)')
    ws.write_formula('K1', '=(1-0.96*COS(E2*PI()/180)^2)^(-0.5)')
    
    ws.write(1, 9, 'Extinction Factor')
    ws.write_formula('K2', '= IF(B1 = "Yes", 1, 10^(-0.4*H2*(K1-1)))')
    
    ws.write(2, 0, 'Range (km)')
    ws.write(2, 1, 1000)
    
    return ws

def add_fps_sheet_func(payload_name, wb, name, ws, df, start_row, stop_row):
    ws.write(4, 2, 'Refraction Factor')
    ws.write_array_formula('C'+str(start_row)+':C'+str(stop_row), '{= 10^(-(B'+str(start_row)+':B'+str(stop_row)+'+26.74)/2.5)/K2}')
    ws.write(4, 3, 'Object Size (cm)')
    ws.write_array_formula('D'+str(start_row)+':D'+str(stop_row), '{= 2*100000*SQRT(3*PI()*B3^2*C'+str(start_row)+':C'+str(stop_row)+'/(2*(H1)*(SIN(E1*PI()/180)+(PI()-E1*PI()/180)*COS(E1*PI()/180))))}')

    chart = wb.add_chart({'type': 'scatter', 'subtype': 'smooth'})
    chart.add_series({
    'name': [name, start_row-2, 1],
    'categories': [name, start_row-1, 0, stop_row-1, 0],
    'values': [name, start_row-1, 1, stop_row-1, 1],
    })
    
    chart.set_title ({'name': 'Sensitivity Plot for ' + payload_name + ' at ' + name})
    chart.set_x_axis({'name': 'Angular Velocity (deg/sec)'})
    chart.set_y_axis({'name': 'Limiting Magnitude', 'min': int(df['Limiting Magnitude'][len(df)- 1])})
    ws.insert_chart('F10', chart)
    return ws

def add_survey_sheet_func(payload_name, name, wb, ws, df, start_row, stop_row):
    n_cols = len(df.columns)
    letter1 = get_excelcolumn_letter(n_cols)
    letter2 = get_excelcolumn_letter(n_cols+1)
    ws.write(4, n_cols, 'Refraction Factor')
    ws.write(4, n_cols+1, 'Object Size (cm)')
    for i in range(len(df)):
        ws.write_array_formula(letter1+str(start_row + i), '{= 10^(-(B'+str(start_row + i)+'+26.74)/2.5)/$K$2}')
        ws.write_array_formula(letter2+str(start_row + i), '{= 2*100000*SQRT(3*PI()*$B$3^2*'+letter1+str(start_row + i)+'/(2*($H$1)*(SIN($E$1*PI()/180)+(PI()-$E$1*PI()/180)*COS($E$1*PI()/180))))}')
    
    chart = wb.add_chart({'type': 'scatter', 'subtype': 'smooth'})
    for i in range(n_cols - 3):
        chart.add_series({
        'name': [name, start_row-2, i+1],
        'categories': [name, start_row-1, 0, stop_row-1, 0],
        'values': [name, start_row-1, i+1, stop_row-1, i+1],
        })
    
    chart.set_title ({'name': 'Sensitivity Plot for ' + payload_name })
    chart.set_x_axis({'name': 'Integration Time (seconds)', 'log_base': 10, 'major_tick_mark': 'inside',
                  'minor_tick_mark': 'inside'})
    chart.set_y_axis({'name': 'Limiting Magnitude'})
    ws.insert_chart('L10', chart)
    
    return ws

def add_obj_size_plot(payload_name, name, wb, ws, df, start_row, stop_row):
    chart = wb.add_chart({'type': 'scatter', 'subtype': 'smooth'})
    for i in range(2):
        chart.add_series({
        'name': [name, start_row-2, i+1],
        'categories': [name, start_row-1, 0, stop_row-1, 0],
        'values': [name, start_row-1, i+1, stop_row-1, i+1],
        })
    
    chart.set_title ({'name': 'Detecable Object Sizes for ' + payload_name })
    chart.set_x_axis({'name': 'Ranges (km)', 'min': df['Ranges (km)'][0], 'max': df['Ranges (km)'][len(df)- 1], 'log_base': 10, 'crossing': 0.1, 'major_tick_mark': 'inside',
                  'minor_tick_mark': 'inside'})
    chart.set_y_axis({'name': 'Object Size (m)', 'log_base': 10, 'major_tick_mark': 'inside',
                  'minor_tick_mark': 'inside'})
    ws.insert_chart('H10', chart)
    
    

def write_to_excel( payload, wb, writer, df, func):
    if func == 'fps':
        sheet = 'FPS_' + str(payload.fps)
    elif func == 'survey':
        sheet = 'Survey'
    elif func == 'obj_sizes':
        sheet = 'obj_sizes'
    
    if func!= 'obj_sizes':    
        start_row = 6
        stop_row = len(df)+start_row-1
    
        df.to_excel(writer, sheet_name = sheet, startrow = start_row-2,  index = False)
        ws = writer.sheets[sheet]
    
        ws = write_inputs(ws, payload.sensor_loc)
    else:
        df.to_excel(writer, sheet_name = sheet,  index = False)
        ws = writer.sheets[sheet]
        ws = add_obj_size_plot(payload.name, sheet, wb, ws, df, 2, len(df+2-1))
    
    if func == 'fps':
        ws = add_fps_sheet_func(payload.name, wb, sheet, ws, df, start_row, stop_row)
    elif func == 'survey':
        ws = add_survey_sheet_func(payload.name, sheet, wb, ws, df, start_row, stop_row)
        
    
    
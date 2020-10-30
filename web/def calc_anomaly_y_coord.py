def calc_anomaly_y_coord(clock_pos, pipe_od, false_northing, clock_offset, y_axis_clock):
    print(pipe_od)
	clock_parts = clock_pos.split(':')
    clock_hours = float(clock_parts[0])
    clock_minutes = float(clock_parts[1])
    pipe_od = float(pipe_od)
    offset_parts = clock_offset.split(':')
    offset_hours = float(offset_parts[0])
    offset_minutes = float(offset_parts[1])

    # Correct clock minutes for the clock minutes offset
    if offset_hours < 0:
        offset_minutes = offset_minutes * (-1)
    clock_minutes = clock_minutes + offset_minutes
    if clock_minutes > 59:
        clock_minutes = clock_minutes - 60
        clock_hours = clock_hours + 1
    elif clock_minutes < 0:
        clock_minutes = clock_minutes + 60
        clock_hours = clock_hours - 1

    # Correct clock hours for the clock hours offset
    clock_hours = clock_hours + offset_hours
    if clock_hours > 12:
        clock_hours = clock_hours - 12
    elif clock_hours < 0:
        clock_hours = clock_hours + 12

    # Calculate y-coordinate
    if y_axis_clock == "6:00 Centered":
        if clock_hours == 12:
            y_coord = ((clock_minutes / 60 / 12) * (pipe_od / 12 * math.pi)) + false_northing
        else:
            y_coord = (((clock_hours / 12) + (clock_minutes / 60 / 12)) * (pipe_od / 12 * math.pi)) + false_northing
    else:  # y_axis_clock = "12:00 Centered"
        if clock_hours == 12:
            y_coord = (-1) * (((clock_minutes / 60 / 12) * (pipe_od / 12 * math.pi)) + false_northing)
        elif 1 <= clock_hours < 6:
            y_coord = (-1) * ((((clock_hours / 12) + (clock_minutes / 60 / 12)) * (pipe_od / 12 * math.pi)) + false_northing)
        else:  # 6 <= clock_hours <= 11
            y_coord = ((1 - ((clock_hours / 12) + (clock_minutes / 60 / 12))) * (pipe_od / 12 * math.pi)) + false_northing
    return y_coord

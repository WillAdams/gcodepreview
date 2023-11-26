//!OpenSCAD

/**
 * @param options [any] 
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 * @param tr [number] 
 * @param stepover [number] 
 * @param clearperimeter [boolean] 
 */
module cut_rectangle(options, bx, by, bz, ex, ey, ez, tr, stepover, clearperimeter) {
    if (("horizontal" == options)) {
        cut_rectangle_horizontal(bx = bx, by = by, bz = bz, ex = ex, ey = ey, ez = ez, tr = tr, stepover = stepover);
    }
    
    if (("vertical" == options)) {
        cut_rectangle_vertical(bx = bx, by = by, bz = bz, ex = ex, ey = ey, ez = ez, tr = tr, stepover = stepover);
    }
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 * @param tr [number] 
 * @param stepover [number] 
 */
module cut_rectangle_horizontal(bx, by, bz, ex, ey, ez, tr, stepover) {
    begintoolpath(bx = bx, by = by, bz = (bz + tr));
    beginpolyline(bx = bx, by = by, bz = (bz + tr));
    rapid(ex = bx, ey = by, ez = (bz + tr));
    cutoneaxis_setfeed(axis = "Z", depth = (tr * -1), feed = plunge);
    * cutwithfeed(ex = bx, ey = by, ez = ez, feed = feed);
    for(var0__gHM5AYfLL0mqB8lH9bnxng = [0:2:(round(number = (((ey - by) / tr) / 2)) * 2)]) {
        cut(ex = bx, ey = (by + (((ey - by) / (round(number = (((ey - by) / tr) / 2)) * 2)) * var0__gHM5AYfLL0mqB8lH9bnxng)), ez = ez);
        addpolyline(bx = bx, by = (by + (((ey - by) / (round(number = (((ey - by) / tr) / 2)) * 2)) * var0__gHM5AYfLL0mqB8lH9bnxng)), bz = ez);
        cut(ex = ex, ey = (by + (((ey - by) / (round(number = (((ey - by) / tr) / 2)) * 2)) * var0__gHM5AYfLL0mqB8lH9bnxng)), ez = ez);
        addpolyline(bx = ex, by = (by + (((ey - by) / (round(number = (((ey - by) / tr) / 2)) * 2)) * var0__gHM5AYfLL0mqB8lH9bnxng)), bz = ez);
        if ((var0__gHM5AYfLL0mqB8lH9bnxng <= ((round(number = (((ey - by) / tr) / 2)) * 2) - 1))) {
            # cut(ex = ex, ey = ((by + (((ey - by) / (round(number = (((ey - by) / tr) / 2)) * 2)) * var0__gHM5AYfLL0mqB8lH9bnxng)) + ((ey - by) / (round(number = (((ey - by) / tr) / 2)) * 2))), ez = ez);
            addpolyline(bx = ex, by = ((by + (((ey - by) / (round(number = (((ey - by) / tr) / 2)) * 2)) * var0__gHM5AYfLL0mqB8lH9bnxng)) + ((ey - by) / (round(number = (((ey - by) / tr) / 2)) * 2))), bz = ez);
            cut(ex = bx, ey = ((by + (((ey - by) / (round(number = (((ey - by) / tr) / 2)) * 2)) * var0__gHM5AYfLL0mqB8lH9bnxng)) + ((ey - by) / (round(number = (((ey - by) / tr) / 2)) * 2))), ez = ez);
            addpolyline(bx = bx, by = ((by + (((ey - by) / (round(number = (((ey - by) / tr) / 2)) * 2)) * var0__gHM5AYfLL0mqB8lH9bnxng)) + ((ey - by) / (round(number = (((ey - by) / tr) / 2)) * 2))), bz = ez);
        }
    }
    
    * cut(ex = ex, ey = ey, ez = ez);
    * addpolyline(bx = ex, by = ey, bz = ez);
    closepolyline();
    movetosafez();
}

/**
 * @param bx [number] 
 * @param by [number] 
 * @param bz [number] 
 * @param ex [number] 
 * @param ey [number] 
 * @param ez [number] 
 * @param tr [number] 
 * @param stepover [number] 
 */
module cut_rectangle_vertical(bx, by, bz, ex, ey, ez, tr, stepover) {
    begintoolpath(bx = bx, by = by, bz = (bz + tr));
    beginpolyline(bx = bx, by = by, bz = (bz + tr));
    rapid(ex = bx, ey = by, ez = (bz + tr));
    echo(((ex - bx) / (round(number = (((ex - bx) / tr) / 2)) * 2)));
    cutoneaxis_setfeed(axis = "Z", depth = (tr * -1), feed = plunge);
    * cutwithfeed(ex = bx, ey = by, ez = ez, feed = feed);
    for(var0__OBbMr8RmlkzxwtrSNySTA = [0:2:(round(number = (((ex - bx) / tr) / 2)) * 2)]) {
        cut(ex = (bx + (((ex - bx) / (round(number = (((ex - bx) / tr) / 2)) * 2)) * var0__OBbMr8RmlkzxwtrSNySTA)), ey = by, ez = ez);
        addpolyline(bx = (bx + (((ex - bx) / (round(number = (((ex - bx) / tr) / 2)) * 2)) * var0__OBbMr8RmlkzxwtrSNySTA)), by = by, bz = ez);
        cut(ex = (bx + (((ex - bx) / (round(number = (((ex - bx) / tr) / 2)) * 2)) * var0__OBbMr8RmlkzxwtrSNySTA)), ey = ey, ez = ez);
        addpolyline(bx = (bx + (((ex - bx) / (round(number = (((ex - bx) / tr) / 2)) * 2)) * var0__OBbMr8RmlkzxwtrSNySTA)), by = ey, bz = ez);
        if ((var0__OBbMr8RmlkzxwtrSNySTA <= ((round(number = (((ex - bx) / tr) / 2)) * 2) - 1))) {
            cut(ex = ((bx + (((ex - bx) / (round(number = (((ex - bx) / tr) / 2)) * 2)) * var0__OBbMr8RmlkzxwtrSNySTA)) + ((ex - bx) / (round(number = (((ex - bx) / tr) / 2)) * 2))), ey = ey, ez = ez);
            addpolyline(bx = ((bx + (((ex - bx) / (round(number = (((ex - bx) / tr) / 2)) * 2)) * var0__OBbMr8RmlkzxwtrSNySTA)) + ((ex - bx) / (round(number = (((ex - bx) / tr) / 2)) * 2))), by = ey, bz = ez);
            cut(ex = ((bx + (((ex - bx) / (round(number = (((ex - bx) / tr) / 2)) * 2)) * var0__OBbMr8RmlkzxwtrSNySTA)) + ((ex - bx) / (round(number = (((ex - bx) / tr) / 2)) * 2))), ey = by, ez = ez);
            addpolyline(bx = ((bx + (((ex - bx) / (round(number = (((ex - bx) / tr) / 2)) * 2)) * var0__OBbMr8RmlkzxwtrSNySTA)) + ((ex - bx) / (round(number = (((ex - bx) / tr) / 2)) * 2))), by = by, bz = ez);
        }
    }
    
    * cut(ex = ex, ey = ey, ez = ez);
    * addpolyline(bx = ex, by = ey, bz = ez);
    closepolyline();
    movetosafez();
}

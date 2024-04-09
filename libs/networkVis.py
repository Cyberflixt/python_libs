
import math, time
import tkinter as tk


def perpendicular_vec(x,y):
    """Returns the 2d perpendicular vector"""
    return y, -x

class Window:
    def __init__(self, network):
        """Create a new window given the graph"""
        self.net = network

        self.dark_mode = False
        self.default_palette()
        
        self.always_refresh = True
        self.run = False

        self.layout = 0
        self.node_distance = 1

        self.font = 'Arial'
        self.font_scale = .1
        self.node_scale = .07

        self.mx = 0
        self.my = 0

    def default_palette(self, dark = True):
        if dark:
            self.palette = (
                '#202830', # bg
                '#ffffff', # text
                '#7800BD', # node
            )
        else:
            self.palette = (
                '#ffffff', # bg
                '#000000', # text
                '#7EBCBD', # node
            )

    def get_highest_weight(self):
        s = self.net.size()
        r = 0
        for y in range(s):
            for x in range(s):
                weight = self.net.matrix[y][x]
                if weight > r:
                    r = weight
        return r

    def show(self, network = None, timeout = None):
        """Display a given network"""
        if network:
            self.net = network
            self.pos = None
        if timeout:
            self.timeout = time.time()+timeout
        else:
            self.timeout = None
        self.max_weight = self.get_highest_weight()
        self.open()

    def open(self):
        """Open rendering window"""

        # new root
        self.root = tk.Tk()
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        fac = .8

        self.root.geometry(f'{int(w*fac)}x{int(h*fac)}')
        self.root.title('Network')
        self.root.focus_set()
        self.root.protocol("WM_DELETE_WINDOW", self.close_event)

        # canvas
        self.canvas = tk.Canvas(self.root, bg = self.palette[0], highlightthickness = 0)
        self.canvas.pack(fill = tk.BOTH, expand = True)

        # events
        self.root.bind("<Configure>", self.on_window_resize)
        self.root.bind('<Motion>', self.on_motion)

        self.loop()

    def loop(self):
        self.run = True
        while self.run:
            self.root.update_idletasks()
            self.root.update()
            if self.always_refresh:
                self.refresh()
            if self.timeout:
                if time.time() > self.timeout:
                    self.run = False
        if self.root:
            self.root.destroy()

    def close_event(self):
        self.run = False
    
    def min_size(self, elem = None):
        """Minimum size of both elements axis"""
        
        if elem == None:
            return self.vh if self.vh<self.vw else self.vw
        
        w = elem.winfo_width()
        h = elem.winfo_height()
        return h if h<w else w
    
    def create_circle(self, canvas, x,y, r, fill = None):
        """Creates a circle of given x,y, radius and color"""
        
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return self.canvas.create_oval(x0, y0, x1, y1,
                                  fill = fill,
                                  outline = '')

    def get_font(self, scale = 1):
        """Get font tuple relative to the window size"""
        return (
            self.font,
            int(scale * self.min_size() * self.font_scale /2),
            'bold'
        )

    def draw_node(self, x,y, color = None, text = None, fontscale = 7):
        """Draws a node at x,y (px); optionnal: color, text, font_scale"""
        if not color:
            color = self.palette[1]
            
        size = self.min_size() * self.node_scale
        self.create_circle(self.canvas, x,y, size, color)
            
        if text:
            self.canvas.create_text(
                x,y, text=text,
                anchor  = 'center',
                justify = 'center',
                fill = self.palette[1],
                font = self.get_font(fontscale * self.node_scale),
            )

    def layout_circle(self):
        """Returns the nodes layout in a circular arrangement"""
        
        res = []
        
        li = self.net.nodes
        ma = len(li)
        for i in range(ma):
            v = li[i]
            weight = 0
            if isinstance(v, list) or isinstance(v, tuple):
                name = v[0]
                if len(v)>1:
                    weight = v[1]
            else:
                name = v

            angle = i/ma * math.pi*2 # radians
            rad = .3
            x = math.cos(angle)*rad + .5
            y = math.sin(angle)*rad + .5
            
            res.append((x, y, name, weight))
        return res

    def calc_tension(self, x,y, res, layout, ix,iy, b):
        """Compute a tension between two nodes by the weight of their connection"""
        # Settings
        speed = .05
        length = .6 * self.node_distance

        weight = self.net.matrix[iy][ix]
        if weight == 0:
            return
        
        weight *= length / self.max_weight

        o = layout[b]
        vx = o[0]-x
        vy = o[1]-y
        
        mag = math.sqrt(vx*vx + vy*vy)
        if mag<.0001:
            mag = .0001

        tension = mag-weight
        sign = 1 if tension > 0 else -1
        tension = tension**2 * sign * speed
        res[0] += vx*tension
        res[1] += vy*tension

        # clamping
        if res[0] < 0:
            res[0] = 0
        if res[1] < 0:
            res[1] = 0
        if res[0] > 1:
            res[0] = 1
        if res[1] > 1:
            res[1] = 1
            


    def layout_tension_step(self, layout):
        """Returns the nodes layout solved by tension"""

        res = []
        
        ma = len(layout)
        for i in range(ma):
            x,y, name, weight = layout[i]
            pos = [x,y]
            
            # row
            for ix in range(ma):
                if ix!=i:
                    self.calc_tension(x,y, pos, layout, ix,i, ix)
            # column
            for iy in range(ma):
                if iy!=i:
                    self.calc_tension(x,y, pos, layout, i,iy, iy)
            
            res.append((*pos, name, weight))
        return res
        

    def draw_layout_node(self, node):
        """Draws the nodes with a given layout result"""
        x,y, name, weight = node
        
        px = x*self.vw
        py = y*self.vh
            
        text = f'{name}\n{weight}'
        color = self.palette[2]
            
        self.draw_node(px, py, color, text)

    def draw_nodes(self, layout):
        """Draws the nodes of the given layout onto the canvas"""
        
        for node in layout:
            self.draw_layout_node(node)

    def text_outline(self, x,y, outline=2, **kwargs):
        """Draws a text with an outline in pixels"""
        bg_color = self.palette[0]
        
        fill = kwargs['fill']
        kwargs['fill'] = bg_color

        self.canvas.create_text(x+outline, y+outline, **kwargs)
        self.canvas.create_text(x-outline, y+outline, **kwargs)
        self.canvas.create_text(x-outline, y-outline, **kwargs)
        self.canvas.create_text(x+outline, y-outline, **kwargs)

        kwargs['fill'] = fill
        self.canvas.create_text(x, y, **kwargs)
        
    def draw_edge(self, ax,ay, bx,by, weight, i=0, fontscale=.5):
        """Draw an arrow between two relative coords, optionnal overlap int and font scale"""
        mi = self.min_size()

        # settings
        shrink = self.node_scale * mi
        dir_offset = .03 * mi # label directional offset
        outline = 3 # label outline (px)

        # to screen space
        basex = ax*self.vw
        basey = ay*self.vh
        tarx = bx*self.vw
        tary = by*self.vh

        # arrow vector
        vx = tarx-basex
        vy = tary-basey
        mag = math.sqrt(vx*vx + vy*vy)
        if mag<.0001:
            mag = .0001

        # unit vector
        vdx = vx/mag
        vdy = vy/mag
        shrink_vx = vdx*shrink
        shrink_vy = vdy*shrink

        # side offset
        
        if i!=0:
            side = (i+1)//2 * (i%2*2-1) * 10
            rx, ry = perpendicular_vec(vdx, vdy)
            ox = rx * side
            oy = ry * side
        else:
            ox = 0
            oy = 0

        # draw arrow
        self.canvas.create_line(
            basex + shrink_vx + ox,
            basey + shrink_vy + oy,
            tarx  - shrink_vx + ox,
            tary  - shrink_vy + oy,
            width = 2,
            fill  = self.palette[1],
            arrow = tk.LAST
        )

        # draw edge weight label
        self.text_outline(
            (basex+tarx)/2 + vdx*dir_offset + ox,
            (basey+tary)/2 + vdy*dir_offset + oy,
            outline,
            
            text = weight,
            anchor  = 'center',
            justify = 'center',
            fill = self.palette[1],
            font = self.get_font(fontscale),
        )

    def draw_arc(self, cx,cy, radius, start_rad=0, end_rad=math.pi*2):
        samples = 50
        ox = None
        oy = None
        for i in range(samples+1):
            alpha = i/samples
            angle = start_rad + (end_rad - start_rad) * alpha

            x = cx + math.cos(angle)*radius
            y = cy + math.sin(angle)*radius
            
            if i!=0:
                self.canvas.create_line(
                    ox,oy, x,y,
                    width = 2,
                    capstyle = 'round',
                    fill = self.palette[1],
                    arrow = tk.LAST if i == samples else None
                )

            ox = x
            oy = y

    def draw_self_edge(self, x,y, weight, fontscale = .5):
        outline = 3
        node_size = self.min_size() * self.node_scale
        
        off = node_size
        radius = off

        ox = x*self.vw-off
        oy = y*self.vh
        angle_a = math.pi/3
        angle_b = math.pi*2-angle_a
        
        self.draw_arc(ox, oy, radius, angle_a, angle_b)

        
        # draw edge weight label
        self.text_outline(
            ox-radius, oy,
            outline,
            
            text = weight,
            anchor  = 'center',
            justify = 'center',
            fill = self.palette[1],
            font = self.get_font(fontscale),
        )

    def draw_edges(self, layout, sel_node = None):
        """Draws all edges or only those connected to the given node"""
        
        li_repeat = {}
        size = self.net.size()
        for y in range(size):
                
            ax = layout[y][0]
            ay = layout[y][1]
            for x in range(size):
                weight = self.net.matrix[y][x]
                if weight != 0:

                    # increment repeat int
                    k = y*size+x if y>x else x*size+y
                    rint = 0
                    if k in li_repeat:
                        rint = li_repeat[k]
                    li_repeat[k] = rint+1

                    # skip if in selected view
                    if sel_node != None:
                        if sel_node != y:
                            continue

                    if x == y:
                        self.draw_self_edge(ax,ay, weight)
                    else:
                        bx = layout[x][0]
                        by = layout[x][1]
                    
                        self.draw_edge(ax,ay, bx,by, weight, rint)

    def get_hovered_node(self, layout):
        """Returns the index of the hovered node or None"""
        threshold = self.node_scale * self.min_size()
        
        best_mag = threshold+1
        best_i = 0
        for i in range(len(layout)):
            elem = layout[i]
            mag = math.sqrt((elem[0]*self.vw-self.mx)**2 + (elem[1]*self.vh-self.my)**2)
            if mag < best_mag:
                best_mag = mag
                best_i = i

        if best_mag < threshold:
            return best_i

    def refresh(self):
        """Refresh the canvas entirely"""
        
        self.canvas.delete('all')

        layout = None
        if self.layout==0:
            # circle
            layout = self.layout_circle()
        else:
            # tension
            if self.pos == None:
                self.pos = self.layout_circle()
            layout = self.layout_tension_step(self.pos)
        self.pos = layout

        self.draw_nodes(layout)
        self.draw_edges(layout)
        
        i = self.get_hovered_node(layout)
        if i!=None:
            self.fill_dim()
            self.draw_layout_node(layout[i])
            self.draw_edges(layout, i)
        
    def fill_dim(self):
        """Dim out the current render (alpha 25%)"""
        
        self.canvas.create_rectangle(
            0, 0, self.vw, self.vh, fill = self.palette[0],
            stipple = 'gray75', outline = '')

    def on_window_resize(self, e):
        """Method called when the window is resized"""
        
        self.vw = self.root.winfo_width()
        self.vh = self.root.winfo_height()
        self.refresh()

    def on_motion(self, e):
        """Method called when the mouse is moved"""
        
        self.mx = e.x
        self.my = e.y
        self.refresh()

        
        
        

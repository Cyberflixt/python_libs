
import math, time
import tkinter as tk


def perpendicular_vec(x,y):
    """Returns the 2d perpendicular vector"""
    return y, -x

class Window:
    def __init__(self, network):
        """Create a new window given the graph"""
        self.net = network

        # Settings
        self.always_refresh = True
        self.dark_mode = False
        self.layout = 0
        self.tension_force = 20
        self.tension_exponent = 1
        self.tension_distance = 1
        self.tension_distance_min = .15
        self.tension_safe_zone = .1
        
        self.font = 'Arial'
        self.font_scale = .1
        self.node_scale = .07
        self.edge_label_scale = .5
        self.edge_label_outline = 3
        

        # Defaults
        self.default_palette()
        
        self.run = False
        self.update = True
        self.drag_node = None

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

        # new network value
        if network:
            self.net = network
            self.pos = None
            self.update = True

        # timout?
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
        self.root.bind("<ButtonPress-1>", self.on_mouse_down)
        self.root.bind("<ButtonRelease-1>", self.on_mouse_up)

        self.loop()

    def loop(self):
        self.run = True
        
        while self.run:
            self.root.update_idletasks()
            self.root.update()

            # dragged node
            if self.drag_node != None:
                self.drag_node[0] = (self.mx + self.drag_dx) / self.vw
                self.drag_node[1] = (self.my + self.drag_dy) / self.vh

                # refresh viewport if not by default
                if not self.always_refresh:
                    self.refresh()

            # refresh viewport
            if self.always_refresh:
                self.refresh()

            # window timed out?
            if self.timeout:
                if time.time() > self.timeout:
                    self.run = False

        # end
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
    
    def create_circle(self, canvas, x,y, r, fill):
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

    def draw_node(self, x,y, text = None, color = None, fontscale = None):
        """Draws a node at x,y (px); optionnal: color, text, font_scale"""
        if not color:
            color = self.palette[1]
        if not fontscale:
            fontscale = 7
            
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
            
            res.append([x, y, name, weight])
        return res

    def calc_tension(self, x,y, res, layout, ix,iy, b):
        """Compute a tension between two nodes by the weight of their connection"""
        # Settings
        speed = .01 * self.tension_force
        length = .6 * self.tension_distance

        weight = self.net.matrix[iy][ix]
        if weight == 0:
            return
        
        weight *= length / self.max_weight
        if weight < self.tension_distance_min:
            weight = self.tension_distance_min

        o = layout[b]
        vx = o[0]-x
        vy = o[1]-y
        
        mag = math.sqrt(vx*vx + vy*vy)
        if mag<.0001:
            mag = .0001

        tension = mag-weight
        sign = 1 if tension > 0 else -1
        tension = abs(tension**self.tension_exponent) * sign * speed
        res[0] += vx*tension
        res[1] += vy*tension

        # clamping
        clamp = self.tension_safe_zone
        if res[0] < clamp:
            res[0] = clamp
        if res[1] < clamp:
            res[1] = clamp
        if res[0] > 1-clamp:
            res[0] = 1-clamp
        if res[1] > 1-clamp:
            res[1] = 1-clamp
            


    def layout_tension_step(self, layout):
        """Affect the nodes layout solved by tension"""

        # Cloning to avoid movement between calculations
        new = []
        
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
            
            new.append(pos)

        for i in range(ma):
            pos = new[i]
            node = layout[i]
            
            node[0] = pos[0]
            node[1] = pos[1]
        
        return layout
        

    def draw_layout_node(self, node):
        """Draws the nodes with a given layout result"""
        x,y, name, weight = node
        
        px = x*self.vw
        py = y*self.vh
            
        text = f'{name}\n{weight}'
        color = self.palette[2]
            
        self.draw_node(px, py, text, color, None)

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
        
    def draw_edge(self, ax,ay, bx,by, weight, i=0):
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

        label_x = (basex+tarx)/2 + vdx*dir_offset + ox
        label_y = (basey+tary)/2 + vdy*dir_offset + oy

        return label_x, label_y

    def draw_arc(self, cx,cy, radius, start_rad=0, end_rad=math.pi*2):
        """Draw a circular arc at x,y with a given radius, with a start and end angle (radians)"""
        
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

    def draw_self_edge(self, x,y, weight):
        outline = 3
        node_size = self.min_size() * self.node_scale
        
        off = node_size
        radius = off

        ox = x*self.vw-off
        oy = y*self.vh
        angle_a = math.pi/3
        angle_b = math.pi*2-angle_a
        
        self.draw_arc(ox, oy, radius, angle_a, angle_b)

        return ox-radius, oy

    def draw_edges(self, layout, sel_node = None):
        """Draws all edges or only those connected to the given node"""
        
        li_repeat = {}
        size = self.net.size()
        labels = []
        
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
                        lx,ly = self.draw_self_edge(ax,ay, weight)
                    else:
                        bx = layout[x][0]
                        by = layout[x][1]
                        
                        lx,ly = self.draw_edge(ax,ay, bx,by, weight, rint)
                    labels.append((lx, ly, weight))

        # draw edges weight labels
        for x,y, text in labels:
            self.text_outline(
                x, y, self.edge_label_outline,
                
                text = text,
                anchor  = 'center',
                justify = 'center',
                fill = self.palette[1],
                font = self.get_font(self.edge_label_scale),
            )

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
        
        if self.layout==0:
            # circle
            if self.pos == None:
                self.pos = self.layout_circle()
        else:
            # tension
            if self.pos == None:
                self.pos = self.layout_circle()
            self.layout_tension_step(self.pos)

        # get selected node
        self.sel_node = None
        if self.drag_node:
            if self.drag_node in self.pos:
                self.sel_node = self.pos.index(self.drag_node)
        else:
            self.sel_node = self.get_hovered_node(self.pos)

        # render everything
        self.draw_nodes(self.pos)
        self.draw_edges(self.pos)


        """
        # draw overlay selected
        if self.sel_node != None:
            self.fill_dim()
            self.draw_layout_node(self.pos[self.sel_node])
            self.draw_edges(self.pos, self.sel_node)
        """
        
    def fill_dim(self):
        """Dim out the current render (alpha 25%)"""
        
        self.canvas.create_rectangle(
            0, 0, self.vw, self.vh, fill = self.palette[0],
            stipple = 'gray75', outline = '')

    def on_window_resize(self, e):
        """Method called when the window is resized"""
        
        self.vw = self.root.winfo_width()
        self.vh = self.root.winfo_height()

        if not self.always_refresh:
            self.refresh()

    def on_motion(self, e = None):
        """Method called when the mouse is moved"""
        if e:
            self.mx = e.x
            self.my = e.y

        if not self.always_refresh:
            self.refresh()

    def on_mouse_down(self, e):
        """LMB pressed"""
        self.lmb = True
        if self.pos:
            i = self.get_hovered_node(self.pos)
            if i != None:
                # clicked node
                node = self.pos[i]
                self.drag_node = node
                self.drag_dx = node[0]*self.vw-self.mx
                self.drag_dy = node[1]*self.vh-self.my

                self.on_motion(None)
                
        
    def on_mouse_up(self, e):
        """LMB released"""
        self.lmb = False
        self.drag_node = None

        
        
        

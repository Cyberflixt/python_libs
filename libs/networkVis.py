
import math, time
import tkinter as tk


def perpendicular_vec(x,y):
    """Returns the 2d perpendicular vector"""
    return y, -x

class Window:
    def __init__(self, network = None):
        """Creates a new window with a given graph"""
        self.net = network

        # Settings
        self.always_refresh = True
        self.sel_overlay = True
        self.dark_mode = False
        self.tension_force = 20
        self.tension_exponent = 1
        self.tension_distance = .8
        self.tension_distance_min = .15
        self.tension_safe_zone = .1
        self.tension_neutral = .01
        
        self.font = 'Arial'
        self.font_scale = .1
        self.node_scale = .05
        self.edge_label_scale = .5
        self.edge_label_outline = 3
        self.arc_samples = 50
        

        # Defaults
        self.palette = self.default_palette()
        
        self.mx = 0
        self.my = 0
        self.vh = 1080
        self.vw = 1920
        self.pos = None
        self.run = False
        self.root = None
        self.layout = 0
        self.timeout = None
        self.drag_node = None
        self.reset_layout = True

        #self.create_root()

    def default_palette(self, dark = True):
        """Get the default palette of the dark/light theme"""
        if dark:
            return (
                '#202830', # bg
                '#ffffff', # text
                '#7800BD', # node
            )
        else: # light
            return (
                '#ffffff', # bg
                '#000000', # text
                '#7EBCBD', # node
            )

    def get_highest_link_weight(self):
        """Returns the highest weight of all links"""
        s = self.net.size()
        r = 0
        for y in range(s):
            for x in range(s):
                weight = self.net.matrix[y][x]
                if weight > r:
                    r = weight
        return r

    def set_layout(self, name):
        """Sets the layout of the network window"""
        
        layouts = ('circle', 'tension')
        self.reset_layout = True
        
        i = name
        if isinstance(name, str):
            if name in layouts:
                i = layouts.index(name)
            else:
                raise ValueError(f'Layout "{name}" does not exist, see existing layouts: {layouts}')

        self.layout = i
        return i

    def update_layout_changes(self):
        """Update network changes without affecting exisiting layout"""

        # Check for deleted nodes
        dels = []
        for i in range(len(self.pos)):
            x,y,name,weight = self.pos[i]
            
            # exists?
            notfound = True
            for elem in self.net.nodes:
                if elem[0] == name and elem[1] == weight:
                    notfound = False
                    break

            if notfound:
                # deleted node
                dels.append(i)

        # delete deleted nodes
        for i in range(len(dels)):
            index = dels[i]-i
            del self.pos[index]
            
        

        # Check for new nodes
        offset = 0
        for i in range(len(self.net.nodes)):
            name, weight = self.net.nodes[i]

            # exists?
            notfound = True
            for elem in self.pos:
                if elem[2] == name and elem[3] == weight:
                    notfound = False
                    break

            if notfound:
                # added node
                x = .5
                y = .5
                self.pos.insert(i, [x,y, name, weight])
            
            
        

    def network_updated(self):
        """Check for changes"""
        self.max_link_weight = self.get_highest_link_weight()

        # layout calculated, update
        if not self.pos:
            self.layout_step(True)
        self.update_layout_changes()
            

    def set_nework(self, network):
        """New network opened, reset everything"""
        self.net = network
        self.reset_layout = True

    def create_root(self, hide = True):
        """Show rendering window"""

        # new root
        self.root = tk.Tk()
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        fac = .8

        self.root.geometry(f'{int(w*fac)}x{int(h*fac)}')
        self.root.title('Network')
        self.root.focus_set()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # canvas
        self.canvas = tk.Canvas(self.root, bg = self.palette[0], highlightthickness = 0)
        self.canvas.pack(fill = tk.BOTH, expand = True)

        # events
        self.root.bind("<Configure>", self.on_window_resize)
        self.root.bind('<Motion>', self.on_motion)
        self.root.bind("<ButtonPress-1>", self.on_mouse_down)
        self.root.bind("<ButtonRelease-1>", self.on_mouse_up)

        if hide:
            self.hide()

    def show(self, network = None, **kwargs):
        """Show rendering window"""
        
        # new network value
        if network:
            self.set_nework(network)

        # timeout?
        if 'time' in kwargs:
            self.timeout = time.time()+kwargs['time']
        else:
            self.timeout = None

        # open/create window
        if self.root:
            self.root.deiconify()
            self.on_window_resize(None)
            self.root.focus_set()
        else:
            self.create_root(False)
        
        self.network_updated()
        self.loop()

    def hide(self):
        if self.root:
            self.root.withdraw()

    def destroy(self):
        if self.root:
            self.root.destroy()
            self.root = None

    def loop(self):
        self.run = True
        self.kill_on_end = True
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
                    self.kill_on_end = False
                    
        if self.kill_on_end:
            if self.root:
                self.destroy()
    
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
    
    def calc_tension(self, pos, ax,ay, bx, by, weight):
        """Compute a tension between two nodes by the weight of their connection"""
        # Settings
        speed = .01 * self.tension_force
        length = .6 * self.tension_distance

        # Get unit vector
        vx = bx-ax
        vy = by-ay
            
        mag = math.sqrt(vx*vx + vy*vy)
        if mag<.0001:
            mag = .0001

        # Link exists?
        if weight == 0:
            # small push force
            force = speed * self.tension_neutral / len(self.pos)
            pos[0] -= vx * force
            pos[1] -= vy * force
        else:
            # tension between nodes weighted distance
            weight *= length / self.max_link_weight
            if weight < self.tension_distance_min:
                weight = self.tension_distance_min

            tension = mag-weight
            sign = 1 if tension > 0 else -1
            tension = abs(tension**self.tension_exponent) * sign * speed
            pos[0] += vx*tension
            pos[1] += vy*tension

        # clamping
        min_size = self.min_size()
        clampx = self.tension_safe_zone * min_size / self.vw
        clampy = self.tension_safe_zone * min_size / self.vh
        
        if pos[0] < clampx:
            pos[0] = clampx
        if pos[1] < clampy:
            pos[1] = clampy
        if pos[0] > 1-clampx:
            pos[0] = 1-clampx
        if pos[1] > 1-clampy:
            pos[1] = 1-clampy
    
    def layout_tension_step(self, layout):
        """Affect the nodes layout solved by tension"""

        # Cloning to avoid movement between calculations
        new = []
        
        ma = len(layout)
        for i in range(ma):
            ax,ay, name, weight = layout[i]
            pos = [ax,ay]
            
            # row
            for ix in range(ma):
                if ix!=i:
                    bx = layout[ix][0]
                    by = layout[ix][1]
                    bweight = self.net.matrix[ix][i]
                    self.calc_tension(pos, ax,ay, bx,by, bweight)
                    
            # column
            for iy in range(ma):
                if iy!=i:
                    bx = layout[iy][0]
                    by = layout[iy][1]
                    bweight = self.net.matrix[i][iy]
                    self.calc_tension(pos, ax,ay, bx,by, bweight)
                    
            
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

        if weight == 0:
            text = str(name)
        else:
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
        
    def draw_edge(self, ax,ay, bx,by, weight, i=0, arrow = True):
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

        # skip edge if its length will be negative
        if mag < shrink*2:
            return (basex+tarx)/2, (basey+tary)/2

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
            arrow = tk.LAST if arrow else None
        )

        label_x = (basex+tarx)/2 + vdx*dir_offset + ox
        label_y = (basey+tary)/2 + vdy*dir_offset + oy

        return label_x, label_y

    def draw_arc(self, cx,cy, radius, start_rad=0, end_rad=math.pi*2):
        """Draw a circular arc at x,y with a given radius, with a start and end angle (radians)"""
        
        samples = self.arc_samples
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
                weight_opp = self.net.matrix[x][y]
                if weight != 0:
                    arrow = weight_opp != weight
                    if not arrow:
                        if x<y:
                            continue

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
                        label_pos = self.draw_self_edge(ax,ay, weight)
                    else:
                        bx = layout[x][0]
                        by = layout[x][1]
                        
                        label_pos = self.draw_edge(ax,ay, bx,by, weight, rint, arrow)
                    
                    if label_pos != None:
                        labels.append((*label_pos, weight))

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
        
        return self

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

    def bake(self, steps = 2000):
        """Bake a tension layout from scratch, with a given amount of steps"""

        if self.layout == 1:
            # tension bake
            self.network_updated()
            if not self.pos:
                self.pos = self.layout_circle()
            self.reset_layout = False

            # bake tension steps
            for i in range(steps):
                self.layout_tension_step(self.pos)
            return self

    def layout_step(self, reset = True):
        """Compute first or next layout positions"""
        if self.layout==0:
            # circle
            if reset:
                self.pos = self.layout_circle()
        elif self.layout==1:
            # tension
            if reset:
                self.pos = self.layout_circle()
            self.layout_tension_step(self.pos)

    def refresh(self):
        """Refresh the canvas entirely"""

        # clear canvas
        self.canvas.delete('all')

        # refresh layout
        reset = self.reset_layout or self.pos == None
        self.reset_layout = False
        self.layout_step(reset)

        # get selected node
        self.sel_node = None
        if not self.drag_node:
            self.sel_node = self.get_hovered_node(self.pos)

        # render everything
        self.draw_nodes(self.pos)
        self.draw_edges(self.pos)


        if self.sel_overlay:
            # draw overlay selected
            if self.sel_node != None:
                self.fill_dim()
                self.draw_layout_node(self.pos[self.sel_node])
                self.draw_edges(self.pos, self.sel_node)
        return self
        
    def fill_dim(self):
        """Dim out the current render (alpha 25%)"""
        
        return self.canvas.create_rectangle(
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

    def on_close(self):
        """Event window closed"""
        self.run = False
        self.kill_on_end = True
                
        
    def on_mouse_up(self, e):
        """LMB released"""
        self.lmb = False
        self.drag_node = None

        
        
        

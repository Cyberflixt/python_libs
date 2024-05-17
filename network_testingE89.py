
import random
from libs.network import Network

a = Network()
a.from_quick_links('T 8 S T 4 E E 10 S S 5 L S 8 N N 4 M N 2 L L 7 M M 10 E E 8 L T 4 E')
 
w = a.get_window()
w.set_layout(1)
w.bake()
a.show()

print(a.path_width_names_by_name('1'))

import minidem as dem
import random

dt = 0.005
t  = 0

    
def apply_gravity():
    for gr in dem.simu.grain_list:
        gr.force = dem.vec(0., -9.81*gr.mass)
        
def manage_contact():
    l = dem.lcm.compute_colliding_pair()
    for (gr1,gr2) in l:
        dem.contact(gr1,gr2)

def velocity_verlet():
    global t, dt
    t = t + dt
    for gr in dem.simu.grain_list:
        a = gr.force/gr.mass
        gr.vel += (gr.acc + a) * (dt/2.)
        gr.pos += gr.vel * dt + 0.5*a*(dt**2.)
        gr.acc  = a

def apply_boundaries():
    for gr in dem.simu.grain_list:

        if gr.pos[0] - gr.radius < 0:
            gr.pos[0] = gr.radius
            if gr.vel[0] < 0.:
                gr.vel[0] *= -.9

        elif gr.pos[0] + gr.radius > 100:
            gr.pos[0] = 100 - gr.radius
            if gr.vel[0] > 0.:
                gr.vel[0] *= -.9

        if gr.pos[1] - gr.radius < 0:
            gr.pos[1] = gr.radius
            if gr.vel[1] < 0.:
                gr.vel[1] *= -.9
            
        elif gr.pos[1] + gr.radius > 100:
            gr.pos[1] = 100 - gr.radius
            if gr.vel[1] > 0.:
                gr.vel[1] *= -.9


def time_loop():
    apply_gravity()
    manage_contact()
    velocity_verlet()
    apply_boundaries()


avg_rad = 1.5
mass = 1

for x in range(2, 99, 5):
    for y in range(2, 99, 5):
        pos = (x + random.random(), y + random.random())
        rad = avg_rad + random.random()
        gr  = dem.grain(pos, rad, mass)

dem.run(tot_iter_number=2000, update_plot_each=10, loop_fn=time_loop, video_name="dem_simulation.mp4")
dem.save_domain("compact-domain.txt")
print ("The end")
import urllib.parse import urlparse
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
import ipinfo
import matplotlib.pyplot as plt
from matplotlib import animation
import mpl_toolkits
from mpl_toolkits.basemap import Basemap

with open("history_data.txt", "r") as f:
    data = f.readlines()

domain_names = set()
for url in data:
    final_url = urlparse(url).netloc
    final_url = final_url.split(":")[0]
    domain_names.add(final_url)

ip_set = set()

def check_url(link):
    try:
        ip_addr = socket.gethostbyname(link)
        return ip_addr
    except:
        return

with ThreadPoolExecutor(max_workers=10) as e:
    for domain in domain_names:
        ip_set.add(e.submit(check_url, domain))

access_token = 'undefined'
handler = ipinfo.getHandler(access_token)

# queries IP info
def get_details(ip_address):
    try:
        details = handler.getDetails(ip_address)
        return details.all
    except:
        print(e)
        return
    
complete_details = []

with ThreadPoolExecutor(max_workers=10) as e:
    for ip_address in as_completed(ip_set):
        print(ip_address.result())
        complete_details.append(
            e.submit(get_details, ip_address.result())
        )
    
lat = []
lon = []

for loc in as_completed(complete_details):
    try:
        lat.append(float(loc.result()['latitude']))
        lon.append(float(loc.result()['longitude']))
    except:
        continue

# Set the size of the plot
fig, ax= plt.subplots(figsize=(40,20))
# removes whitespace on each side
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

map = Basemap()

# styling the map
# dark grey land, black lakes
map.fillcontinents(color='#2d2d2d', lake_color='#000000')
# black background
map.drawmapboundary(fill_color='#000000')
# thin white line for country borders
map.drawcountries(linewidth=0.15, color="w")

map.drawstates(linewidth=0.1, color="w")


def init():
    plt.text( -170, -72,'Server locations of top 500 websites '
        '(by traffic)\nPlot realized with Python and the Basemap library'
        '\n\n~Otero\n hi@otero.me', ha='left', va='bottom', 
        size=28, color='silver')

# Plot the points on the map
def update(frame_number):
    print(frame_number)
    m2.plot(lon[frame_number], lat[frame_number], linestyle='none',
            marker='o', markersize=25, alpha=0.4, c="white",
            markeredgecolor="silver", markeredgewidth=1)

# creating the FuncAnimation object and saving the actual animation:
# fig - the matplotlib being animated
# update - called for rendering each frame
# interval - delay between each frame in milliseconds
anil = animation.FuncAnimation(fig, update, interval=1,
                               frames=490, init_func= init)

writer = animation.writers['ffmpeg']
wirter = writer(fps=20, metadata=dict(artist='Me'), bitrate=1800)
ani.save(anim.mp4, writer=writer)

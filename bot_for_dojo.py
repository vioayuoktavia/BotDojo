import psutil, pyowm

# Create the DojoBot Class
class DojoBot:

    # Create a constant that contains the default text for the message
    DEFAULT_BLOCK_MESSAGE = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Your Computer Report : \n"
            ),
        },
    }

    # The constructor for the class. It takes the channel name as the a 
    # parameter and then sets it as an instance variable
    def __init__(self, channel):
        self.channel = channel

    def _send_report(self):
        text_template = "CPU Usage : %s \n Available Memory : %s  " % (psutil.cpu_percent(), 
                                                                        psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)
        
        return {"type": "section", "text": {"type": "mrkdwn", "text": text_template}},

    # Craft and return the entire message payload as a dictionary.
    def get_message_payload(self):
        return {
                "channel": self.channel,
                "blocks": [
                    self.DEFAULT_BLOCK_MESSAGE,
                    *self._send_report()
                ],
            }
    
    def _send_weather(self):
        api_key = "7e858c38e3133ccb67fd614d08bfe275"

        OpenWMap = pyowm.OWM(api_key)                   # Use API key to get data
        Weather = OpenWMap.weather_manager()  # give where you need to see the weather
        observation = Weather.weather_at_place("Indonesia")
        
        Data = observation.weather
        wind = Data.wind()
        text = "Wind Speed : %s \n Wind Direction : %s" % (wind["speed"], wind["deg"])

        return {"type": "section", "text": {"type": "mrkdwn", "text": text}},


    def weather_message_payload(self):
        return {
                "channel": self.channel,
                "blocks": [
                    *self._send_weather()
                ],
            }
        




# openweather
### Karen addon to get weather information using the [openweather API](https://openweathermap.org/api)

### commands
```
"what's the 7-day forecast",
"what's the weather",
"what's the forecast"
```

### installation
This add-on can be installed using the Karen App or via Karen's addon manager
```
python3 addon_manager.py --install https://github.com/AlfredoSequeida/openweather
```

### setup
Manually updating Karen's config file or using the Karen app, set the following settings:
lat - Lattitude of where you want to get the weather from
long - Longitude of where you want to get the weather from
units - Units to use for weather information. The valid options are `imperial`, `metric`, and `standard`
api_key - Your API key, this is free and you can get one by creating an account with [openweathermap.org](https://home.openweathermap.org/users/sign_up) and going [here](https://home.openweathermap.org/api_keys).

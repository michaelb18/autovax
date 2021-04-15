def load_location(login):
    import geocoder
    g = geocoder.ip('me')
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="an app name")
    location = geolocator.reverse(str(g.latlng[0])+', '+str(g.latlng[1]))#"52.509669, 13.376294")
    print('Your location will be ' + location.address)

    home = location.raw['address']['natural'] + location.raw['address']['road']
    city = location.raw['address']['city']
    state = location.raw['address']['state']
    zipcode = location.raw['address']['postcode']
    login['homeAddress'] = home
    login['city'] = city
    login['state'] = state
    login['zipCode'] = zipcode
    return login



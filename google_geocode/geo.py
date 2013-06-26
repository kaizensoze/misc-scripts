import csv
from geopy import geocoders

addresses = []
errors = []
with open('sample_input.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) > 1:
            addr = {}
            addr['name'] = row[1]
            addr['line1'] = row[2]
            addr['line2'] = row[3]
            addr['city'] = row[4]
            addr['state'] = row[5]
            addr['zipcode'] = row[6]
            addr['phone'] = row[7]
            addr['accountId'] = row[10]
            addr['isProduct'] = row[12]

            if len(addr['zipcode']) < 5:
                addr['zipcode'] = '0' + addr['zipcode']

            addresses.append(addr)

g = geocoders.Google('')

for address in addresses:
    keys_to_write = ['line1', 'line2', 'city', 'state', 'zipcode']
    addr_to_map_parts = []
    for key in keys_to_write:
        if len(address[key]) > 0:
            addr_to_map_parts.append(address[key])
    addr_to_map = ', '.join(addr_to_map_parts)

    try:
        (place, point) = g.geocode(addr_to_map)
        address['lat_lon'] = point
    except ValueError:
        errors.append(address)
        addresses.remove(address)

#print(addresses)

f = open('out.sql', 'w')
for address in addresses:
    if not address.has_key('lat_lon'):
        continue

    line = """
        INSERT INTO [dbo].[RetailLocations]
            ([Name], [Address1], [Address2], [City], [State], [PostalCode], [Phone], [Lat], [Lng], [AccntId], [LastUpdated], [Product])
        VALUES
            ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', getDate(), '%s');
        """ % (address['name'], address['line1'], address['line2'], address['city'], address['state'], address['zipcode'], address['phone'], address['lat_lon'][0], address['lat_lon'][1], address['accountId'], address['isProduct'])
    f.write(line)

f.close()

for error in errors:
    print(error['line1'], error['line2'], error['city'], error['state'], error['zipcode'])

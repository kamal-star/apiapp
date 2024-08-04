import frappe
from frappe.utils import now
import folium
import requests
from shapely.geometry import LineString
import polyline  # To decode Google Maps polyline

@frappe.whitelist(allow_guest=True)
def send_data_to_optimize_route_and_get_map(docsname,method="None"):
    doc=frappe.get_doc("Shipment Delivery",docsname)
    destination_latitudes = []
    destination_longitudes=[]
    sr=[]

    for child in doc.get("delivery_stops"):
        destination_latitudes.append(float(child.latitude))
        destination_longitudes.append(float(child.longitude))
        sr.append(child.service_request)
    # destination_locations=[
    #     {
    #         "latitude": 39.36884572,
    #         "longitude": 44.27144632
    #     },
    # ]
    
    data = {
        "source_latitude": float(doc.pickup_latitude),
        "source_longitude": float(doc.pickup_longitude),
        "destination_latitudes": destination_latitudes,
        "destination_longitudes":destination_longitudes,
        "service_request": sr
    }
    # Headers
    headers = {
        "Authorization": "token 2ded6868a0946dd:22b9bff0aeaf4a8"
    }

    # Step 2: Send the initial route data to your API endpoint for optimization
    api_url = 'http://77.37.87.48/api/method/optimal_route_finder.optimal_route_finder.doctype.api_logger.api_logger.route_api'  # Replace with your API endpoint
    response = requests.post(api_url, headers=headers,json=data)

    if response.status_code == 200:
        optimized_route_data = response.json()
    else:
        print(f"Failed to optimize route data: {response.status_code}")
        optimized_route_data = None

    # Step 3: Extract the bounding box (bbox) and geometry from the optimized route data
    if optimized_route_data:
        coordinates = []
        for route_info in optimized_route_data["message"]['route_info']:
            if route_info['provider'] == 'Google Maps':
                # Decode Google Maps polyline
                decoded_line = polyline.decode(route_info['geometry']['coordinates'])
                coordinates.extend(decoded_line)
            else:
                # Use Mapbox geometry directly
                coordinates.extend(route_info['geometry']['coordinates'])
        
        # Convert coordinates to shapely geometry
        line = LineString(coordinates)

        # Get bounding box
        bbox = line.bounds  # (minx, miny, maxx, maxy)

        # Calculate center for the map
        center_lat = (bbox[1] + bbox[3]) / 2
        center_lon = (bbox[0] + bbox[2]) / 2
        bounds = [[bbox[1], bbox[0]], [bbox[3], bbox[2]]]

        # Step 4: Create a Basemap centered on the optimized route
        basemap = folium.Map(location=[center_lat, center_lon], zoom_start=5)
        basemap.fit_bounds(bounds)

        # Add the starting point marker
        folium.Marker(
            [data["source_latitude"], data["source_longitude"]],
            popup="Starting Point",
            icon=folium.Icon(color="green")
        ).add_to(basemap)

        # Step 5: Add Optimized Route to the Basemap
        for route_info in optimized_route_data['message']['route_info']:
            destination = route_info['destination']
            travel_time = route_info['formatted_travel_time']
            distance = route_info['distance']
            
            if route_info['provider'] == 'Google Maps':
                # Decode Google Maps polyline
                decoded_line = polyline.decode(route_info['geometry']['coordinates'])
                folium.PolyLine(decoded_line, color="blue", weight=2.5, opacity=1).add_to(basemap)
            else:
                # Use Mapbox geometry directly
                folium.PolyLine(route_info['geometry']['coordinates'], color="green", weight=2.5, opacity=1).add_to(basemap)
            
            # Add destination marker with travel time and distance
            folium.Marker(
                [destination['latitude'], destination['longitude']],
                popup=f"Destination\nTime: {travel_time}\nDistance: {distance}",
                icon=folium.Icon(color="red")
            ).add_to(basemap)

        # Display total travel time on the map
        total_time = optimized_route_data.get('total_time', 'N/A')
        total_distance = optimized_route_data.get('total_distance', 'N/A')
        total_info_html = f"""
        <div style="position: fixed; bottom: 50px; left: 50px; width: 200px; height: 60px; background-color: white; border:2px solid grey; z-index: 1000; padding: 10px;">
            <h4>Total Travel Info</h4>
            <p>Time: {total_time}</p>
            <p>Distance: {total_distance}</p>
        </div>
        """
        folium.Marker(
            location=[center_lat, center_lon],
            icon=folium.DivIcon(html=total_info_html)
        ).add_to(basemap)
        return basemap._repr_html_()

        # Step 6: Save the Map to an HTML File
        # basemap.save("optimized_route_map.html")
        # with open("optimized_route_map.html", "r") as file:
        #     map_html_content = file.read()

        # # Update the HTML field in the shipment doctype
        # # frappe.db.set_value("Shipment Delivery",doc.name,"maps", map_html_content)
        # doc.map = map_html_content
        # # doc.maphtml = map_html_content
        # return map_html_content
        # doc.save()
        # return basemap
        # frappe.msgprint("Succesfully Optimized")
        # doc.map = map_html_content
        
        # doc.save()

        # Optional: Display the map directly in a Jupyter Notebook
        # from IPython.display import IFrame
        # IFrame(src="./optimized_route_map.html", width=700, height=500)
    # else:
    #     print("No optimized route data available to display on the map.")


@frappe.whitelist(allow_guest=True)
def send_data_to_optimize_route_and_get_map2(sr_latitude,sr_longitude,de_latitude,de_longitude):
    # doc=frappe.get_doc("Shipment Delivery",docsname)
    # destination_latitudes = []
    # destination_longitudes=[]
    # sr=[]

    # for child in doc.get("delivery_stops"):
    #     destination_latitudes.append(float(child.latitude))
    #     destination_longitudes.append(float(child.longitude))
    #     sr.append(child.service_request)
    # destination_locations=[
    #     {
    #         "latitude": 39.36884572,
    #         "longitude": 44.27144632
    #     },
    # ]
    
    data = {
        "source_latitude": float(sr_latitude),
        "source_longitude": float(sr_longitude),
        "destination_latitudes": de_latitude,
        "destination_longitudes":de_longitude
    }
    # Headers
    headers = {
        "Authorization": "token 2ded6868a0946dd:22b9bff0aeaf4a8"
    }

    # Step 2: Send the initial route data to your API endpoint for optimization
    api_url = 'http://77.37.87.48/api/method/optimal_route_finder.optimal_route_finder.doctype.api_logger.api_logger.route_api'  # Replace with your API endpoint
    response = requests.post(api_url, headers=headers,json=data)

    if response.status_code == 200:
        optimized_route_data = response.json()
    else:
        print(f"Failed to optimize route data: {response.status_code}")
        optimized_route_data = None

    # Step 3: Extract the bounding box (bbox) and geometry from the optimized route data
    if optimized_route_data:
        coordinates = []
        for route_info in optimized_route_data["message"]['route_info']:
            if route_info['provider'] == 'Google Maps':
                # Decode Google Maps polyline
                decoded_line = polyline.decode(route_info['geometry']['coordinates'])
                coordinates.extend(decoded_line)
            else:
                # Use Mapbox geometry directly
                coordinates.extend(route_info['geometry']['coordinates'])
        
        # Convert coordinates to shapely geometry
        line = LineString(coordinates)

        # Get bounding box
        bbox = line.bounds  # (minx, miny, maxx, maxy)

        # Calculate center for the map
        center_lat = (bbox[1] + bbox[3]) / 2
        center_lon = (bbox[0] + bbox[2]) / 2
        bounds = [[bbox[1], bbox[0]], [bbox[3], bbox[2]]]

        # Step 4: Create a Basemap centered on the optimized route
        basemap = folium.Map(location=[center_lat, center_lon], zoom_start=5)
        basemap.fit_bounds(bounds)

        # Add the starting point marker
        folium.Marker(
            [data["source_latitude"], data["source_longitude"]],
            popup="Starting Point",
            icon=folium.Icon(color="green")
        ).add_to(basemap)

        # Step 5: Add Optimized Route to the Basemap
        for route_info in optimized_route_data['message']['route_info']:
            destination = route_info['destination']
            travel_time = route_info['formatted_travel_time']
            distance = route_info['distance']
            
            if route_info['provider'] == 'Google Maps':
                # Decode Google Maps polyline
                decoded_line = polyline.decode(route_info['geometry']['coordinates'])
                folium.PolyLine(decoded_line, color="blue", weight=2.5, opacity=1).add_to(basemap)
            else:
                # Use Mapbox geometry directly
                folium.PolyLine(route_info['geometry']['coordinates'], color="green", weight=2.5, opacity=1).add_to(basemap)
            
            # Add destination marker with travel time and distance
            folium.Marker(
                [destination['latitude'], destination['longitude']],
                popup=f"Destination\nTime: {travel_time}\nDistance: {distance}",
                icon=folium.Icon(color="red")
            ).add_to(basemap)

        # Display total travel time on the map
        total_time = optimized_route_data.get('total_time', 'N/A')
        total_distance = optimized_route_data.get('total_distance', 'N/A')
        total_info_html = f"""
        <div style="position: fixed; bottom: 50px; left: 50px; width: 200px; height: 60px; background-color: white; border:2px solid grey; z-index: 1000; padding: 10px;">
            <h4>Total Travel Info</h4>
            <p>Time: {total_time}</p>
            <p>Distance: {total_distance}</p>
        </div>
        """
        folium.Marker(
            location=[center_lat, center_lon],
            icon=folium.DivIcon(html=total_info_html)
        ).add_to(basemap)
        return basemap._repr_html_()

        # Step 6: Save the Map to an HTML File
        # basemap.save("optimized_route_map.html")
        # with open("optimized_route_map.html", "r") as file:
        #     map_html_content = file.read()

        # # Update the HTML field in the shipment doctype
        # # frappe.db.set_value("Shipment Delivery",doc.name,"maps", map_html_content)
        # doc.map = map_html_content
        # # doc.maphtml = map_html_content
        # return map_html_content
        # doc.save()
        # return basemap
        # frappe.msgprint("Succesfully Optimized")
        # doc.map = map_html_content
        
        # doc.save()

        # Optional: Display the map directly in a Jupyter Notebook
        # from IPython.display import IFrame
        # IFrame(src="./optimized_route_map.html", width=700, height=500)
    # else:
    #     print("No optimized route data available to display on the map.")

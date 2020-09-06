import math
from collections import defaultdict
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
import json
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
db = SQLAlchemy(app)


agency_location_cache={}


class Agency(db.Model):
    __tablename__ = 'agency'
    id = Column(Integer, primary_key=True)
    broker = relationship("Broker", backref="agency")
    title = Column(db.String(50))
    domain = Column(db.String(50))
    address = Column(db.String(255))


class Broker(db.Model):
    __tablename__ = 'broker'
    id = Column(Integer, primary_key=True)
    agency_id = Column(Integer, ForeignKey('agency.id'))
    firstname = Column(db.String(50))
    lastname = Column(db.String(50))
    email = Column(db.String(50))
    address = Column(db.String(255))


class AgencyDomainWhitelist(db.Model):
    __tablename__ = "agency_domain_whitelist"
    id = Column(Integer, primary_key=True)
    domain = Column(db.String(50))


@app.route('/signup', methods=["POST"])
def sign_up():
    payload = json.loads(request.data)
    firstname = payload.get("firstname", None)
    lastname = payload.get("lastname", None)
    email = payload.get("email", None)
    address = payload.get("address", None)

    if not all([firstname, lastname, email, address]):
        return 'firstname,lastname,email,address required!', 400

    try:
        broker_domain = email.split("@")[1]
    except Exception:
        return 'Email is not valid!', 400

    if not AgencyDomainWhitelist.query.filter_by(domain=broker_domain).all():
        return 'No Agency Found!', 400

    q = Agency.query.filter_by(domain=broker_domain)

    if q.count() > 1:
        try:
            matched_agency = __get_closest_agency_to_broker(address, q.all())
        except Exception:
            return 'Check your address', 400
    else:
        matched_agency = q.order_by(Agency.id.desc()).first()

    # Everything is OK, create new broker:

    new_broker = Broker(firstname=firstname,
                        lastname=lastname,
                        email=email,
                        address=address,
                        agency_id=matched_agency.id)

    db.session.add(new_broker)
    db.session.commit()
    return 'New broker account created and assigned to:{}'.format(matched_agency.title), 201


def __get_closest_agency_to_broker(broker_address, agency_list):
    try:
        broker_coordinates = __get_coordinates_of_address(broker_address)
    except Exception:
        raise
    # O(n) runtime
    agency_distance_list = []
    # TODO: cache agency coordinates for performance
    for a in agency_list:
        agency_coordinates = __get_coordinates_of_address(a.address)
        agency_distance_list.append(
            {
                "agency": a,
                "coordinates": agency_coordinates,
                "distance": __calculate_cartesian_distance(broker_coordinates, agency_coordinates)
            }
        )

    min_distance_agency = agency_distance_list[0]
    for a in agency_distance_list:
        if a["distance"] < min_distance_agency["distance"]:
            min_distance_agency = a

    return min_distance_agency["agency"]


def __calculate_cartesian_distance(coor1, coor2):
    lat_diff = coor1.get("lat") - coor2.get("lat")
    lng_diff = coor1.get("lng") - coor2.get("lng")
    return math.sqrt(lat_diff ** 2 + lng_diff ** 2)


def __get_coordinates_of_address(address):
    #TODO API key must be environment variable
    api_key = "hfdi-6Pzch71e2nTGd6Hrw_BkoNNAgU4DTv17PlBd7I"
    geolocation_api = "https://geocode.search.hereapi.com/v1/geocode?apiKey=" + api_key
    query_endpoint = geolocation_api + "&q={}".format(address)

    # Avoid expensive api calls with simple cache:
    if agency_location_cache.get(address, None):
        return agency_location_cache[address]

    try:
        r = requests.get(query_endpoint)
        coordinate_pair = r.json().get('items')[0].get('position', None)
        if not coordinate_pair:
            raise Exception("Error parsing Geolocation data, probably invalid address")
    except Exception as e:
        print(e)
        raise e
    agency_location_cache[address] = coordinate_pair
    return coordinate_pair


@app.route('/brokers', methods=["GET"])
def list_brokers():
    brokers = Broker.query.all()

    brokers_list = []
    for b in brokers:
        brokers_list.append({
            "firstname": b.firstname,
            "lastname": b.lastname,
            "email": b.email,
            "address": b.address,
            "agency_name": b.agency.title,
            "agency_domain": b.agency.domain
        })
    return json.dumps(brokers_list)


def prepopulate_db():
    import csv
    import os

    with open(os.path.dirname(os.path.abspath(__file__)) + '/../data/agency_domain_whitelist.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for idx, row in enumerate(csv_reader):
            if idx != 0:
                adw = AgencyDomainWhitelist(domain=row[1])
                db.session.add(adw)
                db.session.commit()

    with open(os.path.dirname(os.path.abspath(__file__)) + '/../data/agency.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for idx, row in enumerate(csv_reader):
            if idx != 0:
                adw = Agency(title=row[1], domain=row[2], address=row[3])
                db.session.add(adw)
                db.session.commit()

    with open(os.path.dirname(os.path.abspath(__file__)) + '/../data/broker.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for idx, row in enumerate(csv_reader):
            if idx != 0:
                adw = Broker(firstname=row[0], lastname=row[1], email=row[2], address=row[3], agency_id=row[4])
                db.session.add(adw)
                db.session.commit()


def initialize_db():
    print("initializing db...")
    db.drop_all()
    db.create_all()
    prepopulate_db()


if __name__ == '__main__':
    initialize_db()
    app.run(debug=True, host="0.0.0.0")

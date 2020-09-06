import json

def test_signup_valid_broker(client):

    data = json.dumps(dict(
        firstname="testuser",
        lastname="testuser",
        email="email@cyberworld.com",
        address="MIAMI"
    ))
    rv = client.post("/signup", data=data)
    assert rv.status_code == 201

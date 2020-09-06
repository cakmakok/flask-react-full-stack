import json
def test_signup_invalid_broker(client):

    data = json.dumps(dict(
        firstname="testuser",
        lastname="testuser",
        email="email@notvaliddomain.com",
        address="dummyaddress"
    ))
    rv = client.post("/signup", data=data)
    assert rv.status_code == 400


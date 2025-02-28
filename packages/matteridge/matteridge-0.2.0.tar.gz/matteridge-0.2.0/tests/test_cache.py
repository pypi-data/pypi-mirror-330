from matteridge.cache import Cache


def test_user(tmp_path):
    c = Cache(tmp_path / "test.sql")

    c.add_server("example.com")
    c.add_server("example.com")

    c.add_user("example.com", "id", "name")
    c.add_user("example.com", "id", "name")

    assert c.get_by_user_id("example.com", "id").username == "name"
    assert c.get_by_username("example.com", "name").user_id == "id"


def test_direct_channel(tmp_path):
    c = Cache(tmp_path / "test.sql")

    c.add_server("example.com")

    c.add_user("example.com", "me", "myname")
    c.add_user("example.com", "them", "theirname")
    c.add_direct_channel("example.com", "me", "them", "channel")
    c.add_direct_channel("example.com", "me", "them", "channel")

    assert (
        c.get_user_by_direct_channel_id("example.com", "me", "channel").username
        == "theirname"
    )

    assert c.get_direct_channel_id("example.com", "me", "them") == "channel"

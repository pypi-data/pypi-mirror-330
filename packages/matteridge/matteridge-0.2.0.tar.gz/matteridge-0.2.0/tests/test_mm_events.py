from matteridge import events


def test_user_typing():
    user_typing = events.from_dict(
        {
            "event": "typing",
            "data": {"parent_id": "", "user_id": "8xhx4op61tdp9jorka88fi7psh"},
            "broadcast": {
                "omit_users": {"8xhx4op61tdp9jorka88fi7psh": True},
                "user_id": "",
                "channel_id": "drr65sfhttfrzydzde9uwqnc4w",
                "team_id": "",
                "connection_id": "",
                "omit_connection_id": "",
            },
            "seq": 1,
        }
    )
    assert isinstance(user_typing, events.Typing)
    assert user_typing.user_id == "8xhx4op61tdp9jorka88fi7psh"
    assert user_typing.broadcast.channel_id == "drr65sfhttfrzydzde9uwqnc4w"
    assert user_typing.broadcast.team_id == ""


def test_posted():
    posted = events.from_dict(
        {
            "event": "posted",
            "data": {
                "channel_display_name": "@nicocul",
                "channel_name": "8xhx4op61tdp9jorka88fi7psh__fqup8n699pnm7rwo1xt3krbw3c",
                "channel_type": "D",
                "mentions": '["fqup8n699pnm7rwo1xt3krbw3c"]',
                "post": '{"id":"18u1csu9etb5u8jangzzrkqz5a","create_at":1692688083105,"update_at":1692688083105,"edit_at":0,"delete_at":0,"is_pinned":false,"user_id":"8xhx4op61tdp9jorka88fi7psh","channel_id":"drr65sfhttfrzydzde9uwqnc4w","root_id":"","original_id":"","message":"fdff","type":"","props":{"disable_group_highlight":true},"hashtags":"","pending_post_id":"8xhx4op61tdp9jorka88fi7psh:1692688083034","reply_count":0,"last_reply_at":0,"participants":null,"metadata":{}}',
                "sender_name": "@nicocul",
                "set_online": True,
                "team_id": "",
            },
            "broadcast": {
                "omit_users": None,
                "user_id": "",
                "channel_id": "drr65sfhttfrzydzde9uwqnc4w",
                "team_id": "",
                "connection_id": "",
                "omit_connection_id": "",
            },
            "seq": 2,
        }
    )
    assert isinstance(posted, events.Posted)
    assert posted.post.id == "18u1csu9etb5u8jangzzrkqz5a"
    assert posted.post.user_id == "8xhx4op61tdp9jorka88fi7psh"
    assert posted.channel_type == "D"
    assert posted.set_online


def test_channel_viewed():
    v = events.from_dict(
        {
            "event": "channel_viewed",
            "data": {"channel_id": "drr65sfhttfrzydzde9uwqnc4w"},
            "broadcast": {
                "omit_users": None,
                "user_id": "fqup8n699pnm7rwo1xt3krbw3c",
                "channel_id": "",
                "team_id": "",
                "connection_id": "",
                "omit_connection_id": "",
            },
            "seq": 1,
        }
    )
    assert isinstance(v, events.ChannelViewed)
    assert v.channel_id == "drr65sfhttfrzydzde9uwqnc4w"


def test_user_updated():
    up = events.from_dict(
        {
            "event": "user_updated",
            "data": {
                "user": {
                    "id": "8xhx4op61tdp9jorka88fi7psh",
                    "create_at": 1692651314881,
                    "update_at": 1692688281975,
                    "delete_at": 0,
                    "username": "nicocul",
                    "auth_data": "",
                    "auth_service": "",
                    "email": "sdfasdf@dsfdsdsf.fr",
                    "nickname": "",
                    "first_name": "",
                    "last_name": "",
                    "position": "",
                    "roles": "system_user",
                    "props": {
                        "customStatus": '{"emoji":"calendar","text":"In a meeting","duration":"one_hour","expires_at":"2023-08-22T08:11:00Z"}'
                    },
                    "locale": "en",
                    "timezone": {
                        "automaticTimezone": "",
                        "manualTimezone": "",
                        "useAutomaticTimezone": "true",
                    },
                    "disable_welcome_email": False,
                }
            },
            "broadcast": {
                "omit_users": {"8xhx4op61tdp9jorka88fi7psh": True},
                "user_id": "",
                "channel_id": "",
                "team_id": "",
                "connection_id": "",
                "omit_connection_id": "",
                "contains_sensitive_data": True,
            },
            "seq": 4,
        }
    )
    assert isinstance(up, events.UserUpdated)
    assert up.user.id == "8xhx4op61tdp9jorka88fi7psh"
    # assert up.user.props.additional_properties["customStatus"].emoji == "calendar"


def test_status_change():
    ch = events.from_dict(
        {
            "event": "status_change",
            "data": {"status": "away", "user_id": "fqup8n699pnm7rwo1xt3krbw3c"},
            "broadcast": {
                "omit_users": None,
                "user_id": "fqup8n699pnm7rwo1xt3krbw3c",
                "channel_id": "",
                "team_id": "",
                "connection_id": "",
                "omit_connection_id": "",
            },
            "seq": 4,
        }
    )
    assert isinstance(ch, events.StatusChange)
    assert ch.status == "away"
    assert ch.user_id == "fqup8n699pnm7rwo1xt3krbw3c"


def test_post_edited():
    edited = events.from_dict(
        {
            "event": "post_edited",
            "data": {
                "post": '{"id":"18u1csu9etb5u8jangzzrkqz5a","create_at":1692688083105,"update_at":1692688675756,"edit_at":1692688675756,"delete_at":0,"is_pinned":false,"user_id":"8xhx4op61tdp9jorka88fi7psh","channel_id":"drr65sfhttfrzydzde9uwqnc4w","root_id":"","original_id":"","message":"fdffkk","type":"","props":{"disable_group_highlight":true},"hashtags":"","pending_post_id":"","reply_count":0,"last_reply_at":0,"participants":null,"metadata":{}}'
            },
            "broadcast": {
                "omit_users": None,
                "user_id": "",
                "channel_id": "drr65sfhttfrzydzde9uwqnc4w",
                "team_id": "",
                "connection_id": "",
                "omit_connection_id": "",
            },
            "seq": 4,
        }
    )
    assert isinstance(edited, events.PostEdited)
    assert edited.post.id == "18u1csu9etb5u8jangzzrkqz5a"


def test_post_deleted():
    deleted = events.from_dict(
        {
            "event": "post_deleted",
            "data": {
                "delete_by": "8xhx4op61tdp9jorka88fi7psh",
                "post": '{"id":"18u1csu9etb5u8jangzzrkqz5a","create_at":1692688083105,"update_at":1692688675756,"edit_at":1692688675756,"delete_at":0,"is_pinned":false,"user_id":"8xhx4op61tdp9jorka88fi7psh","channel_id":"drr65sfhttfrzydzde9uwqnc4w","root_id":"","original_id":"","message":"fdffkk","type":"","props":{"disable_group_highlight":true},"hashtags":"","pending_post_id":"","reply_count":0,"last_reply_at":0,"participants":null}',
            },
            "broadcast": {
                "omit_users": None,
                "user_id": "",
                "channel_id": "drr65sfhttfrzydzde9uwqnc4w",
                "team_id": "",
                "connection_id": "",
                "omit_connection_id": "",
                "contains_sensitive_data": True,
            },
            "seq": 1,
        }
    )
    assert isinstance(deleted, events.PostDeleted)
    assert deleted.post.id == "18u1csu9etb5u8jangzzrkqz5a"
    assert deleted.delete_by == "8xhx4op61tdp9jorka88fi7psh"


def test_reaction_added():
    added = events.from_dict(
        {
            "event": "reaction_added",
            "data": {
                "reaction": '{"user_id":"8xhx4op61tdp9jorka88fi7psh","post_id":"bki8mmackpby8b7a3cdid7cmpy","emoji_name":"+1","create_at":1692688870813,"update_at":1692688870813,"delete_at":0,"remote_id":"","channel_id":"drr65sfhttfrzydzde9uwqnc4w"}'
            },
            "broadcast": {
                "omit_users": None,
                "user_id": "",
                "channel_id": "drr65sfhttfrzydzde9uwqnc4w",
                "team_id": "",
                "connection_id": "",
                "omit_connection_id": "",
            },
            "seq": 3,
        }
    )
    assert isinstance(added, events.ReactionAdded)
    assert added.reaction.user_id == "8xhx4op61tdp9jorka88fi7psh"
    assert added.reaction.emoji_name == "+1"


def test_reaction_removed():
    removed = events.from_dict(
        {
            "event": "reaction_removed",
            "data": {
                "reaction": '{"user_id":"8xhx4op61tdp9jorka88fi7psh","post_id":"bki8mmackpby8b7a3cdid7cmpy","emoji_name":"+1","create_at":0,"update_at":1692688987734,"delete_at":0,"remote_id":"","channel_id":""}'
            },
            "broadcast": {
                "omit_users": None,
                "user_id": "",
                "channel_id": "drr65sfhttfrzydzde9uwqnc4w",
                "team_id": "",
                "connection_id": "",
                "omit_connection_id": "",
            },
            "seq": 1,
        }
    )
    assert isinstance(removed, events.ReactionRemoved)
    assert removed.reaction.user_id == "8xhx4op61tdp9jorka88fi7psh"
    assert removed.reaction.emoji_name == "+1"


def test_direct_added():
    added = events.from_dict(
        {
            "event": "direct_added",
            "data": {
                "creator_id": "7gmp5ysfq3rwubknc543fs4dwr",
                "teammate_id": "ib3jjjy75fdpjm9pioq15bmbfe",
            },
            "broadcast": {
                "omit_users": None,
                "user_id": "",
                "channel_id": "ee111hwyajn4ifih3dg5p3fbwc",
                "team_id": "",
                "connection_id": "",
                "omit_connection_id": "",
            },
            "seq": 2,
        }
    )
    assert isinstance(added, events.DirectAdded)
    assert added.creator_id == "7gmp5ysfq3rwubknc543fs4dwr"
    assert added.teammate_id == "ib3jjjy75fdpjm9pioq15bmbfe"


def test_channel_created():
    created = events.from_dict(
        {
            "event": "channel_created",
            "data": {
                "channel_id": "9uwpihcx83r5unr58ccing49mc",
                "team_id": "qhqtxhzropfjixhbjofkz3m81r",
            },
            "broadcast": {
                "omit_users": None,
                "user_id": "7gmp5ysfq3rwubknc543fs4dwr",
                "channel_id": "",
                "team_id": "",
                "connection_id": "",
                "omit_connection_id": "",
            },
            "seq": 18,
        }
    )
    assert isinstance(created, events.ChannelCreated)
    assert created.channel_id == "9uwpihcx83r5unr58ccing49mc"
    assert created.team_id == "qhqtxhzropfjixhbjofkz3m81r"


def test_user_added():
    added = events.from_dict(
        {
            "event": "user_added",
            "data": {
                "team_id": "qhqtxhzropfjixhbjofkz3m81r",
                "user_id": "ib3jjjy75fdpjm9pioq15bmbfe",
            },
            "broadcast": {
                "omit_users": None,
                "user_id": "",
                "channel_id": "9uwpihcx83r5unr58ccing49mc",
                "team_id": "",
                "connection_id": "",
                "omit_connection_id": "",
            },
            "seq": 18,
        }
    )
    assert isinstance(added, events.UserAdded)
    assert added.team_id == "qhqtxhzropfjixhbjofkz3m81r"
    assert added.user_id == "ib3jjjy75fdpjm9pioq15bmbfe"


def test_posted_user_added():
    posted = events.from_dict(
        {
            "event": "posted",
            "data": {
                "channel_display_name": "privé",
                "channel_name": "prive",
                "channel_type": "P",
                "mentions": '["ib3jjjy75fdpjm9pioq15bmbfe"]',
                "post": '{"id":"shydbsd3xjys5b3aqwms7c95ah","create_at":1693152077355,"update_at":1693152077355,"edit_at":0,"delete_at":0,"is_pinned":false,"user_id":"7gmp5ysfq3rwubknc543fs4dwr","channel_id":"9uwpihcx83r5unr58ccing49mc","root_id":"","original_id":"","message":"test2 added to the channel by test.","type":"system_add_to_channel","props":{"addedUserId":"ib3jjjy75fdpjm9pioq15bmbfe","addedUsername":"test2","userId":"7gmp5ysfq3rwubknc543fs4dwr","username":"test"},"hashtags":"","pending_post_id":"","reply_count":0,"last_reply_at":0,"participants":null,"metadata":{}}',
                "sender_name": "System",
                "set_online": True,
                "team_id": "qhqtxhzropfjixhbjofkz3m81r",
            },
            "broadcast": {
                "omit_users": None,
                "user_id": "",
                "channel_id": "9uwpihcx83r5unr58ccing49mc",
                "team_id": "",
                "connection_id": "",
                "omit_connection_id": "",
            },
            "seq": 19,
        }
    )
    assert posted.post.type == "system_add_to_channel"

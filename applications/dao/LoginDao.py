from func import select_req


def findById(id, pin):
    data = select_req(
        f"select * from ms_user where user_id= %(user_id)s and pin=%(pin)s", {'user_id': id, 'pin': pin})
    print(f"data ini {data}")
    return data

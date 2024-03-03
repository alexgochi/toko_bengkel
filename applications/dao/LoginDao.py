from func import select_req


def findById(id):
    data = select_req(
        f"select * from ms_user where user_id= %(user_id)s", {'user_id': id})
    print(f"data ini {data}")
    return data

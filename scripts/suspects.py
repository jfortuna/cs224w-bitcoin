def get_
    f = open("../Bitcoin/user_edges.txt", 'r')
    lines = f.readlines()
    user_time_pairs = ((line[1], line[3]) for line in lines.split(','))
    user_time_pairs = sorted(user_time_pairs, key=lambda x:x[0])
    user_transactions = []
    cur_user = None
    cur_trans = None
    for pair in user_time_pairs:
    

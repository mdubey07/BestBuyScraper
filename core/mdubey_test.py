from datetime import datetime, timedelta

sep = '/'
text = '18.02.2020 / 11:56'
rest = text.split(sep, 1)[0]
rest.strip()
# rest = rest.replace('.', '/')
print(rest)

past = datetime.now() - timedelta(days=1)
present = datetime.now()
print(present)
print(past)
if past < present:
    print("true")
else:
    print("false")

date_object = datetime.strptime(rest.strip(), "%d.%m.%Y")
date_today = datetime.strptime(str(datetime.now().date()), "%Y-%m-%d")
print(date_object)
print("current date - " + str(date_today))
print(datetime.now().date())

long_str = 'გადაცემათა კოლოფი: მექანიკა, საჭე: მარცხენა'
# xy_list = long_str.split(',')
# print(xy_list)
# # matching = [s for s in xy_list if ":" in s]
# pair_list = []
# un_pair_list = []
# add_info = {}
# for s in xy_list:
#     if ':' in s:
#         pair_list.append(s.strip())
#     else:
#         un_pair_list.append(s.strip())
# for p in pair_list:
#     add_info[p.split(':')[0].strip()] = p.split(':')[1].strip()
# print(pair_list)
# print(add_info)


# print(un_pair_list)


def car_add_infos(item_str):
    pair_list = []
    un_pair_list = []
    combine_list = []

    for s in item_str.split(','):
        if ':' in s:
            pair_list.append(s.strip())
        else:
            un_pair_list.append(s.strip())
    combine_list.append(pair_list)
    combine_list.append(un_pair_list)
    return combine_list


print(car_add_infos(long_str))


def car_add_pair_info(item_list):
    add_info = {}
    for p in item_list:
        add_info[p.split(':')[0].strip()] = p.split(':')[1].strip()
    return add_info


print(car_add_pair_info(car_add_infos(long_str)[0]))

if 'გადაცემათა კოლოფი' in car_add_pair_info(car_add_infos(long_str)[0]):
    print(car_add_pair_info(car_add_infos(long_str)[0])['გადაცემათა კოლოფი'])

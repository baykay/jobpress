import os
import string
from jobs.models import JobsCategories
import random
from django.contrib.auth import get_user_model
Users = get_user_model()
for user in Users:
    user.interests.add(random.randint(5, 10))
    user.save()

#
# dm = ['com', 'org', 'in', 'mail', 'info', 'co', 'io', 'ng']
#
# ms = ['gmail', 'yahoo', 'outlook', 'aol', 'yandex']
#
#
# def dm_gen():
#     index = random.randint(1, 7)
#     return dm[index]
#
#
# def ms_gen():
#     index = random.randint(1, 6)
#     return ms[index]
#
#
# dm_list = dm_gen()
# ms_list = ms_gen()

# in_filename = 'freelancer_names'
# out_filename = f'{in_filename}_cleaned.txt'
# in_mode = 'r'
# out_mode = 'w'
# with open(out_filename, out_mode) as tagline:
#     for line in open(in_filename + '.txt', in_mode):
#         name = line.strip().split(' ')
#         if len(name) > 1:
#             name1 = line.strip().split(' ')[0]
#             name2 = line.strip().split(' ')[1]
#             new_name = f'{name2} {name1}\n'
#             tagline.write(new_name)
#             print(line)
# # os.remove(in_filename+".txt")
# os.rename(out_filename, 'freelancer_name_reversed.txt')
# print('Done')


# To extract lines that has more than 3 words for company tagline
# import os
#
# address_list = '''

# in_filename = 'addresses'
# out_filename = f'{in_filename}_cleaned.txt'
# in_mode = 'r'
# out_mode = 'a'
# with open(out_filename, out_mode) as tagline:
#     for name in address_list.split(','):
#         new_name = f'{name}\n'.strip()
#         tagline.write(new_name)
#         print(new_name)
#
# # os.remove(in_filename+".txt")
# os.rename(out_filename, 'addresses_.txt')
# print('Done')

#
# def rsg(size=10, char=string.ascii_lowercase + string.digits):
#     return ''.join(random.choice(char) for _ in range(size))
#
#
# # To extract duplicate lines
# in_filename = 'freelancer_name'
# out_filename = f'{in_filename}_no_dup.txt'
# in_mode = 'r'
# out_mode = 'w'
# with open(out_filename, out_mode) as out_names:
#     for each_line in open(in_filename + '.txt', in_mode):
#         names = each_line.split('-')[0]
#         name = names.split(' ')[1]
#         fname = names.split(' ')[0]
#         lname = name.replace(name, name+rsg(size=2))
#         prof = each_line.split('-')[1]
#         adrs = each_line.split('-')[2]
#         name_to_write = f"{fname} {lname} - {prof} - {adrs}\n"
#         print(name_to_write)
#         out_names.write(name_to_write)
# # os.remove(in_filename+".txt")
# os.rename(out_filename, 'freelancer_names_new.txt')
# print('Done')

# To set the freelancer unique username

#
# in_filename = 'company_email.txt'
# out_filename = f'{in_filename}_cleaned.txt'
# in_mode = 'r'
# out_mode = 'w'
# unique_usernames = set()
# with open(out_filename, out_mode) as unique_names:
#     for username in open(in_filename, in_mode):
#         if username.strip().split('@')[0] in unique_usernames:
#             username = username.strip().split('.')[1][:4]
#         unique_names.write(username)
#         unique_usernames.add(username)
# # os.remove(in_filename+".txt")
# os.rename(out_filename, 'company_email.txt')
# print('Done')
#
# dm = ['com', 'org', 'in', 'mail', 'info', 'co', 'io', 'ng']
#
# ms = ['gmail', 'yahoo', 'outlook', 'aol', 'yandex']
#
#
# def dm_gen():
#     index = random.randint(1, 8)
#     return dm[index]
#
#
# def ms_gen():
#     index = random.randint(1, 5)
#     return ms[index]
#
#
# dm_list = dm_gen()
# ms_list = ms_gen()
# in_filename = 'company_name.txt'
# out_filename = f'{in_filename}_cleaned.txt'
# in_mode = 'r'
# out_mode = 'w'
# with open(out_filename, out_mode) as unique_names:
#     for row in open(in_filename, in_mode):
#         name1 = row.strip().split(' ')[0]
#         name2 = row.strip().split(' ')[1]
#         email = f'{name1.lower()}{name2.lower()}@{ms_list}.{dm_list}\n'
#         print(email)
#         unique_names.write(email)
# # os.remove(in_filename+".txt")
# os.rename(out_filename, 'company_email.txt')
# print('Done')

# To set distinct email for company
# in_filename = 'freelancer_email_no_dup'
# out_filename = f'{in_filename}_cleaned.txt'
# in_mode = 'r'
# out_mode = 'a'
# with open(out_filename, out_mode) as company_email:
#     for email in open(in_filename + '.txt', in_mode):
#         renamed_email = 'company_' + email
#         company_email.write(renamed_email)
# # os.remove(in_filename+".txt")
# os.rename(out_filename, 'company_email.txt')
# print('Done')

# To se the freelancer profession
import os
#
# in_filename = 'addresses_'
# out_filename = f'{in_filename}_cleaned.txt'
# in_mode = 'r'
# out_mode = 'a'
# with open(out_filename, out_mode) as profession:
#     for line in open(in_filename + '.txt', in_mode):
#         if len(line.strip().split(' ')) >= 2:
#             profession.write(line)
# # os.remove(in_filename+".txt")
# # os.rename(out_filename, 'address_.txt')
# print('Done')

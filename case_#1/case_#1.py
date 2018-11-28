import pandas as pd
#!pip3 install requests
import requests
BASE_URL = "https://api.hh.ru/areas"
requests.get(BASE_URL)
s = requests.Session()
response = s.get(BASE_URL)
content = response.json()
dict1 = {}  # cловарь город-id
def find_name(name, content):
    dict1[content["name"]] = content["id"]
    if len(content["areas"]) > 0:
        for item in content["areas"]:
            find_name(name, item)
for cont in content:
    find_name("Московская область", cont)
def distance(city_a, city_b):
    n, m = len(city_a), len(city_b)
    a, b = city_a, city_b
    if n > m:
        a, b = b, a
        n, m = m, n
    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


class C_Validator():
    def c_validate(self, city):
        import re
        city = city.lower()
        #sub = re.sub('[,.]|([\s][\п][\г][\т])|([\п][\о][\с][\s])|([\s][\г][\.][\s]+)|([\г][\.][\s]+)|([\г]{1}[\s]+)|([\с]+[\s]+)|([\s][\д][\.][\s])|(^[\д][\.][\s])|(^[\д][\s])|([\о][\б][\л])|([\s][\к][\р])|([\м][\к][\р]+[\s]+)|([\с][\т][\а][\н][\и][\ц][\а][\s])|([\s][\р][\а][\и][\о][\н])|([\р][-][\н])',"", city)
        city = city.replace("й", "и")
        city = city.replace("ё", "е")
        sub = re.sub('[,-.]|пгт|пос |р?п |г |с |д |обл|кр|мкр|станица|раион|р-н|область|краи|республика|ао', "", city)
        if sub == "":
            return None
        if sub == None:
            return None
        return sub.strip()
"""
# тест функции c_validate()
all_sity = ['волжский район', 'Сибирский р-н', 'пос ПосСибирский пгт']
validator2 = C_Validator()
list_sity = [validator2.c_validate(list_sity) for list_sity in all_sity ]
print (list_sity)
"""


class E_Validator():
    def e_validate(self, email):
        import re
        # match = re.match('^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+[\-]+(\.[a-z0-9_-]+)*[\.]{2}[a-z]{2,5}$' , email)
        match = re.match(
            "^[-a-z0-9!#$%&'*+/=?^_`{|}~]+(?:\.[-a-z0-9!#$%&'*+/=?^_`{|}~]+)*@(?:[a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*(?:aero|arpa|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|[a-z][a-z])$",
            email)
        if match == None:
            return None
        else:
            return email
"""
# тест функции e_validate()
all_email = ['chizhikilia@gmail.com', 'sasha3419@mai.-.ru', 'perxin.a@sdgr.ru', 'krikу19.94@mail.ru', '', 'email']
validator1 = E_Validator()
list_email = [validator1.e_validate(list_email) for list_email in all_email]
print(list_email)
"""


class P_Validator():
    def p_validate(self, phone):
        import re
        l = 0
        i = 0
        phone = phone.replace("-", "")
        phone = phone.replace(" ", "")
        phone = phone.replace(")", "")
        phone = phone.replace("(", "")
        phone = phone.replace(" ", "")
        l = len(phone)
        # phone = "".join(re.findall("\d+", phone))
        if phone == "":
            return None
        if (phone[0] == "8" and (phone[1] != "9" or l != 11)) or (phone[0] == "9" and l != 10) or (
                phone[0] == "+" and (phone[1] != "7" or phone[2] != "9" or l != 12)):
            return None
        if (l < 10) or (l > 12):
            return None
        if phone[0] != "+" and phone[1] != "7":
            if phone[0] == "8":
                phone = phone[1:]
                phone = "+7" + phone
            elif phone[0] == "9":
                phone = "+7" + phone
        if phone[0] != "+":
            return None
        return phone
"""
# тест функции p_validate()
phones = ['38099258352', "украли=", "+79090994519", "+79090994519", "+79090994519", "89090994519", "9090994519", "+79090994519", "+79090994519", "89090994519"]
validator = P_Validator()
new_list = [validator.p_validate(new_list) for new_list in phones]
print(new_list)
"""
def get_id(city_name, max_distance=0):
    """
    Функция преобразовывает название города в id города из словаря hh (dict1)
    """
    validator = C_Validator()
    validated_city = validator.c_validate(city_name)
    list_city_names = dict1.keys()
    for name in list_city_names:
        if max_distance >= distance(validator.c_validate(name), validated_city):
            return dict1[name]
def get_id_in_row(city_name):
    len_space = len([c for c in city_name if c in [' ', '\n', '\t']])
    if len_space > 0:
        city_name.strip
        city_name = city_name.split(' ')
        for name in city_name:
            name = name.replace(" ", "")
            if name != "":
              name = get_id(name, 0)
              if name != None:
                  return name
    if len_space == 0:
         name = get_id(city_name, 0)
         return name
# print(get_id("волжскии район", 0))
data = pd.read_csv("CRM_sample.tsv", sep='\t')
pd.options.mode.chained_assignment = None                                                                                  # убрать предупреждение о копии...
validator = P_Validator()
validator_e = E_Validator()
validator_c = C_Validator()
data['validation_city'] = 0                                                                                                # новый столбец
data['id'] = 0                                                                                                             # новый столбец

data['phone_validation']= data['phone_validation'].astype(str)                                                             # меняем тип данных столбца
data['HomePhone']= data['HomePhone'].astype(str)
data['Email']= data['Email'].astype(str)
data['validation_email']= data['validation_email'].astype(str)
data['City']= data['City'].astype(str)                                                                                     # меняем тип данных столбца
data['validation_city']= data['validation_city'].astype(str)                                                               # меняем тип данных столбца
data['phone_validation'] = data['HomePhone'].apply(validator.p_validate)                                                   # применяем validator.p_validate к столбцу HomePhone и заносим в phone_validation
data['validation_email'] = data['Email'].apply(validator_e.e_validate)                                                     # тоже что и строчкой выше только для email


#
data_clean = data[(data['validation_email'].notnull())|(data['phone_validation'].notnull()) & (data['City'].notnull()) ]  # все значения, где город не пустой и email или телефон не пустой
data_clean['validation_city'] = data_clean['City'].apply(validator_c.c_validate)                                          # валидируем столбец

data_clean['id'] = data_clean['validation_city'].apply(get_id_in_row)
data_clean = data_clean[(data_clean['id'].notnull())]                                                                     # выбираем только все строки имеющие id

offer = pd.read_csv("offers.tsv", sep='\t')                                                                               # добавляем табл предложения
offer['id']= ""                                                                                                           # добавляем столбец id
offer['Place']= offer['Place'].astype(str)                                                                                # меняем тип данных на str
offer['id'] = offer['Place'].apply(get_id)                                                                                # заносим в id id c помощью функции get_id
result = pd.merge(offer, data_clean, on = 'id')                                                                           # соеденяем по id
result = result[["FirstName", "LastName", "City", "validation_email", "phone_validation", "Text"]]                        # обрезаем полученную таблицу
result.to_csv("test.tsv", sep='\t', index=False)                                                                          # создаем test.tsv
print(result)
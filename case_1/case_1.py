class Validator:
    @staticmethod
    def c_validate(city):

        import re
        city = city.lower()
        city = city.replace("й", "и")
        city = city.replace("ё", "е")
        sub_sity = re.sub('[,-.]|пгт|пос |р?п |г |с |д |обл|кр|мкр|станица|раион|р-н|область|краи|республика|ао', "",
                          city)
        if sub_sity == "":
            return None
        if sub_sity is None:
            return None
        return sub_sity.strip()

    """
     # тест функции c_validate()
     all_sity = ['волжский район', 'Сибирский р-н', 'пос ПосСибирский пгт']
     validator2 = C_Validator()
     list_sity = [validator2.c_validate(list_sity) for list_sity in all_sity ]
     print (list_sity)
     """

    @staticmethod
    def e_validate(email):

        match = re.match(
            "^[-a-z0-9!#$%&'*+/=?^_`{|}~]+(?:\.[-a-z0-9!#$%&'*+/=?^_`{|}~]+)*@(?:[a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?\.)*(?:aero|arpa|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|[a-z][a-z])$",
            email)
        if match is None:
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

    @staticmethod
    def p_validate(phone):

        phone = phone.replace("-", "")
        phone = phone.replace(" ", "")
        phone = phone.replace(")", "")
        phone = phone.replace("(", "")
        phone = phone.replace(" ", "")
        lens_phone = len(phone)
        if phone == "":
            return None
        if (phone[0] == "8" and (phone[1] != "9" or lens_phone != 11)) or (phone[0] == "9" and lens_phone != 10) or (
                phone[0] == "+" and (phone[1] != "7" or phone[2] != "9" or lens_phone != 12)):
            return None
        if (lens_phone < 10) or (lens_phone > 12):
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
    valid = Validator()
    validated_city = valid.c_validate(city_name)
    list_city_names = dict1.keys()
    for name in list_city_names:
        if max_distance >= distance(valid.c_validate(name), validated_city):
            return dict1[name]


def get_id_in_row(city_name):
    import re
    len_space = len([c for c in city_name if c in [' ', '\n', '\t']])
    if len_space > 0:
        city_name.strip
        city = city_name.split(' ')
        for name in city:
            name = name.replace(" ", "")
            if name != "":
                name = get_id(name, 0)

                if name is not None:
                    return name
    if len_space == 0:
        name = get_id(city_name, 0)
        return name


def find_name(name, contents):
    dict1[contents["name"]] = contents["id"]
    if len(contents["areas"]) > 0:
        for item in contents["areas"]:
            find_name(name, item)



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



if __name__ == "__main__":
    import re
    import pandas as pd
    import requests

    BASE_URL = "https://api.hh.ru/areas"
    requests.get(BASE_URL)
    s = requests.Session()
    response = s.get(BASE_URL)
    content = response.json()
    dict1 = {}  # cловарь город-id
    for cont in content:
        find_name("Московская область", cont)
    data = pd.read_csv("CRM_sample.tsv", sep='\t')
    # убираем предупреждение о копии...
    pd.options.mode.chained_assignment = None
    validator = Validator()
    # добовляем столбцы
    data['validation_city'] = 0
    data['id'] = 0
    # меняем тип данных столбц
    data['phone_validation'] = data['phone_validation'].astype(str)
    data['HomePhone'] = data['HomePhone'].astype(str)
    data['Email'] = data['Email'].astype(str)
    data['validation_email'] = data['validation_email'].astype(str)
    data['City'] = data['City'].astype(str)
    data['validation_city'] = data['validation_city'].astype(str)
    data['phone_validation'] = data['HomePhone'].apply(validator.p_validate)
    # применяем validator.p_validate к столбцу HomePhone и заносим в phone_validation
    data['validation_email'] = data['Email'].apply(validator.e_validate)
    # все значения, где город не пустой и email или телефон не пустой
    data_clean = data[
        (data['validation_email'].notnull()) | (data['phone_validation'].notnull()) & (data['City'].notnull())]
    data_clean['validation_city'] = data_clean['City'].apply(validator.c_validate)
    # валидируем столбец
    data_clean['id'] = data_clean['validation_city'].apply(get_id_in_row)
    # выбираем только строки имеющие id
    data_clean = data_clean[(data_clean['id'].notnull())]
    offer = pd.read_csv("offers.tsv", sep='\t')
    offer['id'] = ""
    offer['Place'] = offer['Place'].astype(str)
    # заносим в id id c помощью функции get_id
    offer['id'] = offer['Place'].apply(get_id)
    # соеденяем по id
    result = pd.merge(offer, data_clean, on='id')
    result = result[["FirstName", "LastName", "City", "validation_email", "phone_validation", "Text"]]
    # создаем test.tsv
    result.to_csv("test.tsv", sep='\t', index=False)

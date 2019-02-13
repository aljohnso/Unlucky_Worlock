
accountSystemInputs = {'user_AJ': {
                    'googleNum': '1234',
                    'picture': 'https://i.ytimg.com/vi/28B6ncI92js/hqdefault.jpg',
                    'username': 'Alasdair Johnson',
                    'email': 'alasdair@gmail.com',
                    'firstName': 'Alasdair',
                    'lastName': 'Johnson',
                    'gender': 'TBD',
                    'age': '19',
                    'height': '60.0',
                    'allergies': 'TBD',
                    'dietRestrictions': 'TBD',
                    'studentIDNumber': '12345',
                    'phoneNumber': '99988887777',
                    'carCapacity': '0',
                    'locale': 'en'
                },
     'user_MV': {   'googleNum': '2345',
                    'picture': 'https://i.ytimg.com/vi/28B6ncI92js/hqdefault.jpg',
                    'username': 'Matthew vonAllmen',
                    'email': 'matthew@gmail.com',
                    'firstName': 'Matthew',
                    'lastName': 'vonAllmen',
                    'gender': 'TBD',
                    'age': '19',
                    'height': '60.0',
                    'allergies': 'TBD',
                    'dietRestrictions': 'TBD',
                    'studentIDNumber': '12345',
                    'phoneNumber': '99988887777',
                    'carCapacity': '0',
                    'locale': 'en'
                },
     'user_MB': {   'googleNum': '3456',
                    'picture': 'https://i.ytimg.com/vi/28B6ncI92js/hqdefault.jpg',
                    'username': 'Mario Batali',
                    'email': 'mariobatali@gmail.com',
                    'firstName': 'Mario',
                    'lastName': 'Batali',
                    'gender': 'TBD',
                    'age': '19',
                    'height': '60.0',
                    'allergies': 'TBD',
                    'dietRestrictions': 'TBD',
                    'studentIDNumber': '12345',
                    'phoneNumber': '99988887777',
                    'carCapacity': '0',
                    'locale': 'en'
                }
    }

accountSystemExpected = {
        'expected_AJ': accountSystemInputs['user_AJ'],
        'expected_MV': accountSystemInputs['user_MV'],
        'expected_MB': accountSystemInputs['user_MB']
    }

apiHelperInput = {'user_AJ' : {"meta": {"type": "account", "operation": "create"},
                               "token": "1as",
                               "payload": {
                                    'googleNum': '3456',
                                    'picture': 'https://i.ytimg.com/vi/28B6ncI92js/hqdefault.jpg',
                                    'username': 'Mario Batali',
                                    'email': 'mariobatali@gmail.com',
                                    'firstName': 'Mario',
                                    'lastName': 'Batali',
                                    'gender': 'TBD',
                                    'age': '19',
                                    'height': '60.0',
                                    'allergies': 'TBD',
                                    'dietRestrictions': 'TBD',
                                    'studentIDNumber': '12345',
                                    'phoneNumber': '99988887777',
                                    'carCapacity': '0',
                                    'locale': 'en'
                                    }}}

apiHelperExpected= {
        'expected_AJ': apiHelperInput['user_AJ']['payload']
    }
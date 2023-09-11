from amocrm.v2 import tokens, Lead, Contact


tokens.default_token_manager(
    client_id="8339a558-e86f-4b11-9524-bbec6daef36c",
    client_secret="KIec2F1rwD6e5EMldCKPBDwcOZVmXGKEgC2XRofH9eA7BFR1ZRpGb3zLAI7B2pBp",
    subdomain="dipetr94",
    redirect_url="https://test.kz",
    storage=tokens.FileTokensStorage(),  # by default FileTokensStorage
)
# tokens.default_token_manager.init(code="def50200384665043c1a0bfe0982780608ba95f749de81922306c4da53d299cb8c8e1f4f7e29f3e0c26321afce1286385a2689cd089b90cca1632700cb0a65b73cd0f158a54c95f8066d3337463d4414e70a0a8cc049e6f1528e47fe30cc9b30831aaa582c6907ff35313d43c5783578ca8b726c16f9886e8d9ca813ee63c3e4e5a0ea9389dbe314387e863d86d756eff04b3335a492dda74d58bd105843b701f28c8460574b6e68a35318532a6e7dd8a814decba103138255957d59db86a3941e786f0c465202297612bac3af3ff76e2fb72ffa447f7cc758a2a9f072cc3b3d8426e880c8683a50b940d3128fc717d3f2af12577b8457f735a0f4e3adfaff2ea6d9e4c2c42416a4e64ce9ed9e5451c52fb28f6ebd80aadbd36c2452719c9b6c3b7f0345d623a3a5c88f0b70c099ccb78e3fd25a2f3b5e96e26afd4be454461448ede5fcd5d2a6681f9a7440fa1afc53db6e7eb799a66bcbebe70349c0511e46c61dd06917949d634a2b03b94a35eab9a86d4391fb7d663af27d461e7e4b1cdc2849ebf6337e4dd23de560463fdae9b973bee24a6d620e2fea2eecc426bbcd6acc58cdd60a2f32b7ac50925be1bc43e97283f69582739ee6ab5e0465666aeec0fc11371001cb646daeecf412196954aaf43efb931c2fbc357f64c5421d11b9", skip_error=False)

# # Функция для создания контакта
# def create_contact(name, email, phone,miner,language, electr, cur):

#     custom_fields = [
#         {"id": "1725947", "values": [{"value": miner}]},  # Замените "ID_поля_Майнер" на фактический идентификатор поля
#         {"id": "1725953", "values": [{"value": language}]},  # Замените "ID_поля_Язык" на фактический идентификатор поля
#         {"id": "1725955", "values": [{"value": electr}]},
#         {"id": "1725963", "values": [{"value": cur}]},
#     ]

#     contact = Contact()
#     contact.name = name
#     contact.email = email
#     contact.phone = phone
#     contact.custom_fields = custom_fields
#     contact.save()
#     return contact

# Функция для создания лида без связи с контактом
def create_lead_without_contact(title, amount, currency):
    lead_data = {
        "name": title,
        "sale": amount,
        "currency": currency,
    }

    lead = Lead.create(lead_data)
    return lead

# Пример использования
if __name__ == "__main__":
    lead_title = "Новая сделка"
    lead_amount = 1000
    lead_currency = "USD"

    # Создание лида без связи с контактом
    new_lead = create_lead_without_contact(lead_title, lead_amount, lead_currency)

    print(f"Создан лид с ID: {new_lead.id}")
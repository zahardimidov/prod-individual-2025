

def advertisers():
    return [
        {
            "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa1",
            "name": "Advertiser1"
        },
        {
            "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa2",
            "name": "Advertiser2"
        },
        {
            "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa3",
            "name": "Advertiser3"
        },
        {
            "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa4",
            "name": "Advertiser4"
        },
        {
            "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa5",
            "name": "Advertiser5"
        },
        {
            "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "name": "Advertiser6"
        },
        {
            "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "name": "Advertiser7"
        },
        {
            "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
            "name": "Advertiser8"
        },
        {
            "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
            "name": "Advertiser9"
        },
        {
            "advertiser_id": "3fa85f64-5717-4562-b3fc-2c963f66afa10",
            "name": "Advertiser10"
        }
    ]


def clients():
    return [
        {
            "client_id": "3fa85f64-5717-4562-b3fc-2c963f66af1",
            "login": "Client1",
            "age": 50,
            "location": "Moscow",
            "gender": "MALE"
        },
        {
            "client_id": "3fa85f64-5717-4562-b3fc-2c963f66af2",
            "login": "Client2",
            "age": 18,
            "location": "Moscow",
            "gender": "FEMALE"
        },
        {
            "client_id": "3fa85f64-5717-4562-b3fc-2c963f66af3",
            "login": "Client3",
            "age": 70,
            "location": "Moscow",
            "gender": "MALE"
        },
        {
            "client_id": "3fa85f64-5717-4562-b3fc-2c963f66af4",
            "login": "Client4",
            "age": 40,
            "location": "Moscow",
            "gender": "MALE"
        },
        {
            "client_id": "3fa85f64-5717-4562-b3fc-2c963f66af5",
            "login": "Client5",
            "age": 25,
            "location": "Saint Petersburg",
            "gender": "FEMALE"
        },
        {
            "client_id": "3fa85f64-5717-4562-b3fc-2c963f66af6",
            "login": "Client6",
            "age": 32,
            "location": "Novosibirsk",
            "gender": "MALE"
        },
        {
            "client_id": "3fa85f64-5717-4562-b3fc-2c963f66af7",
            "login": "Client7",
            "age": 45,
            "location": "Yekaterinburg",
            "gender": "FEMALE"
        },
        {
            "client_id": "3fa85f64-5717-4562-b3fc-2c963f66af8",
            "login": "Client8",
            "age": 29,
            "location": "Kazan",
            "gender": "MALE"
        },
        {
            "client_id": "3fa85f64-5717-4562-b3fc-2c963f66af9",
            "login": "Client9",
            "age": 60,
            "location": "Nizhny Novgorod",
            "gender": "FEMALE"
        },
        {
            "client_id": "3fa85f64-5717-4562-b3fc-2c963f66afa",
            "login": "Client10",
            "age": 35,
            "location": "Chelyabinsk",
            "gender": "MALE"
        }
    ]


def campaigns():
    return [
        {
            "impressions_limit": 100,
            "clicks_limit": 50,
            "cost_per_impression": 1,
            "cost_per_click": 10,
            "ad_title": "Summer Sale",
            "ad_text": "Get up to 50% off on summer clothing!",
            "start_date": 1,
            "end_date": 30,
            "targeting": {
                "gender": "ALL",
                "age_from": 18,
                "age_to": 65,
                "location": "Worldwide"
            }
        },
        {
            "impressions_limit": 200,
            "clicks_limit": 100,
            "cost_per_impression": 2,
            "cost_per_click": 15,
            "ad_title": "New Laptop Launch",
            "ad_text": "Check out the latest features of our new laptop!",
            "start_date": 5,
            "end_date": 20,
            "targeting": {
                "gender": "MALE",
                "location": "Moscow"
            }
        },
        {
            "impressions_limit": 150,
            "clicks_limit": 75,
            "cost_per_impression": 1.5,
            "cost_per_click": 12,
            "ad_title": "Healthy Snacks",
            "ad_text": "Try our new range of healthy snacks!",
            "start_date": 10,
            "end_date": 25,
            "targeting": {
                "gender": "FEMALE",
                "age_from": 18,
                "age_to": 50,
                "location": "Saint Petersburg"
            }
        },
        {
            "impressions_limit": 300,
            "clicks_limit": 150,
            "cost_per_impression": 0.5,
            "cost_per_click": 8,
            "ad_title": "Fitness Program",
            "ad_text": "Join our fitness program and get fit this summer!",
            "start_date": 15,
            "end_date": 45,
            "targeting": {
                "gender": "ALL",
                "age_from": 16,
                "age_to": 60,
                "location": "Kazan"
            }
        },
        {
            "impressions_limit": 250,
            "clicks_limit": 125,
            "cost_per_impression": 1.2,
            "cost_per_click": 9,
            "ad_title": "Travel Deals",
            "ad_text": "Explore the world with our exclusive travel deals!",
            "start_date": 20,
            "end_date": 50,
            "targeting": {
                "gender": "ALL",
                "age_from": 25,
                "age_to": 65,
                "location": "Novosibirsk"
            }
        },
        {
            "impressions_limit": 80,
            "clicks_limit": 40,
            "cost_per_impression": 3,
            "cost_per_click": 20,
            "ad_title": "Luxury Watch Sale",
            "ad_text": "Limited time offer on luxury watches!",
            "start_date": 1,
            "end_date": 10,
            "targeting": {
                "gender": "MALE",
                "age_from": 30,
                "age_to": 55,
                "location": "Yekaterinburg"
            }
        },
        {
            "impressions_limit": 120,
            "clicks_limit": 60,
            "cost_per_impression": 2.5,
            "cost_per_click": 18,
            "ad_title": "Online Courses",
            "ad_text": "Enhance your skills with our online courses!",
            "start_date": 5,
            "end_date": 35,
            "targeting": {
                "gender": "FEMALE",
                "age_from": 22,
                "age_to": 45
            }
        },
        {
            "impressions_limit": 90,
            "clicks_limit": 45,
            "cost_per_impression": 1.8,
            "cost_per_click": 14,
            "ad_title": "Eco-Friendly Products",
            "ad_text": "Join the green movement with our eco-friendly products!",
            "start_date": 10,
            "end_date": 40,
            "targeting": {
                "gender": "ALL",
                "age_from": 18,
                "age_to": 60,
            }
        },
        {
            "impressions_limit": 75,
            "clicks_limit": 30,
            "cost_per_impression": 2.2,
            "cost_per_click": 16,
            "ad_title": "Gourmet Coffee Subscription",
            "ad_text": "Get gourmet coffee delivered to your door monthly!",
            "start_date": 3,
            "end_date": 33,
            "targeting": {
                "age_from": 20,
                "age_to": 50
            }
        },
        {
            "impressions_limit": 60,
            "clicks_limit": 25,
            "cost_per_impression": 4,
            "cost_per_click": 25,
            "ad_title": "Exclusive Fashion Collection",
            "ad_text": "Shop our exclusive fashion collection before it's gone!",
            "start_date": 15,
            "end_date": 30
        }
    ]
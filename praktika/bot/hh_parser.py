import requests

# Функция для парсинга вакансий
def fetch(vacancy_title, 
          region,
          salary=None, 
          experience=None, 
          employment=None, 
          schedule=None, 
          count=6 
          ):
    url = "https://api.hh.ru/vacancies"
    vacancies = []
    page = 0
    per_page = 50 
    # Преобразование параметров фильтра
    maps = {
        'experience': {
            'Нет значений': None,
            'Без опыта': 'noExperience',
            'От 1 года до 3 лет': 'between1And3',
            'От 3 до 6 лет': 'between3And6',
            'Более 6 лет': 'moreThan6',
        },
        'employment': {
            'Полная занятость': 'full',
            'Частичная занятость': 'part',
            'Стажировка': 'probation',
        },
        'schedule': {
            'Полный день': 'fullDay',
            'Сменный график': 'shift',
            'Гибкий график': 'flexible',
            'Удаленная работа': 'remote',
        }
    }

    while len(vacancies) < count:
        params = {
            'text': vacancy_title,
            'area': region,
            'per_page': per_page,
            'page': page,
            'salary_from': salary[0] if salary else None,
            'salary_to': salary[1] if salary else None,
            'experience': maps['experience'].get(experience),
            'employment': maps['employment'].get(employment),
            'schedule': maps['schedule'].get(schedule)
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
        if not data['items']:
            break
        for item in data['items']:
            if vacancy_title.lower() in item['name'].lower():
                vacancies.append({
                    'name': item['name'],
                    'area': item['area']['name'],
                    'salary': item.get('salary'),
                    'experience': item['experience']['name'],
                    'employment': item['employment']['name'],
                    'schedule': item.get('schedule', {}).get('name', '')
                })
                if len(vacancies) >= count:
                    break
        page += 1

    return vacancies[:count]

try:
    import requests as _requests
except Exception as e:
     ImportError('Exception was raised when importing requests module. Requests dependency are installed ??')


def get_item(_id):
    '''
        Get a hackers news item by id.
    '''
    return _requests.get('https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(_id)).json()

def get_job_stories(n=10):
    '''
        Get the n firsted jobs. n default is 10.
    '''

    jobs_ids = _requests.get('https://hacker-news.firebaseio.com/v0/jobstories.json?print=pretty').json()



    jobs = []

    for i in jobs_ids[0:n]:
        item = get_item(i)

        jobs.append(item)
    
    return jobs



def get_top_stories(n=10):
    '''
        Get the n firsted top best stories. n default is 10.
    '''
    stories_ids = _requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty').json()

    stories = []

    for i in stories_ids[0:n]:
        item = get_item(i)

        # delleting kids from actual storie
        del item['kids']

        stories.append(item)
    
    return stories


if __name__ == '__main__':
    print(get_top_stories(1))
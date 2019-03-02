
import requests

# downloading bank from repository: https://github.com/oseparovic/fodmap_list
def downloadDatabase(localFilePath):
    url = "https://raw.githubusercontent.com/oseparovic/fodmap_list/master/fodmap_repo.json"
    database = requests.get(url).text
    with open(localFilePath, 'w') as File:
        File.write(database)

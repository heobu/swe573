import requests 
  
def get_wikidata(title):
  wikidata_url = "https://www.wikidata.org/w/api.php"
  token = {'action':'wbgetentities', 'sites':'enwiki', 'titles':title, 'props':'descriptions', 'languages':'en', 'format':'json'}

  result = requests.get(wikidata_url, token)
  json = result.json()

  if json["success"] == 1:
    print("Entry '", title , "' was found.")

  return json

def main():
    
  title = "Munich"
  json1 = get_wikidata(title)
    
  title = "Nikola_Tesla"
  json2 = get_wikidata(title)
    
  title = "Formula_One"
  json3 = get_wikidata(title)

  print(json1)
  print(json2)
  print(json3)

if __name__ == "__main__":
    main()

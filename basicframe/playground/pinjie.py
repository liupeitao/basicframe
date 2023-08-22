base_urls = [
    "https://www.tribalfootball.com/leagues/english-premier-league",
    "https://www.tribalfootball.com/leagues/spanish-liga",
    "https://www.tribalfootball.com/leagues/italian-serie-a",
    "https://www.tribalfootball.com/leagues/a-league",
    "https://www.tribalfootball.com/leagues/english-championship",
    "https://www.tribalfootball.com/leagues/argentine-primera-division",
    "https://www.tribalfootball.com/leagues/campeonato-brasileiro-serie-a",
    "https://www.tribalfootball.com/leagues/mls",
    "https://www.tribalfootball.com/leagues/eredivisie",
    "https://www.tribalfootball.com/leagues/j-league",
    "https://www.tribalfootball.com/leagues/ligue-1"
]

page_numbers = [
    15438, 2980, 3057, 233, 2972, 26, 119, 49, 290, 24, 502
]


with open('../assets/tripage.txt', mode='w') as f :
    for base_url, page_number in zip(base_urls, page_numbers):
        for i in range(1, page_number+1):
            url = f"{base_url}?page={i}"
            f.write(url + '\n')

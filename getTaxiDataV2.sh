cat urls.txt | xargs -n 1 -P 6 wget -P data/ &

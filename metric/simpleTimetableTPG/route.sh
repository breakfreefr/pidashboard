curl -s "https://transport.opendata.ch/v1/connections?from=Pr%C3%A9vessin%2C%20Prenepla&to=Gen%C3%A8ve&limit=3" \
| jq -r '
.connections[]
| (.from.departure | split("+")[0]) as $raw
| ($raw | strptime("%Y-%m-%dT%H:%M:%S") | mktime) as $dep
| (($dep - now) / 60 | floor - 60 ) as $m
| select($m >= 0)
| ( .sections[0].journey.number // .products[0] 
    | gsub("Bus "; "") ) as $line
| ($raw | strptime("%Y-%m-%dT%H:%M:%S") | strftime("%H:%M")) as $time
| "\($line) \($time) \($m)m"
'

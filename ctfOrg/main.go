package main

import (
	"encoding/csv"
	"log"
	"net/http"
	"os"

	"golang.org/x/net/html"
)

func main() {
	client := http.Client{}

	req, err := http.NewRequest("GET", "https://ctftime.org/event/list/upcoming", nil)
	if err != nil {
		log.Fatal(err)
	}

	req.Header.Set("User-Agent",
		"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")

	resp, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	doc, err := html.Parse(resp.Body)
	if err != nil {
		log.Fatal(err)
	}

	records := [][]string{
		{"Name", "Date", "Format", "Location", "Weight", "Notes"},
	}

	for n := range doc.Descendants() {
		if n.Type == html.ElementNode && n.Data == "tr" {
			record := []string{}
			for k := range n.Descendants() {
				if k.Type == html.TextNode && (k.Parent.Data == "td" || k.Parent.Data == "a") {
					record = append(record, k.Data)
				}
			}
			records = append(records, record)
		}
	}

	rec, err := os.OpenFile("rec.csv", os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatal(err)
	}

	w := csv.NewWriter(rec)
	for _, reco := range records {
		if err := w.Write(reco); err != nil {
			log.Fatal(err)
		}
	}
	w.Flush()
	if err := w.Error(); err != nil {
		log.Fatal(err)
	}

}

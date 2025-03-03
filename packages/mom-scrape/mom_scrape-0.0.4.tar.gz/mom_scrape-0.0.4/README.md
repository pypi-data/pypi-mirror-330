# `mom_scrape`

example usage:

```
from mom_scrape.scrapers import ReportScraper, WebScraper

reportscraper=ReportScraper(filter_by='Reports',save_dir='stats/reports')
results=reportscraper.get_info()
```

This first creates a `dates` folder then dump the dates of the various repoerts in the `mom_reports.json` file. Then, the new PDFs (these are PDFs that are not already recorded in `mom_reports.json` file) are downloaded under save_dir
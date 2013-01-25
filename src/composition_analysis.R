# Libraries
library(entropy)
library(gridExtra)
library(scales)
library(ggplot2)
library(plyr)

# Import Datasets
gnews_monthly <- read.csv("~/attention/gnews_monthly-4-21.csv")
df <- data.frame(gnews_monthly)
df <- subset(df, orig_lang == "en")

# Helper Methods

# Finding the media attention core
modified.jaccard <- function(a, b) {
  intersect(a, b)
}

arrange(df, desc(num_results))


df$date <- mdy(df$date)
a.date <- mdy('1/1/07')
a.vec <- arrange(subset(df, date == a.date), desc(num_results))$dest_country

for (i in 1:length(unique(df$date_period))) {
  b.date <- mdy('1/1/07') + months(i)
  b.vec <- arrange(subset(df, date == b.date), desc(num_results))$dest_country
  print(modified.jaccard(a.vec, b.vec))
}

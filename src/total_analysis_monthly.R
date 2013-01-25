# Libraries
library(entropy)
library(gridExtra)
library(scales)
library(ggplot2)
library(plyr)
library(lubridate)

# Import Datasets
gnews_monthly <- read.csv("~/attention/gnews_monthly_us_mx_cn_2012-04-21_augmented.csv")
df <- data.frame(gnews_monthly)

# Helper Methods
ent <- function(df) {  # Entropy from observed counts
  v <- df$num_results
  freqs <- v / sum(v)
  -sum(ifelse(freqs > 0, freqs * log(freqs), 0))
}

exp_ent <- function(df) { exp(ent(df$num_results)) }

stacked_area_plot <- function(df) {
  ggplot(df, aes(x=date, y=num_results)) +
  geom_area(aes(fill=dest_country), position='stack') +
  scale_x_datetime(labels = date_format("%m/%y"), breaks =
  date_breaks("3 months")) +
  scale_y_continuous(labels=function(x) format(x, width = 12)) +
  labs(x="Date Period", y="Number of Results") +
  theme_bw() +
  theme(legend.position="none", axis.text.x = element_text(angle=-90, hjust = 0))
  }

ent_area_plot <- function(df) {
  ggplot(df, aes(x=date, y=ent)) +
  geom_area(position='stack') +
  scale_x_datetime(labels = date_format("%m/%y"), breaks = date_breaks("3 months")) +
  scale_y_continuous(labels=function(x) format(x, width = 16)) +
  theme_bw() +
  theme(axis.text.x = element_text(angle=-90, hjust=0)) +
  labs(x="Date Period", y="Entropy")
}

exp_ent_area_plot <- function(df) {
  ggplot(df, aes(x=date, y=exp_ent)) +
  geom_area(position='stack') +
  scale_x_datetime(labels = date_format("%m/%y"), breaks =
  date_breaks("3 months")) +
  scale_y_continuous(labels=function(x) format(x, width = 16)) +
  theme_bw() +
  theme(axis.text.x = element_text(angle=-90, hjust=0)) +
  labs(x="Date Period", y="exp(Entropy)")
}

sort_subset <- function(df, ordered_df=123) {
  country_order <- ordered_df$dest_country
  count_order_vector <- as.character(country_order)
  df[match(count_order_vector, df$dest_country),]
}

totally_order_df <- function(df) {
  df_2007 <- subset(df, date == mdy('1/1/07'))
  ordered_df <- arrange(df_2007, desc(num_results))
  ddply(df, .(date), sort_subset, ordered_df)
}

total_plot <- function(df) {
  df$date <- mdy(df$date_period)
  ordered_df <- totally_order_df(df)
  df_entropies <- ddply(df, .(date), c("ent", "exp_ent"))
  p1 <- stacked_area_plot(ordered_df)
  p2 <- ent_area_plot(df_entropies)
  p3 <- exp_ent_area_plot(df_entropies)
  grid.arrange(p1, p2, p3, nrow=3, main=paste(
  toString(df$orig_lang[1]), "Language Edition Monthly Results", sep=" "))
}

# Plot creation
postscript("area_plots_ordered_legend_monthly.eps", horizontal = FALSE, onefile = TRUE, width = 8, height = 9.5)
tryCatch(d_ply(df, .(orig_country), failwith(NA, total_plot), .print = TRUE))
dev.off()

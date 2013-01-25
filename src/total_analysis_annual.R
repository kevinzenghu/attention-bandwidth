# Libraries
library(entropy)
library(gridExtra)
library(scales)
library(ggplot2)
library(plyr)

# Import Datasets
gnews_monthly <- read.csv("~/attention/gnews_monthly-4-21.csv")
# gnews_annual <- read.csv("~/attention/gnews_time_annual_all_fixed.csv")
df <- data.frame(gnews_monthly)

# Helper Methods
ent <- function(df) { entropy.Dirichlet(df$num_results) }
exp_ent <- function(df) { exp(entropy.Dirichlet(df$num_results)) }

stacked_area_plot <- function(df) {
  ggplot(df, aes(x=date_period, y=num_results)) +
  geom_area(aes(fill=dest_country), position='stack') +
  scale_x_continuous(breaks=2005:2012) +
  scale_y_continuous(labels=function(x) format(x, width = 12)) +
  labs(x="Date Period", y="Number of Results") +
  theme_bw() +
  theme(legend.position="none")
  }

ent_area_plot <- function(df) {
  ggplot(df, aes(x=date_period, y=ent)) +
  geom_area(position='stack') +
  scale_x_continuous(breaks=2005:2012) +
  scale_y_continuous(labels=function(x) format(x, width = 16)) +
  theme_bw() +
  labs(x="Date Period", y="Entropy")
}

exp_ent_area_plot <- function(df) {
  ggplot(df, aes(x=date_period, y=exp_ent)) +
  geom_area(position='stack') +
  scale_x_continuous(breaks=2005:2012) +
  scale_y_continuous(labels=function(x) format(x, width = 16)) +
  theme_bw() +
  labs(x="Date Period", y="exp(Entropy)")
}

sort_subset <- function(df, ordered_df=123) {
  country_order <- ordered_df$dest_country
  count_order_vector <- as.character(country_order)
  df[match(count_order_vector, df$dest_country),]
}

totally_order_df <- function(df) {
  df_2012 <- subset(df, date_period == 2012)
  ordered_df <- arrange(df_2012, desc(num_results))
  ddply(df, .(date_period), sort_subset, ordered_df)
}

total_plot <- function(df) {
  ordered_df <- totally_order_df(df)
  df_entropies <- ddply(df, .(date_period), c("ent", "exp_ent"))
  p1 <- stacked_area_plot(ordered_df)
  p2 <- ent_area_plot(df_entropies)
  p3 <- exp_ent_area_plot(df_entropies)
  grid.arrange(p1, p2, p3, nrow=3, main=paste(toString(df$orig_lang[1]), "Language Edition Annual Results", sep=" "))
}

# Plot creation
postscript("area_plots_ordered_legend_monthly_1-16-2013.eps", horizontal = FALSE, onefile = TRUE, width = 8, height = 9.5)
d_ply(df, .(orig_country), failwith(NA, total_plot), .print = TRUE)
dev.off()

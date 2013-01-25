library('rjson')

df <- gnews_monthly_us_mx_cn_2012.04.21_augmented
df.en <- subset(df, orig_lang == 'en')


generate_ranks <- function(df) {
  df.ordered <- arrange(df, order=desc(num_results))
  df.ordered$rank <- 1 : nrow(df.ordered)
  return(df.ordered)
}

ranked.df <- ddply(df, .(date_period), generate_ranks)
dates <- unique(df$date_period)

library(gridExtra)

nx <- function(v, x) {
  v <- sort(v, decreasing=TRUE)
  cutoff <- x * sum(v)
  total <- 0
  for (i in 1:length(v)) {
    total = total + v[i]
    if (total >= cutoff) return (i)
  }
}


nx.stacked.area.plot <- function(df) {
  ggplot(df, aes(x))
}

postscript("nx_plots_annual.eps", horizontal = FALSE, onefile = TRUE, width = 8, height = 9.5)
par(mfrow=c(5, 2))
for (x in seq(from=0, to=1, by=0.1)) {
  d_ply(df, .(orig_), failwith(NA, total_plot), .print = TRUE)
}
dev.off()

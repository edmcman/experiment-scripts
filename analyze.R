#!/usr/bin/Rscript
# Example R script

library(ggplot2)
library(reshape)
library(plyr)
library(grid)
require(RCurl)

theme_set(theme_bw())
pointsize=2

## Read in data

if (!exists("d")) {

  print("Downloading...");

  d <- read.csv(textConnection(getURL("https://docs.google.com/spreadsheet/pub?key=0Au4zXzOoce8JdGFjZ0JBVTIxRmgzeEpZN0VFRVktb0E&single=true&gid=3&output=csv")), na.strings = c("-1"))

  d$name <- factor(d$name, levels=c("ed", "thanassis"))

  print("Factorizing")

  md = melt(d, measure.vars=c("time"))

}

print("Downloaded csv data");

g = qplot(name, time, data=d, geom="boxplot", xlab="Name", ylab="Time (seconds)")
ggsave(file = "box.pdf", width=6.6, height=2.2, scale=1.5)

g = qplot(time, data=d, fill = name)
ggsave(file = "hist.pdf", width=6.6, height=2.2, scale=1.5)

# Stats
numsamples = nrow(d)

edmean = round(mean(d[d$name == "ed",]$time), digits=2)
thanassismean = round(mean(d[d$name == "thanassis",]$time), digits=2)

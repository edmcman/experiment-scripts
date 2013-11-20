#!/usr/bin/Rscript
# Example R script to analyze fake typing time data.  The mean times
# for both words are computed.  Two figures are also produced.

library(ggplot2)
library(reshape)
library(plyr)
library(grid)
require(RCurl)

theme_set(theme_bw())
theme_slides <- theme_bw(base_size = 28) +
                theme(axis.title.x = element_text(vjust = -1),
                      axis.title.y = element_text(vjust = 0.35),
                      plot.margin = unit(c(.5, .5, 1, .5), "cm"),
                      legend.text = element_text(size = 18))

## From http://www.cookbook-r.com/Manipulating_data/Summarizing_data/#using-summaryby
## Summarizes data.
## Gives count, mean, standard deviation, standard error of the mean, and confidence interval (default 95%).
##   data: a data frame.
##   measurevar: the name of a column that contains the variable to be summariezed
##   groupvars: a vector containing names of columns that contain grouping variables
##   na.rm: a boolean that indicates whether to ignore NA's
##   conf.interval: the percent range of the confidence interval (default is 95%)
summarySE <- function(data=NULL, measurevar, groupvars=NULL, na.rm=FALSE,
                      conf.interval=.95, .drop=TRUE) {
    require(plyr)

    # New version of length which can handle NA's: if na.rm==T, don't count them
    length2 <- function (x, na.rm=FALSE) {
        if (na.rm) sum(!is.na(x))
        else       length(x)
    }

    # This does the summary. For each group's data frame, return a vector with
    # N, mean, and sd
    datac <- ddply(data, groupvars, .drop=.drop,
      .fun = function(xx, col) {
        c(N    = length2(xx[[col]], na.rm=na.rm),
          mean = mean   (xx[[col]], na.rm=na.rm),
          sd   = sd     (xx[[col]], na.rm=na.rm)
        )
      },
      measurevar
    )

    # Rename the "mean" column    
    datac <- rename(datac, c("mean" = measurevar))

    datac$se <- datac$sd / sqrt(datac$N)  # Calculate standard error of the mean

    # Confidence interval multiplier for standard error
    # Calculate t-statistic for confidence interval: 
    # e.g., if conf.interval is .95, use .975 (above/below), and use df=N-1
    ciMult <- qt(conf.interval/2 + .5, datac$N-1)
    datac$ci <- datac$se * ciMult

    return(datac)
}

## Read in data

if (!exists("d")) {

  print("Downloading...");

  d <- read.csv(textConnection(getURL("https://docs.google.com/spreadsheet/pub?key=0Au4zXzOoce8JdGFjZ0JBVTIxRmgzeEpZN0VFRVktb0E&single=true&gid=3&output=csv")), na.strings = c("-1"))

  d$name <- factor(d$name, levels=c("ed", "thanassis"))

  print("Factorizing")

  md = melt(d, measure.vars=c("time"))

}

print("Downloaded csv data");

dsummary <- summarySE(d, "time", c("name"))

g = qplot(name, time, data=d, geom="boxplot", xlab="Name", ylab="Time (seconds)")
ggsave(file = "box.pdf", width=6.6, height=2.2, scale=1.5)

g = qplot(time, data=d, fill = name)
ggsave(file = "hist.pdf", width=6.6, height=2.2, scale=1.5)

g = qplot(name, time, geom=c("bar"), fill=name, data=dsummary) + geom_errorbar(aes(ymin=time-ci, ymax=time+ci))
ggsave(file = "histsummary.pdf", width=3.16, height=1.75, scale=1.5)

g + theme_slides
ggsave(file = "histsummary-slides.pdf", width=11.5, height=7.5, scale=0.9)
ggsave(file = "histsummary-slides.svg", width=11.5, height=7.5, scale=0.9)

# Stats
numsamples = nrow(d)

edmean = round(mean(d[d$name == "ed",]$time), digits=2)
thanassismean = round(mean(d[d$name == "thanassis",]$time), digits=2)

### Criando Gráfcos com plot()

### Limpando Plots, Console and Ambiente
rm(list = ls())
dev.off(dev.list()["RStudioGD"])
cat("\014")

# Creating a Graph
attach(mtcars)

names(mtcars) # variables
str(mtcars) # information
head(mtcars, n=10) # header
tail(mtcars, n=5) # ender

plot(wt, mpg)
abline(lm(mpg~wt))
title("Regression of MPG on Weight")

# Simple Histogram
hist(mtcars$mpg)

# Colored Histogram with Different Number of Bins
hist(mtcars$mpg, breaks=12, col="red") 

# Add a Normal Curve (Thanks to Peter Dalgaard)
x <- mtcars$mpg
h<-hist(x, breaks=10, col="red", xlab="Miles Per Gallon",
        main="Histogram with Normal Curve")
xfit<-seq(min(x),max(x),length=40)
yfit<-dnorm(xfit,mean=mean(x),sd=sd(x))
yfit <- yfit*diff(h$mids[1:2])*length(x)
lines(xfit, yfit, col="blue", lwd=2) 

# Kernel Density Plot
d <- density(mtcars$mpg) # returns the density data
plot(d) # plots the results 

# Filled Density Plot
d <- density(mtcars$mpg)
plot(d, main="Kernel Density of Miles Per Gallon")
polygon(d, col="red", border="blue") 

# Compare MPG distributions for cars with
# 4,6, or 8 cylinders
library(sm)
attach(mtcars)

### Limpando Plots, Console and Ambiente
rm(list = ls())
dev.off(dev.list()["RStudioGD"])
cat("\014")

# create value labels
cyl.f <- factor(cyl, levels= c(4,6,8),
                labels = c("4 cylinder", "6 cylinder", "8 cylinder"))

# plot densities
sm.density.compare(mpg, cyl, xlab="Miles Per Gallon")
title(main="MPG Distribution by Car Cylinders")

# add legend via mouse click
colfill<-c(2:(2+length(levels(cyl.f))))
#legend(locator(1), levels(cyl.f), fill=colfill) 


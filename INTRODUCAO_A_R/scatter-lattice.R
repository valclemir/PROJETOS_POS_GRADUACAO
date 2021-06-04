### Criando Gráfcos com plot()

### Limpando Plots, Console and Ambiente
rm(list = ls())
dev.off(dev.list()["RStudioGD"])
cat("\014")

#install.packages("car")
#install.packages("scatterplot3d")

# Simple Scatterplot
attach(mtcars)

plot(wt, mpg, main="Scatterplot Example",
     xlab="Car Weight ", ylab="Miles Per Gallon ", pch=19) 

# Add fit lines
abline(lm(mpg~wt), col="red") # regression line (y~x)
lines(lowess(wt,mpg), col="blue") # lowess line (x,y) 

# Basic Scatterplot Matrix
pairs(~mpg+disp+drat+wt,data=mtcars,
      main="Simple Scatterplot Matrix")

# 3D Scatterplot with Coloring and Vertical Drop Lines
library(scatterplot3d)
#attach(mtcars)
scatterplot3d(wt,disp,mpg, pch=16, highlight.3d=TRUE,
              type="h", main="3D Scatterplot") 


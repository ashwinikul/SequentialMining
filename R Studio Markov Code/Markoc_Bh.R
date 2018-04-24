# Created By
# (Ashwini Kulkarni, Ningle Lei )
# Program to plot markov chain diagram for sequence data
# Data Mining Project


library(clickstream)
library(arulesSequences)
library(ggplot2)

clickstreams1 <- readClickstreams(file = "C:/Python/DataMining/Proccessed.txt", sep = " ", header = F)
print(clickstreams1)
print(clickstreams1[4])
print(clickstreams1[5])


mc <- fitMarkovChain(clickstreams1)
startPattern <- new("Pattern", sequence = c("a"))
predict(mc, startPattern)
plot(mc)

# Load modules
library(nlme)
library(lmtest)

# Load data
data_dir <- 'C:/Users/eerou/Desktop/opinnot/tutkielma/analyysi/data/data_points/'
data <- 'data_points_strIDs_blocknrs.csv'
path <- paste(
    data_dir,
    data,
    sep=''
    )
data_points <- read.table(
    path,
    header=TRUE,
    sep=','
    )
attach(data_points)

# Model using GLS
model <- gls(
    Mean.Reaction.Time ~ Block.Number,
    data=data_points,
    correlation=corCompSymm(
        0.5,
        form=~1|ID
        )
    )

# Summarize the model
summary(model)

# Perform the Wald test on the model
waldtest(model)

# Fit and summarize the autoregressive variant
model.ar <- gls(
    Mean.Reaction.Time ~ Block.Number,
    data=data_points,
    correlation=corAR1(
        0.5,
        form=~1|ID
        )
    )
summary(model.ar)

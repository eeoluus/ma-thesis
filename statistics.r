# Load modules
library(ggplot2)
library(nlme)
library(lmtest)

# Load data
data_dir <- 'C:/Users/eerou/Desktop/analyysi/data/data_points/'
data <- 'data_points.csv'
path <- paste(
    data_dir, 
    data, 
    sep=''
    )
data_points<- read.table(
    path, 
    header=TRUE,
    sep=','
    )
attach(data_points)

# Model using GLS
model <- gls(
    Mean.Reaction.Time ~ N400.Mean.Difference,
    data=data_points,
    correlation=corCompSymm(
        0.5,
        form=~1|ID
        ) 
    )

# Set up values to calculate confidence intervals from
des <- model.matrix(
    formula(model)[-2], 
    data_points
    )
predvar <- diag(des %*% vcov(model) %*% t(des))

# Extract predicted values and confidence intervals
data_points$predgls <- predict(model)
data_points$lower <- with(
    data_points, 
    predgls - 1.96*sqrt(predvar) 
    )
data_points$upper <- with(
    data_points, 
    predgls + 1.96*sqrt(predvar) 
    )

# Summarize the model
summary(model)

# Perform the Wald test on the model
waldtest(model)

# Plot the data, the model and the confidence intervals
theme_set(theme_bw())
ggplot(
    data_points, 
    aes(
        N400.Mean.Difference, 
        Mean.Reaction.Time
        ) 
    ) +
    geom_point() +
    geom_line(
            aes(y=predgls), 
            color='blue', 
            size=1
            ) +
    geom_ribbon(
        data=data_points, 
        aes(
            y=NULL, 
            ymin=lower, 
            ymax=upper, 
            color=NULL, 
            ),
        alpha=.15,
        fill='blue'
        ) +
    labs(
        x='N400 Mean Difference (fT/m)',
        y='Mean Reaction Time (ms)',
        title='Generalized Least Squares Model'
        ) +
    scale_x_continuous(labels=function(x)x*10^15) +
    theme(plot.title=element_text(
            hjust=0.5,
            vjust=2.5
            )
        )

# Uncomment to save figure                       
#ggsave(
 #   'path/figurename.png', 
  #  dpi=300
   # )

# Sanity check the confidence intervals
confidence = intervals(
    model, 
    0.95, 
    'coef'
    )
head(confidence)
                                              
# Fit and summarize the autoregressive variant
model.ar <- gls(
    Mean.Reaction.Time ~ N400.Mean.Difference,
    data=data_points,
    correlation=corAR1(
        0.5,
        form=~1|ID
        )
    )
summary(model.ar)

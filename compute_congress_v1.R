setwd("C:/Users/mahon")


# Load objects

library(distrom)
library(Matrix)

data<-read.csv("Trigram_Counts_congress_2016_2021_v3.csv")
n=length(data[1,])
zero_index=which(rowSums(data[,5:n])==0)

data=data[-zero_index,]
data=data[,-1]
speaker_metadata<-data[,1:3]
colnames(speaker_metadata)=c("Speaker","Date","Party")

write.csv(speaker_metadata,"Speaker_metadata_congress.csv")

rownames(data)=speaker_metadata$id
data=data[,-c(1,2,3)]

#####DIAGONOSTICS#######

#idx=which(speaker_metadata$Speaker=='Fox Staff')
#data=data[-idx,]
#speaker_metadata=speaker_metadata[-idx,]


#idx=which(speaker_metadata$Speaker=='CNN Staff')
#data=data[-idx,]
#speaker_metadata=speaker_metadata[-idx,]


#idx=which(speaker_metadata$Date=='2015-03')
#data_diag=data[idx,]
#rm_idx=which(as.vector(rowSums(data_diag))>500)

#speaker_metadata_diag=speaker_metadata[idx,]

#data=data[-idx,]
#speaker_metadata=speaker_metadata[-idx,]

#data_diag=data_diag[-rm_idx,]
#speaker_metadata_diag=speaker_metadata_diag[-rm_idx,]

#speaker_metadata=rbind(speaker_metadata,speaker_metadata_diag)
#data=rbind(data,data_diag)

#zero_index=which(rowSums(data)==0)


#########################

for(i in 1:length(data[1,])){data[,i]=as.integer(data[,i])} 
data = Matrix(as.matrix(data),sparse=TRUE )
data[which(data<0)]=-data[which(data<0)]

speaker_metadata$Party[speaker_metadata$Party=="\"Republican\""]=1
speaker_metadata$Party[speaker_metadata$Party=="\"Democrat\""]=0
speaker_metadata$Party=as.numeric(speaker_metadata$Party)

years=speaker_metadata$Date
years=substr(years,1,4)

#elect_index=which(years=="2012"|years=="2016"|years=="2020")
rep_pres_index=which(years=="2017"|years=="2018"|years=="2019"|years=="2020")

speaker_metadata$election=0
speaker_metadata$rep_pres=0

#$election[elect_index]=1
speaker_metadata$rep_pres[rep_pres_index]=1


speaker_metadata$Date=as.character(speaker_metadata$Date)
date_dict=matrix(0,length(unique((speaker_metadata$Date))),2)

date_dict[,1]=unique((speaker_metadata$Date))
date_dict[,2]=seq(from=1,to=length(date_dict[,1]),by=1)
for(i in 1:length(date_dict[,1])){
  
  idx = which(speaker_metadata$Date==date_dict[i,1])
  speaker_metadata$Date[idx]=as.numeric(date_dict[i,2])
  
  
}

speaker_metadata$id=seq(from=1,to=length(speaker_metadata[,1]),by=1)

words=colnames(data)

#speaker_metadata$FoxStaff=0
#speaker_metadata$CNNStaff=0

#idx=which(speaker_metadata$Speaker=='Fox Staff')
#speaker_metadata$FoxStaff[idx]=1
#idx=which(speaker_metadata$Speaker=='CNN Staff')
#speaker_metadata$CNNStaff[idx]=1



C=data
dimnames(C) = list(speaker_metadata$id,words)

colnames(C)=words
rownames(C)=speaker_metadata$id


rm(data)


# Construct penalized estimation inputs
X   <- sparse.model.matrix( ~ 0 + rep_pres + Date+Speaker, data = speaker_metadata)

qx          <- qr(as.matrix(X))
X           <- X[, qx$pivot[1:qx$rank]]
rownames(X) <- speaker_metadata$id
X           <- X[rownames(C), ]


R         <- sparse.model.matrix(~ 0+ rep_pres + Date+Speaker, 
                                    data = speaker_metadata)
R          <- R * speaker_metadata$Party
colnames(R) <- paste(colnames(R), 'R', sep = '_')
rownames(R) <- speaker_metadata$id
R           <- R[rownames(C), ]


mu <- log(rowSums(C))

# Estimate penalized MLE
cl <- makeCluster(2, type = ifelse(.Platform$OS.type == 'unix', 'FORK', 'PSOCK')) 
fit <- dmr(
  cl = cl, 
  covars = cbind(X, R),
  counts = C, 
  mu = mu,
  free = 1:ncol(X),
  fixedcost = 1e-5,
  lambda.start = Inf,
  lambda.min.ratio = 1e-5,
  nlambda = 100,
  standardize = F
)
stopCluster(cl)
col_size=ncol(C)


# Get coefficients from penalized MLE
coefs   <- coef(fit, k = log(nrow(X)), corrected = F)
coefs_X <- coefs[colnames(X), ]
coefs_R <- coefs[colnames(R), ]

# Indicate Fox/CNN for speakers and clones
republican <- rowSums(R) > 0
republican <- as.vector(republican)

# Indicate session of congress for speakers and clones
session        <- as.numeric(speaker_metadata$Date)
names(session) <- speaker_metadata$id
session        <- session[rownames(C)]
session        <- as.matrix(session)

# Incremental utility of each phrase for Fox hosts in a given month
# "Phrase-time-specific Party loadings"
phi <- R %*% coefs_R

# Compute utility of speech for Democrats and Republicans
utility_D <- Matrix(cbind(1, X) %*% Matrix(rbind(coefs['intercept', ], coefs_X),sparse = TRUE),sparse=TRUE)
utility_R <- utility_D + phi

# Compute utility of speech for observed speakers and 
# speaker "clones" with the same speech and covariates but the opposite party.
party_matrix       <- replicate(col_size, rowSums(R))
party_matrix_clone <- (1 - party_matrix)
utility_real       <- utility_D + party_matrix * phi
utility_clone      <- utility_D + party_matrix_clone * phi

party_ratio        <- rowSums(exp(utility_D)) / rowSums(exp(utility_R))

likelihood_ratio   <- rowSums(exp(utility_D)) / rowSums(exp(utility_R)) * exp(phi)
rho                <- rowSums(exp(utility_D)) / rowSums(exp(utility_R)) * exp(phi / (1+ rowSums(exp(utility_D)) / rowSums(exp(utility_R)) * exp(phi)))
rho                <- likelihood_ratio / (1 + likelihood_ratio)
rm(utility_D)
rm(utility_R)
rm(likelihood_ratio)

q_real             <- exp(utility_real)  / rowSums(exp(utility_real))
q_clone            <- exp(utility_clone) / rowSums(exp(utility_clone))
rm(utility_real)
rm(utility_clone)
q_R                <- q_real * republican       + q_clone * (1 - republican) # Real Democrat speakers are Republicans in "clone" matrix
q_D                <- q_real * (1 - republican) + q_clone * republican       # Real Republican speakers are Democrats in "clone" matrix
pi                 <- rowSums(0.5 * q_R * rho + 0.5 * q_D * (1 - rho))

# Compute average partisanship
average_pi       <- tapply(pi, list(session), mean) 
average_pi       <- average_pi[order(as.integer(names(average_pi)))]
average_pi       <- data.frame(session = as.integer(names(average_pi)), average_pi = average_pi)
write.csv(average_pi, file = 'partisanship.csv', row.names = F, quote = F)

plot(average_pi$average_pi,type='l')

phidf <- as.matrix(phi)
colnames(phidf) <- colnames(C)
phi_cols_data <-  phidf[, which(colSums(phidf)!=0)]
phi_cols_data <- phi_cols_data[which(rowSums(phi_cols_data[,9:ncol(phi_cols_data)]) > 0), ]  # works much faster than below
phi_cols_data <- data.frame(phi_cols_data)
str(phi_cols_data)

needed<-which(rownames(phi_cols_data) %in% speaker_metadata$id)
speaker<-speaker_metadata[needed,]
phi_cols_data <- cbind(speaker,phi_cols_data)
write.csv(phi_cols_data, file = 'trigram_output_congress.csv', row.names = F, quote = F)








### 
### This code is developed by Christian P. Janssen of Utrecht University
### It is intended for students from the Master's course Cognitive Modeling
### Large parts are based on the following research papers:
### Janssen, C. P., & Brumby, D. P. (2010). Strategic adaptation to performance objectives in a dual‐task setting. Cognitive science, 34(8), 1548-1560. https://onlinelibrary.wiley.com/doi/full/10.1111/j.1551-6709.2010.01124.x
### Janssen, C. P., Brumby, D. P., & Garnett, R. (2012). Natural break points: The influence of priorities and cognitive and motor cues on dual-task interleaving. Journal of Cognitive Engineering and Decision Making, 6(1), 5-29. https://journals.sagepub.com/doi/abs/10.1177/1555343411432339
###
### If you want to use this code for anything outside of its intended purposes (training of AI students at Utrecht University), please contact the author:
### c.p.janssen@uu.nl



### 
### import packages
###

from pathlib import Path

import numpy
import matplotlib.pyplot as plt


###
###
### Global parameters. These can be called within functions to change (Python: make sure to call GLOBAL)
###
###


###
### Car / driving related parameters
###
steeringUpdateTime = 250    #in ms ## How long does one steering update take? (250 ms consistent with Salvucci 2005 Cognitive Science)
timeStepPerDriftUpdate = 50 ### msec: what is the time interval between two updates of lateral position?
startingPositionInLane = 0.27 			#assume that car starts already slightly away from lane centre (in meters) (cf. Janssen & Brumby, 2010)


#parameters for deviations in car drift due the simulator environment: See Janssen & Brumby (2010) page 1555
gaussDeviateMean = 0
gaussDeviateSD = 0.13 ##in meter/sec



### The car is controlled using a steering wheel that has a maximum angle. Therefore, there is also a maximum to the lateral velocity coming from a steering update
maxLateralVelocity = 1.7	# in m/s: maximum lateral velocity: what is the maximum that you can steer?
minLateralVelocity = -1* maxLateralVelocity

startvelocity = 0 	#a global parameter used to store the lateral velocity of the car


###
### Switch related parameters
###
retrievalTimeWord = 200   #ms. ## How long does it take to think of the next word when interleaving after a word (time not spent driving, but drifting)
retrievalTimeSentence = 300 #ms. ## how long does it take to retrieve a sentence from memory (time not spent driving, but drifting)



###
### parameters for typing task
###
timePerWord = 0  ### ms ## How much time does one word take
wordsPerMinuteMean = 39.33   # parameters that control typing speed: when typing two fingers, on average you type this many words per minute. From Jiang et al. (2020; CHI)
wordsPerMinuteSD = 10.3 ## this si standard deviation (Jiang et al, 2020)


## Function to reset all parameters. Call this function at the start of each simulated trial. Make sure to reset GLOBAL parameters.
def resetParameters():
    global timePerWord
    global retrievalTimeWord
    global retrievalTimeSentence 
    global steeringUpdateTime 
    global startingPositionInLane 
    global gaussDeviateMean
    global gaussDeviateSD 
    global gaussDriveNoiseMean 
    global gaussDriveNoiseSD 
    global timeStepPerDriftUpdate 
    global maxLateralVelocity 
    global minLateralVelocity 
    global startvelocity
    global wordsPerMinuteMean
    global wordsPerMinuteSD
    
    timePerWord = 0  ### ms

    retrievalTimeWord = 200   #ms
    retrievalTimeSentence = 300 #ms
	
    steeringUpdateTime = 250    #in ms
    startingPositionInLane = 0.27 			#assume that car starts already away from lane centre (in meters)
	

    gaussDeviateMean = 0
    gaussDeviateSD = 0.13 ##in meter/sec
    gaussDriveNoiseMean = 0
    gaussDriveNoiseSD = 0.1	#in meter/sec
    timeStepPerDriftUpdate = 50 ### msec: what is the time interval between two updates of lateral position?
    maxLateralVelocity = 1.7	# in m/s: maximum lateral velocity: what is the maximum that you can steer?
    minLateralVelocity = -1* maxLateralVelocity
    startvelocity = 0 	#a global parameter used to store the lateral velocity of the car
    wordsPerMinuteMean = 39.33
    wordsPerMinuteSD = 10.3
	



##calculates if the car is not accelerating (m/s) more than it should (maxLateralVelocity) or less than it should (minLateralVelocity)  (done for a vector of numbers)
def velocityCheckForVectors(velocityVectors):
    global maxLateralVelocity
    global minLateralVelocity

    velocityVectorsLoc = velocityVectors

    if (type(velocityVectorsLoc) is list):
            ### this can be done faster with for example numpy functions
        velocityVectorsLoc = velocityVectors
        for i in range(len(velocityVectorsLoc)):
            if(velocityVectorsLoc[i]>1.7):
                velocityVectorsLoc[i] = 1.7
            elif (velocityVectorsLoc[i] < -1.7):
                velocityVectorsLoc[i] = -1.7
    else:
        if(velocityVectorsLoc > 1.7):
            velocityVectorsLoc = 1.7
        elif (velocityVectorsLoc < -1.7):
            velocityVectorsLoc = -1.7

    return velocityVectorsLoc  ### in m/s
	




## Function to determine lateral velocity (controlled with steering wheel) based on where car is currently positioned. See Janssen & Brumby (2010) for more detailed explanation.
## Lateral velocity update depends on current position in lane. Intuition behind function: the further away you are, the stronger the correction will be that a human makes
def vehicleUpdateActiveSteering(LD):

	latVel = 0.2617 * LD*LD + 0.0233 * LD - 0.022
	returnValue = velocityCheckForVectors(latVel)
	return returnValue ### in m/s
	


### function to update lateral deviation in cases where the driver is NOT steering actively (when they are distracted by typing for example). Draw a value from a random distribution. This can be added to the position where the car is already.
def vehicleUpdateNotSteering():
    global gaussDeviateMean
    global gaussDeviateSD 

    vals = numpy.random.normal(loc=gaussDeviateMean, scale=gaussDeviateSD,size=1)[0]
    returnValue = velocityCheckForVectors(vals)
    return returnValue   ### in m/s


def plotTrialResults(locPos, locColor, trialTime, resultDir, plotId, interleaving):
    plt.figure(figsize=(25, 5))
    times = numpy.arange(len(locPos)) * timeStepPerDriftUpdate
    meanPos = numpy.mean(numpy.abs(locPos))
    maxPos = numpy.max(numpy.abs(locPos))
    locPosArr = numpy.array(locPos)
    colorArr = numpy.array(locColor)
    labels = {"green": "Start position", "red": "Typing (drift)", "blue": "Steering"}

    for color, label in labels.items():
        mask = colorArr == color
        plt.scatter(times[mask], locPosArr[mask], c=color, s=2, label=label)

    plt.legend(loc="best")
    plt.xlabel("Time (ms)")
    plt.ylabel("Lane position (m)")
    plt.title(f"Total trial time = {trialTime:.0f} ms; Mean position on the road = {meanPos:.3f} m; "
              f"Max position on the road (absolute) = {maxPos:.3f} m", fontsize=8)
    plt.savefig(resultDir / f"{interleaving}_trial_{0 if plotId < 10 else ''}{plotId}.png", dpi=300)
    
    
### Function to run a trial. Needs to be defined by students (section 2 and 3 of assignment)
def runTrial(resultDir, plotId, nrWordsPerSentence=17, nrSentences=10, nrSteeringMovementsWhenSteering=4,
             interleaving="word", directionalSteering=False): 
    def updateTrialActiveSteering():
        nonlocal locPos, locColor, trialTime
        
        for _ in range(nrSteeringMovementsWhenSteering):
            distanceSteering = vehicleUpdateActiveSteering(abs(locPos[-1])) * 0.25
            
            for _ in range(int(steeringUpdateTime / timeStepPerDriftUpdate)):
                if directionalSteering:
                    direction = -1 if locPos[-1] > 0 else 1
                    distanceSteering *= direction
                    
                newPos = locPos[-1] - (distanceSteering / 5)
                locPos.append(newPos)
                locColor.append("blue")
                
            trialTime += 250
            
    def updateTrialNotSteering(nrUpdates):
        nonlocal locPos, locColor, trialTime
        
        for _ in range(nrUpdates):
            drift = vehicleUpdateNotSteering() * 0.05
            newPos = locPos[-1]
            
            if directionalSteering:
                newPos += drift
            else:
                newPos += abs(drift)
                
            locPos.append(newPos)
            locColor.append("red")
    
          
    resetParameters()
    locPos = [startingPositionInLane] #measured in meters
    trialTime = 0 #measured in miliseconds
    locColor = ["green"]
    wordsPerMinute = numpy.random.normal(wordsPerMinuteMean, wordsPerMinuteSD)
    timePerWord = 60000 / wordsPerMinute

    for s in range(nrSentences):
        if interleaving == "word":
            for w in range(nrWordsPerSentence):
                if w == 0:
                    timeNoAttention = retrievalTimeSentence + retrievalTimeWord + timePerWord
                else:
                    timeNoAttention = retrievalTimeWord + timePerWord

                trialTime += timeNoAttention
                nrUpdates = int(timeNoAttention / timeStepPerDriftUpdate)
                updateTrialNotSteering(nrUpdates)
                
                if s == nrSentences - 1 and w == nrWordsPerSentence - 1:   # don't steer for the final word
                    break
                
                updateTrialActiveSteering()
        elif interleaving == "sentence":
            timeNoAttention = retrievalTimeSentence + (nrWordsPerSentence * timePerWord)
            trialTime += timeNoAttention
            nrUpdates = int(timeNoAttention / timeStepPerDriftUpdate)
            updateTrialNotSteering(nrUpdates)
            
            if s == nrSentences - 1:   # don't steer for the final sentence
                break
            
            updateTrialActiveSteering()
                
    plotTrialResults(locPos, locColor, trialTime, resultDir, plotId, interleaving)


### function to run multiple simulations. Needs to be defined by students (section 3 of assignment)
def runSimulations(nrSims = 100):
    print("hello world")


def main():
    result_dir = Path("results/section2")
    result_dir.mkdir(parents=True, exist_ok=True)
    
    for plot_id in range(1, 11):
        runTrial(resultDir=result_dir, plotId=plot_id, interleaving="word")
        runTrial(resultDir=result_dir, plotId=plot_id, interleaving="sentence")
    
    
if __name__ == "__main__":
    main()

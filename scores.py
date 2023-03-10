import json
import requests
from AdminDatabase import *

def getCodeforcesRating(codeforcesHandle):
    profileUrl = f"https://competitive-coding-api.herokuapp.com/api/codeforces/{codeforcesHandle}"
    req = requests.get(profileUrl)
    jsonData = json.loads(req.content)

    rating = jsonData["rating"]

    req.close()
    return rating

def getCodechefRating(codechefsHandle):
    profileUrl = f"https://competitive-coding-api.herokuapp.com/api/codechef/{codechefsHandle}"
    req = requests.get(profileUrl)
    jsonData = json.loads(req.content)

    rating = int(jsonData["rating"])
    totalsolved = int(jsonData["fully_solved"]["count"])
    rating = rating + totalsolved*20

    req.close()
    return rating

def getInterviewBitRating(inerviewbitHandle):
    profileUrl = f"https://competitive-coding-api.herokuapp.com/api/interviewbit/{inerviewbitHandle}"
    req = requests.get(profileUrl)
    jsonData = json.loads(req.content)
    score = int(jsonData["score"])
    req.close()
    return score//10
    

def getSpojRating(spojHandle):
    profileUrl = f"https://competitive-coding-api.herokuapp.com/api/spoj/{spojHandle}"
    req = requests.get(profileUrl)
    jsonData = json.loads(req.content)
    points = float(jsonData["points"])

    profileUrl = f"http://all-cp-platforms-api.herokuapp.com/api/spoj/{spojHandle}"
    req = requests.get(profileUrl)
    jsonData = json.loads(req.content)
    submissions = int(jsonData["Problems solved"])

    rating = points*500+submissions*10
    req.close()
    return int(rating)
    
def getLeetcodeRating(leetcodeHandle):
    profileUrl = f"https://competitive-coding-api.herokuapp.com/api/leetcode/{leetcodeHandle}"
    req = requests.get(profileUrl)
    jsonData = json.loads(req.content)

    totalProblemsSolved = int(jsonData["total_problems_solved"])

    contributionPoints = int(jsonData["contribution_points"])

    rating = contributionPoints + totalProblemsSolved*10
    req.close()
    return int(rating)
    
def getOverAllRating(codeforcesRating,codechefRating,interviewBitRating,spojRating,leetcodeRating):
    return sum([codeforcesRating,codechefRating,interviewBitRating,spojRating,leetcodeRating])


def updateScore():
    #gathering all the registered userIds
    users = getAllUsers()

    for user in users:
        userId = user[0]
        handles = getUserHandles(userId)
        if(handles is None):
            print("The user does not exists")
            exit(0)

        #retrivng the scores of all platforms
        codechefRating = getCodechefRating(handles["codechef"])
        codeforcesRating = getCodeforcesRating(handles["codeforces"])
        interviewBitRating = getInterviewBitRating(handles["interviewBit"])
        leetcodeRating = getLeetcodeRating(handles["leetcode"])
        spojRating = getSpojRating(handles["spoj"])

        #calculating overall score
        overAllRating = getOverAllRating(codeforcesRating,codechefRating,interviewBitRating,spojRating,leetcodeRating)

        #to update the values in the database table
        updateLeaderBoard(userId,codechefRating,codeforcesRating,interviewBitRating,leetcodeRating,spojRating,overAllRating)
        print(f"userid:{userId}\ncodeforces: {codeforcesRating}\ncodechef:{codechefRating}\ninterview bit:{interviewBitRating}\nspoj:{spojRating}\nleetcode:{leetcodeRating}\noverall:{overAllRating}\n")

if __name__ == "__main__":
    updateScore()
    
import cgi
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import mail
from google.appengine.api import urlfetch

# data model section
class GoalMessage(db.Model):
    author = db.UserProperty()
    jobGoal = db.StringProperty(multiline=True)
    schoolGoal = db.StringProperty(multiline=True)
    gycGoal = db.StringProperty(multiline=True)

class NotepadText(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    
class UserInfo(db.Model):
    author = db.UserProperty()
    firstName = db.StringProperty()
    lastName = db.StringProperty()
    phoneNumber = db.StringProperty()
    school = db.StringProperty()
    gradeLevel = db.StringProperty()

class PersonalityInfo(db.Model):
    author = db.UserProperty()
    content = db.StringListProperty()

class Extracurriculars(db.Model):
    author = db.UserProperty()
    
    activityName1 = db.StringProperty()
    dateStarted1 = db.StringProperty()
    dateEnded1 = db.StringProperty()
    appeals1 = db.StringProperty(multiline=True)
    references1 = db.StringProperty(multiline=True)
    accomplish1 = db.StringProperty(multiline=True)
    notes1 = db.StringProperty(multiline=True)
    
    activityName2 = db.StringProperty()
    dateStarted2 = db.StringProperty()
    dateEnded2 = db.StringProperty()
    appeals2 = db.StringProperty(multiline=True)
    references2 = db.StringProperty(multiline=True)
    accomplish2 = db.StringProperty(multiline=True)
    notes2 = db.StringProperty(multiline=True)

    activityName3 = db.StringProperty()
    dateStarted3 = db.StringProperty()
    dateEnded3 = db.StringProperty()
    appeals3 = db.StringProperty(multiline=True)
    references3 = db.StringProperty(multiline=True)
    accomplish3 = db.StringProperty(multiline=True)
    notes3 = db.StringProperty(multiline=True)
    
    activityName4 = db.StringProperty()
    dateStarted4 = db.StringProperty()
    dateEnded4 = db.StringProperty()
    appeals4 = db.StringProperty(multiline=True)
    references4 = db.StringProperty(multiline=True)
    accomplish4 = db.StringProperty(multiline=True)
    notes4 = db.StringProperty(multiline=True)
    
    activityName5 = db.StringProperty()
    dateStarted5 = db.StringProperty()
    dateEnded5 = db.StringProperty()
    appeals5 = db.StringProperty(multiline=True)
    references5 = db.StringProperty(multiline=True)
    accomplish5 = db.StringProperty(multiline=True)
    notes5 = db.StringProperty(multiline=True)
    
    otherExtracurricNotes = db.StringProperty(multiline=True)

class FeedbackMessage(db.Model):
    author = db.UserProperty()
    messageType = db.StringProperty()
    message = db.StringProperty(multiline=True)
    
# standard query function section
def queryUserInfo():
    # first reset vals in case the calling function references the variable without it
    # being assigned after a query
    firstName = lastName = phoneNumber = school = grade = ""
    
    
    userInfo_query = UserInfo.all()
    userInfo_list = userInfo_query.filter("author =", users.get_current_user())
    userInfo = userInfo_list.fetch(1)
    for info in userInfo:
        firstName = info.firstName
        lastName = info.lastName
        phoneNumber = info.phoneNumber
        school = info.school
        grade = info.gradeLevel
    return (firstName, lastName, phoneNumber, school, grade)

def queryStudentGoals():
    user_goals = jobGoal = schoolGoal = gycGoal = ""
    user_goals = GoalMessage.all().filter("author = ",users.get_current_user()).fetch(1)
    for info in user_goals:
        jobGoal = info.jobGoal
        schoolGoal = info.schoolGoal
        gycGoal = info.gycGoal
    return (jobGoal, schoolGoal, gycGoal)

def queryNotepadText():
    user_note = NotepadText.all().filter("author = ",users.get_current_user()).fetch(1)
    return user_note

def queryPersonality():
    user_personality = PersonalityInfo.all().filter("author = ",users.get_current_user()).fetch(1)
    return user_personality

def queryPersonalityStats():
    gChartAPIString = ""
    personality_info = queryPersonality()
    if personality_info:
        letterKeys = [item[0] for item in personality_info[0]._content]
        realisticTotal = letterKeys.count('R')
        investigativeTotal = letterKeys.count('I')
        artisticTotal = letterKeys.count('A')
        socialTotal = letterKeys.count('S')
        enterprisingTotal = letterKeys.count('E')
        conventionalTotal = letterKeys.count('C')
        gChartAPIString = ""
        
        totalLetters = len(personality_info[0]._content)
        if totalLetters > 0:
            # calculating proportions
            realisticPct = RoundedPctString(realisticTotal,totalLetters)
            investigativePct = RoundedPctString(investigativeTotal,totalLetters)
            artisticPct = RoundedPctString(artisticTotal,totalLetters)
            socialPct = RoundedPctString(socialTotal,totalLetters)
            enterprisingPct = RoundedPctString(enterprisingTotal,totalLetters)
            conventionalPct = RoundedPctString(conventionalTotal,totalLetters)
            
            gChartAPIString = "http://chart.apis.google.com/chart?cht=p3&chd=t:%s,%s,%s,%s,%s,%s&chs=800x350&chl=Realistic|Investigative|Artistic|Social|Enterprising|Conventional" \
                                    % (realisticPct, investigativePct, artisticPct, socialPct, enterprisingPct, conventionalPct)
    return gChartAPIString

def queryExtracurriculars():
    activityName1 = dateStarted1 = dateEnded1 = appeals1 = references1 = accomplish1 = notes1 = ""
    activityName2 = dateStarted2 = dateEnded2 = appeals2 = references2 = accomplish2 = notes2 = ""
    activityName3 = dateStarted3 = dateEnded3 = appeals3 = references3 = accomplish3 = notes3 = ""
    activityName4 = dateStarted4 = dateEnded4 = appeals4 = references4 = accomplish4 = notes4 = ""
    activityName5 = dateStarted5 = dateEnded5 = appeals5 = references5 = accomplish5 = notes5 = ""
    otherExtracurricNotes = ""
    
    user_extracurricular = Extracurriculars.all().filter("author = ",users.get_current_user()).fetch(1)
    for info in user_extracurricular:
        activityName1 = info.activityName1
        dateStarted1 = info.dateStarted1
        dateEnded1 = info.dateEnded1
        appeals1 = info.appeals1
        references1 = info.references1
        accomplish1 = info.accomplish1
        notes1 = info.notes1
        
        activityName2 = info.activityName2
        dateStarted2 = info.dateStarted2
        dateEnded2 = info.dateEnded2
        appeals2 = info.appeals2
        references2 = info.references2
        accomplish2 = info.accomplish2
        notes2 = info.notes2
        
        activityName3 = info.activityName3
        dateStarted3 = info.dateStarted3
        dateEnded3 = info.dateEnded3
        appeals3 = info.appeals3
        references3 = info.references3
        accomplish3 = info.accomplish3
        notes3 = info.notes3
        
        activityName4 = info.activityName4
        dateStarted4 = info.dateStarted4
        dateEnded4 = info.dateEnded4
        appeals4 = info.appeals4
        references4 = info.references4
        accomplish4 = info.accomplish4
        notes4 = info.notes4
        
        activityName5 = info.activityName5
        dateStarted5 = info.dateStarted5
        dateEnded5 = info.dateEnded5
        appeals5 = info.appeals5
        references5 = info.references5
        accomplish5 = info.accomplish5
        notes5 = info.notes5
        
        otherExtracurricNotes = info.otherExtracurricNotes
        
    return (activityName1, dateStarted1, dateEnded1, appeals1, references1, accomplish1, notes1,
            activityName2, dateStarted2, dateEnded2, appeals2, references2, accomplish2, notes2,
            activityName3, dateStarted3, dateEnded3, appeals3, references3, accomplish3, notes3,
            activityName4, dateStarted4, dateEnded4, appeals4, references4, accomplish4, notes4,
            activityName5, dateStarted5, dateEnded5, appeals5, references5, accomplish5, notes5,
            otherExtracurricNotes)
    
# other utility functions
def RoundedPctString(portion, total):
    return '%.0f' % ((1.0 * portion / total) * 100)
    
# page definition section

class GeneralPage(webapp.RequestHandler):
    # this is the general set of initial values for a new page in this schema
    # just copy-paste for now until refactoring in version 2
    def get(self):
        user = users.get_current_user()
        pageTemplate = 'goalSheet.html'
        
        
        # query code and variable setting goes here
            
            
        # create a logout
        logout_url = users.create_logout_url(self.request.uri)
        logout_linktext = 'Log Out of Odyssey'
            
        # enter your variables to pass to the page here
        template_values = {'logout_url': logout_url,
                           'logout_linktext': logout_linktext}
            
        # call the proper page in an OS-agnostic way
        path = os.path.join(os.path.dirname(__file__), pageTemplate)
        self.response.out.write(template.render(path, template_values))

class MainPage(webapp.RequestHandler):
    def get(self):

        user = users.get_current_user()
        
        firstName, lastName, phoneNumber, school, grade = queryUserInfo()
        welcomeString = ""
            
        gradeActivityList = ""
        commonActivities = []

        # do this for the kind of activity in which the results are on a separate page
        # and we only want that page to be accessible if (a) the user has done it before and
        # (b) there might be useful information on it
        totalPersonalityItems = 0
        personality_info = queryPersonality()
        if personality_info:
            totalPersonalityItems = len(personality_info[0]._content)
            
            
        commonActivitiesList = ['Define Goals','Complete a New Personal Inventory','Record Extracurricular Activities','Send Feedback to GYC','Notepad']
        commonUrlList = ['/GoalsPage','/InventoryPage','/ExtracurricularPage','/FeedbackPage','/Notepad']
        commonActivityList = zip(commonActivitiesList,commonUrlList)
            
        if personality_info and (totalPersonalityItems > 0):
            personalityResultsTuple = ('View Past Personality Inventory Results','/InventoryResultsPage')
            commonActivityList.insert(2,personalityResultsTuple)
            
        # these lists are empty for now (December 2009)
        # but this is a fully-functional feature that lists certain activities
        # depending on grade level
            
        seniorActivitiesList = []
        seniorUrlList = []
        seniorPairingList = zip(seniorActivitiesList,seniorUrlList)
            
        juniorActivitiesList = []
        juniorUrlList = []
        juniorPairingList = zip(juniorActivitiesList,juniorUrlList)
            
        sophActivitiesList = []
        sophUrlList = []
        sophPairingList = zip(sophActivitiesList,sophUrlList)
            
        freshActivitiesList = []
        freshUrlList = []
        freshPairingList = zip(freshActivitiesList,freshUrlList)
            
        if firstName.strip() == "":
            self.redirect('/UserInfoPage')
        elif lastName.strip() == "":
            self.redirect('/UserInfoPage')
        else:
            welcomeString = "Welcome, " + firstName + "!"
            
        if grade == "Senior":
            gradeActivityList = seniorPairingList
        elif grade == "Junior":
            gradeActivityList = juniorPairingList
        elif grade == "Sophomore":
            gradeActivityList = sophPairingList
        elif grade == "Freshman":
            gradeActivityList = freshPairingList
        else:
            gradeActivityList = []
                
        logout_url = users.create_logout_url(self.request.uri)
        logout_linktext = 'Log Out of Odyssey'

        userInfo_url = '/UserInfoPage'
            
        template_values = {
            'logout_url': logout_url,
            'logout_linktext': logout_linktext,
            'userInfo_url': userInfo_url,
            'firstName': firstName,
            'welcomeString': welcomeString,
            'commonActivityList': commonActivityList,
            'gradeActivityList': gradeActivityList,
        }
            
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class UserInfoPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        
        firstName, lastName, phoneNumber, school, grade = queryUserInfo()
        logout_url = users.create_logout_url(self.request.uri)
        logout_linktext = 'Log Out of Odyssey'
            
        # cludgy way to make sure you get the right default selection
        # in a drop-down list
        # could be optimized
            
        uchs_selected = west_selected = auto_selected = none_selected = ""
            
        if school == "UCHS":
            uchs_selected = 'selected'
        elif school == "West":
            west_selected = 'selected'
        elif school == "West Auto Academy":
            auto_selected = 'selected'
        else:
            none_selected = 'selected'
            
        fresh_selected = soph_selected = junior_selected = senior_selected = ""
            
        if grade == "Freshman":
            fresh_selected = 'selected'
        elif grade == "Sophomore":
            soph_selected = 'selected'
        elif grade == "Junior":
            junior_selected = 'selected'
        elif grade == "Senior":
            senior_selected = 'selected'
        else:
            none_selected = 'selected'
            
        proceed_link = "More information required to proceed to main activities page."
        if (len(firstName) and len(lastName)) > 0:
            proceed_link = '<a href="/">All required information complete! Proceed to activities page</a>'
            
        userName = user.nickname()
        template_values = {
            'logout_url': logout_url,
            'logout_linktext': logout_linktext,
            'username': userName,
            'firstName': firstName,
            'lastName': lastName,
            'phoneNumber': phoneNumber,
            'school': school,
            'grade': grade,
            'uchs_selected': uchs_selected,
            'west_selected': west_selected,
            'auto_selected': auto_selected,
            'none_selected': none_selected,
            'fresh_selected': fresh_selected,
            'soph_selected': soph_selected,
            'junior_selected': junior_selected,
            'senior_selected': senior_selected,
            'proceed_link': proceed_link
        }
        path = os.path.join(os.path.dirname(__file__), 'userInfo.html')
        self.response.out.write(template.render(path, template_values))

class GoalsPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
            
        jobGoal, schoolGoal, gycGoal = queryStudentGoals()
            
        logout_url = users.create_logout_url(self.request.uri)
        logout_linktext = 'Log Out of Odyssey'
            
        template_values = { 'logout_url': logout_url,
                            'logout_linktext': logout_linktext,
                            'jobGoal': jobGoal,
                            'schoolGoal': schoolGoal,
                            'gycGoal': gycGoal
                          }
            
        path = os.path.join(os.path.dirname(__file__), 'goalSheet.html')
        self.response.out.write(template.render(path, template_values))

class NotepadPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        logout_url = users.create_logout_url(self.request.uri)
        logout_linktext = 'Log Out of Odyssey'
            
        user_note = queryNotepadText()
        template_values = { 'user_note': user_note,
                            'logout_url': logout_url,
                            'logout_linktext': logout_linktext}
            
        path = os.path.join(os.path.dirname(__file__), 'notepadSheet.html')
        self.response.out.write(template.render(path, template_values))
        
    
class UserSummaryPage(webapp.RequestHandler):
    def get(self):
        
        user = users.get_current_user()
        pageTemplate = 'userSummaryPage.html'
        
        # query code and variable setting goes here
        firstName, lastName, phoneNumber, school, grade = queryUserInfo()
        notepad_contents = queryNotepadText()
        personality_chart = queryPersonalityStats()
        jobGoal, schoolGoal, gycGoal = queryStudentGoals()
            
        extracurriculars = list(queryExtracurriculars())
        # remove blank entries from extracurriculars before output
        extracurriculars = [item for item in extracurriculars if item!='']

            
        logout_url = users.create_logout_url(self.request.uri)
        logout_linktext = 'Log Out of Odyssey'
            
        # enter your variables to pass to the page here
        template_values = { 'logout_url': logout_url,
                            'logout_linktext': logout_linktext,
                            'firstName': firstName,
                            'lastName': lastName,
                            'phoneNumber': phoneNumber,
                            'school': school,
                            'grade': grade,
                            'notepad_contents': notepad_contents,
                            'personality_chart': personality_chart,
                            'jobGoal': jobGoal,
                            'schoolGoal': schoolGoal,
                            'gycGoal': gycGoal,
                            'extracurriculars': extracurriculars,
                          }
            
        # call the proper page in an OS-agnostic way
        path = os.path.join(os.path.dirname(__file__), pageTemplate)
        self.response.out.write(template.render(path, template_values))
        

class InventoryPage(webapp.RequestHandler):
    
    def get(self):
        user = users.get_current_user()
        pageTemplate = 'persInventorySheet.html'
            
        logout_url = users.create_logout_url(self.request.uri)
        logout_linktext = 'Log Out of Odyssey'
            
        # enter your variables to pass to the page here
            
        template_values = {'logout_url': logout_url,
                           'logout_linktext': logout_linktext,
                          }
            
        # call the proper page in an OS-agnostic way
        path = os.path.join(os.path.dirname(__file__), pageTemplate)
        self.response.out.write(template.render(path, template_values))

class InventoryResultsPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        pageTemplate = 'inventoryResultsSheet.html'
        
        # query code and variable setting goes here
            
        personality_info = queryPersonality()
            
        totalLetters = realisticPct = investigativePct \
        = artisticPct = socialPct = enterprisingPct = conventionalPct = 0
            
        gChartAPIString = ""
            
        # FIXME: good refactoring candidate
        if personality_info:
            letterKeys = [item[0] for item in personality_info[0]._content]
            realisticTotal = letterKeys.count('R')
            investigativeTotal = letterKeys.count('I')
            artisticTotal = letterKeys.count('A')
            socialTotal = letterKeys.count('S')
            enterprisingTotal = letterKeys.count('E')
            conventionalTotal = letterKeys.count('C')
            gChartAPIString = ""
        
            totalLetters = len(personality_info[0]._content)
                
            if totalLetters > 0:
            # calculating proportions
                realisticPct = RoundedPctString(realisticTotal,totalLetters)
                investigativePct = RoundedPctString(investigativeTotal,totalLetters)
                artisticPct = RoundedPctString(artisticTotal,totalLetters)
                socialPct = RoundedPctString(socialTotal,totalLetters)
                enterprisingPct = RoundedPctString(enterprisingTotal,totalLetters)
                conventionalPct = RoundedPctString(conventionalTotal,totalLetters)
            
                gChartAPIString = "http://chart.apis.google.com/chart?cht=p3&chd=t:%s,%s,%s,%s,%s,%s&chs=800x350&chl=Realistic|Investigative|Artistic|Social|Enterprising|Conventional" \
                                % (realisticPct, investigativePct, artisticPct, socialPct, enterprisingPct, conventionalPct)

            # create a logout
        logout_url = users.create_logout_url(self.request.uri)
        logout_linktext = 'Log Out of Odyssey'
            
        # enter your variables to pass to the page here
        template_values = {
                           'totalLetters': totalLetters,
                           'gChartAPIString': gChartAPIString,
                           'logout_url': logout_url,
                           'logout_linktext': logout_linktext,
                           'RealPCT' : realisticPct,
                           'InvestPCT' : investigativePct,
                           'ArtPCT' : artisticPct,
                           'SocialPCT' : socialPct,
                           'EnterPCT' : enterprisingPct,
                           'ConventPCT' : conventionalPct,
                          }
            
        # call the proper page in an OS-agnostic way
        path = os.path.join(os.path.dirname(__file__), pageTemplate)
        self.response.out.write(template.render(path, template_values))

class ExtracurricularPage(webapp.RequestHandler):
    # this is the general set of initial values for a new page in this schema
    # just do the copy-paste thing for now until have time to refactor
    def get(self):
        user = users.get_current_user()
        pageTemplate = 'extracurricularSheet.html'
        
        # query code and variable setting goes here
            
        activityName1, dateStarted1, dateEnded1, appeals1, references1, accomplish1, notes1, \
        activityName2, dateStarted2, dateEnded2, appeals2, references2, accomplish2, notes2, \
        activityName3, dateStarted3, dateEnded3, appeals3, references3, accomplish3, notes3, \
        activityName4, dateStarted4, dateEnded4, appeals4, references4, accomplish4, notes4, \
        activityName5, dateStarted5, dateEnded5, appeals5, references5, accomplish5, notes5, \
        otherExtracurricNotes =  queryExtracurriculars()
            
        # create a logout
        logout_url = users.create_logout_url(self.request.uri)
        logout_linktext = 'Log Out of Odyssey'
            
        # enter your variables to pass to the page here
        template_values = {'logout_url': logout_url,
                           'logout_linktext': logout_linktext,
                           'activityName1': activityName1,
                           'dateStarted1': dateStarted1,
                           'dateEnded1': dateEnded1,
                           'appeals1': appeals1,
                           'references1': references1,
                           'accomplish1': accomplish1,
                           'notes1': notes1,
                           'activityName2': activityName2,
                           'dateStarted2': dateStarted2,
                           'dateEnded2': dateEnded2,
                           'appeals2': appeals2,
                           'references2': references2,
                           'accomplish2': accomplish2,
                           'notes2': notes2,
                           'activityName3': activityName3,
                           'dateStarted3': dateStarted3,
                           'dateEnded3': dateEnded3,
                           'appeals3': appeals3,
                           'references3': references3,
                           'accomplish3': accomplish3,
                           'notes3': notes3,
                           'activityName4': activityName4,
                           'dateStarted4': dateStarted4,
                           'dateEnded4': dateEnded4,
                           'appeals4': appeals4,
                           'references4': references4,
                           'accomplish4': accomplish4,
                           'notes4': notes4,
                           'activityName5': activityName5,
                           'dateStarted5': dateStarted5,
                           'dateEnded5': dateEnded5,
                           'appeals5': appeals5,
                           'references5': references5,
                           'accomplish5': accomplish5,
                           'notes5': notes5,
                           'otherExtracurricNotes': otherExtracurricNotes
                           }
            
        # call the proper page in an OS-agnostic way
        path = os.path.join(os.path.dirname(__file__), pageTemplate)
        self.response.out.write(template.render(path, template_values))

class FeedbackPage(webapp.RequestHandler):
    # this is the general set of initial values for a new page in this schema
    # just do the copy-paste thing for now until have time to refactor
    def get(self):
        user = users.get_current_user()
        pageTemplate = 'feedbackSheet.html'
        
        # query code and variable setting goes here
            
            
        # create a logout
        logout_url = users.create_logout_url(self.request.uri)
        logout_linktext = 'Log Out of Odyssey'
          
        # enter your variables to pass to the page here
        template_values = {'logout_url': logout_url,
                           'logout_linktext': logout_linktext}
            
        # call the proper page in an OS-agnostic way
        path = os.path.join(os.path.dirname(__file__), pageTemplate)
        self.response.out.write(template.render(path, template_values))

class ThanksPage(webapp.RequestHandler):
    # this is the general set of initial values for a new page in this schema
    # just do the copy-paste thing for now until have time to refactor
    def get(self):
        user = users.get_current_user()
        pageTemplate = 'thanksSheet.html'
        
        # query code and variable setting goes here
            
            
        # create a logout
        logout_url = users.create_logout_url(self.request.uri)
        logout_linktext = 'Log Out of Odyssey'
            
        # enter your variables to pass to the page here
        template_values = {'logout_url': logout_url,
                           'logout_linktext': logout_linktext}
            
        # call the proper page in an OS-agnostic way
        path = os.path.join(os.path.dirname(__file__), pageTemplate)
        self.response.out.write(template.render(path, template_values))

class AboutOdysseyPage(webapp.RequestHandler):
    # this is the general set of initial values for a new page in this schema
    # just do the copy-paste thing for now until have time to refactor
    def get(self):
        user = users.get_current_user()
        pageTemplate = 'aboutOdyssey.html'
        
        
        # query code and variable setting goes here
            
            
        # create a logout
        logout_url = users.create_logout_url(self.request.uri)
        logout_linktext = 'Log Out of Odyssey'
            
        # enter your variables to pass to the page here
        template_values = {'logout_url': logout_url,
                           'logout_linktext': logout_linktext}
            
        # call the proper page in an OS-agnostic way
        path = os.path.join(os.path.dirname(__file__), pageTemplate)
        self.response.out.write(template.render(path, template_values))

class GDocsTemplates(webapp.RequestHandler):
    # this is the general set of initial values for a new page in this schema
    # just copy-paste for now until refactoring in version 2
    def get(self):
        user = users.get_current_user()
        pageTemplate = 'docsTemplatesSheet.html'
            
        # query code and variable setting goes here
            
            
        # create a logout
        logout_url = users.create_logout_url(self.request.uri)
        logout_linktext = 'Log Out of Odyssey'
            
        # enter your variables to pass to the page here
        template_values = {'logout_url': logout_url,
                           'logout_linktext': logout_linktext,
                          }
            
        # call the proper page in an OS-agnostic way
        path = os.path.join(os.path.dirname(__file__), pageTemplate)
        self.response.out.write(template.render(path, template_values))

# action section (write classes)
class goalWriter(webapp.RequestHandler):
    def post(self):
        
        user_goals = GoalMessage.all().filter("author =",users.get_current_user()).fetch(1)
        for goal in user_goals:
            goal.delete()
        
        newGoal = GoalMessage()
        newGoal.author = users.get_current_user()
        newGoal.jobGoal = self.request.get('jobGoal')
        newGoal.schoolGoal = self.request.get('schoolGoal')
        newGoal.gycGoal = self.request.get('gycGoal')
        newGoal.put()
        
        self.redirect('/GoalsPage')

class noteWriter(webapp.RequestHandler):
    def post(self):
        
        user_note = queryNotepadText()
        for note in user_note:
            note.delete()
         
        newNote = NotepadText()
        newNote.author = users.get_current_user()
        newNote.content = self.request.get('notepadText')
        newNote.put()
        
        self.redirect('/Notepad')
        
class userEditWriter(webapp.RequestHandler):
    def post(self):
        userInfo_query = UserInfo.all()
        userInfo_list = userInfo_query.filter("author =", users.get_current_user())
        userInfo = userInfo_list.fetch(1)
        
        for userItem in userInfo:
            userItem.delete()
        
        newUserInfo = UserInfo()
        newUserInfo.author = users.get_current_user()
        newUserInfo.firstName = self.request.get('firstName')
        newUserInfo.lastName = self.request.get('lastName')
        newUserInfo.phoneNumber = self.request.get('phoneNumber')
        newUserInfo.school = self.request.get('school')
        newUserInfo.gradeLevel = self.request.get('grade')
        newUserInfo.put()
        
        self.redirect('/UserInfoPage')
        
class personalInventoryWriter(webapp.RequestHandler):
    def post(self):
        
        userPersonality_query = PersonalityInfo.all().filter("author =",users.get_current_user()).fetch(1)
        for userItem in userPersonality_query:
            userItem.delete()
        
        userPersonality = PersonalityInfo()
        userPersonality.author = users.get_current_user()
        userPersonality.content = self.request.get_all('adjectives')
        userPersonality.put()
        
        self.redirect('/InventoryResultsPage')

class extracurricularWrite(webapp.RequestHandler):
    def post(self):
        
        extracurricular_query = Extracurriculars.all().filter("author =",users.get_current_user()).fetch(1)
        for userItem in extracurricular_query:
            userItem.delete()
        
        userExtracurricular = Extracurriculars()
        userExtracurricular.author = users.get_current_user()
        
        userExtracurricular.activityName1 = self.request.get('activityName1')
        userExtracurricular.dateStarted1 = self.request.get('dateStarted1')
        userExtracurricular.dateEnded1 = self.request.get('dateEnded1')
        userExtracurricular.appeals1 = self.request.get('appeals1')
        userExtracurricular.references1 = self.request.get('references1')
        userExtracurricular.accomplish1 = self.request.get('accomplish1')
        userExtracurricular.notes1 = self.request.get('notes1')
        
        userExtracurricular.activityName2 = self.request.get('activityName2')
        userExtracurricular.dateStarted2 = self.request.get('dateStarted2')
        userExtracurricular.dateEnded2 = self.request.get('dateEnded2')
        userExtracurricular.appeals2 = self.request.get('appeals2')
        userExtracurricular.references2 = self.request.get('references2')
        userExtracurricular.accomplish2 = self.request.get('accomplish2')
        userExtracurricular.notes2 = self.request.get('notes2')
        
        userExtracurricular.activityName3 = self.request.get('activityName3')
        userExtracurricular.dateStarted3 = self.request.get('dateStarted3')
        userExtracurricular.dateEnded3 = self.request.get('dateEnded3')
        userExtracurricular.appeals3 = self.request.get('appeals3')
        userExtracurricular.references3 = self.request.get('references3')
        userExtracurricular.accomplish3 = self.request.get('accomplish3')
        userExtracurricular.notes3 = self.request.get('notes3')
        
        userExtracurricular.activityName4 = self.request.get('activityName4')
        userExtracurricular.dateStarted4 = self.request.get('dateStarted4')
        userExtracurricular.dateEnded4 = self.request.get('dateEnded4')
        userExtracurricular.appeals4 = self.request.get('appeals4')
        userExtracurricular.references4 = self.request.get('references4')
        userExtracurricular.accomplish4 = self.request.get('accomplish4')
        userExtracurricular.notes4 = self.request.get('notes4')
        
        userExtracurricular.activityName5 = self.request.get('activityName5')
        userExtracurricular.dateStarted5 = self.request.get('dateStarted5')
        userExtracurricular.dateEnded5 = self.request.get('dateEnded5')
        userExtracurricular.appeals5 = self.request.get('appeals5')
        userExtracurricular.references5 = self.request.get('references5')
        userExtracurricular.accomplish5 = self.request.get('accomplish5')
        userExtracurricular.notes5 = self.request.get('notes5')
        
        userExtracurricular.otherExtracurricNotes = self.request.get('otherExtracurricNotes')
        userExtracurricular.put()
        
        self.redirect('/ExtracurricularPage')

class sendFeedback(webapp.RequestHandler):
    def post(self):
        
        userMessage = FeedbackMessage()
        userMessage.author = users.get_current_user()
        userMessage.messageType = self.request.get('messageType')
        userMessage.message = self.request.get('message')
        userMessage.put()
        
        mail.send_mail(sender=users.get_current_user().email(),
                       to='drexelgyc@gmail.com',
                       subject=userMessage.messageType,
                       body=userMessage.message)
        
        self.redirect('/ThanksPage')

# defining main application handlers and all that
application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/UserInfoPage', UserInfoPage),
                                      ('/userEdit', userEditWriter),
                                      ('/GoalsPage', GoalsPage),
                                      ('/goalDefine', goalWriter),
                                      ('/UserSummaryPage', UserSummaryPage),
                                      ('/Notepad', NotepadPage),
                                      ('/noteWrite', noteWriter),
                                      ('/InventoryPage',InventoryPage),
                                      ('/inventoryWrite', personalInventoryWriter),
                                      ('/InventoryResultsPage',InventoryResultsPage),
                                      ('/ExtracurricularPage',ExtracurricularPage),
                                      ('/extracurricularWrite', extracurricularWrite),
                                      ('/FeedbackPage',FeedbackPage),
                                      ('/sendFeedback',sendFeedback),
                                      ('/ThanksPage',ThanksPage),
                                      ('/GDocsTemplates',GDocsTemplates),
                                      ('/AboutOdyssey',AboutOdysseyPage),
                                      ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
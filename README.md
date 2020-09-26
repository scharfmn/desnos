# Desnos: Language Events

## an Experiment in Free-Tier Poetry Pegagogy

### designed for the classroom by Vivek Narayanan

with code by scharfmn

## Introduction

Desnos is an application version of Robert Desnos' Language Event 1 and Language Event 2 as adapted for the classroom

In this version of Desnos' language events, the user creates a specific language “event” for a class meeting. Students contribute text in real-time, which is then combined into a poem in real-time. Can be done in-person or remote.

Try this one (which shows pre-loaded text as a demo):

- https://desnos.herokuapp.com/demo/qa/combine

## Inspiration

![original language event 1](https://storage.googleapis.com/mns/desnos_1a.png)

![original language event 2](https://storage.googleapis.com/mns/desnos_2.png)

## question -> answer language event:
The "add" endpoints allow anyone with the URL to send text to the event:
 - https://desnos.herokuapp.com/{some-random-id}/qa/add
 
The "combine" endpoints randomly combine the text sent into the event in couplets: 
 - https://desnos.herokuapp.com/{some-random-id}/qa/combine

The "show" endpoints show all of the text that has been contributed:
 - https://desnos.herokuapp.com/{some-random-id}/qa/show

## if/when -> then language event:
The "add" endpoints allow anyone with the URL to send text to the event:
 - https://desnos.herokuapp.com/{some-random-id}/if-then/add
 
The "combine" endpoints randomly combine the text sent into the event in couplets: 
 - https://desnos.herokuapp.com/{some-random-id}/if-then/combine
 
The "show" endpoints show all of the text that has been contributed:
 - https://desnos.herokuapp.com/{some-random-id}/if-then/show

### Notes

Each time you want to start a new session, or anytime you want to keep a set of responses together, create a new id, replacing {some-random-id} with something like instructor-name-2020-09-25

Can change {some-random-id} to whatever makes sense for you and as long as it is valid for a URL 

All text received for the session is used once before it can appear again in any combine operation

Each user using the "combine" endpoint will see a different version of the poem

Usually there is a set period where people enter text before a separate "combine" point

The "show" endpoints show all of the text that has been contributed

There is a pause button on the "combine" pages, and also a facility to pasting the poem into the text clipboard for pasting into a document

## Background

The poet Vivek Narayanan, who teaches creative writing at George Mason University in Fairfax County, VA, developed a classroom practice based on the “Language Events” of Robert Desnos for the real-time classroom.

In Narayanan’s initial adaptation, he collected responses to Desnos’ prompts from writing students via their phones using a variety of intermediate internet-based steps. Narayanan explicitly wanted to eschew SMS/text-messaging for collecting the student responses, as there are sometimes fees associating with texting depending on one’s phone plan. 

Narayanan eventually settled on Mentimeter, a live-polling app, for collecting responses. He chose Mentimeter for its free-tier service, its “crystal clear” user interface (as Narayanan described it to me), and for the ability of students/participants to use the university wifi network to access it. Narayanan waited until mid-term to stage the events; the timing allowed relationships among the students to form, which in turn would allow sharing in cases where a student did not have a smart phone (a situation which in fact did not arise).

There were several issues with this iteration of the project. The major one was that Mentimeter did not have a means for combining and presenting the responses in the manner Narayanan wanted. Instead, Narayanan developed a manual process for combination and presentation: he exported the responses to an Excel Workbook, and, as the students stood by, chose combinations to paste into a presentation projection from his laptop. It was a cumbersome process that broke the flow of the event.

As we discussed Narayanan’s process further, we decided to collaborate on writing a custom application. We finished the first iteration on June 16th, 2018: a Jupyter Notebook in Python that read-in Narayanan’s existing Excel Workbooks and printed out random combinations of the existing responses to the prompts. The combinations were selected via using Python’s pseudo-random number generator picking elements from among the sets of responses from the Desnos’ couplets. 

The main bit of presentation logic that we worked out that evening was the rate at which combinations would be displayed: too quickly, and the resulting poem soon became overwhelming; too slowly, and the poem seemed to drag, as if someone were speaking too slowly. After many iterations, we settled on a rate of one couplet every three seconds. With the notebook code in hand, I left to develop an web application version on my own, one that would both collect the lines from participants and display them.

As I starting thinking through the implementation details of Narayanan’s project, and how it might fit in with a larger pedagogy-based project, it occurred to me that another major problem with some of the versions of what I had in mind—the need for one centralized app to serve world-wide, and the costs and logistical problems with collaboration associated with that—-disappeared when one began thinking about individual events, workshops, and classrooms such as Narayanan’s. 

One classroom, one event, one instance, is what I thought. What I mean is, it occurred to me that classroom-scale is also free-tier scale: that I could implement Narayanan’s language events as a stand-alone Flask application that would run on free-tier services from cloud providers such as Amazon or Heroku without incurring any charges. And that anyone with a credit card and a little bit of developer knowledge, while neither trivial requirements, could do the same. 

In our initial discussions, I had told Narayanan that I would try to incorporate the Language Events into the larger project, which at that point was a skeleton application that had a working authentication flow that included a working database connection, and working drafts of two projects I had worked on earlier on my own and which could be re-focused toward pedagogy. Incorporating the Language Events in this way, however, committed me to running a centralized server, the users to an auth flow, and likely costs. 

The login itself, I soon thought, also posed problems: what was the point of adding another step to the student experience, adding yet another password to their lives, and also collecting and storing information about them in a database that might at any point be demanded by some agency. And if I decided to go the OAuth2 route, then I was introducing (requiring, really) a third party provider such as Google/Gmail. At that point I decided: no login should be required for the instructor or students to use the app, and the app should do one thing and do it well (the language events, and that’s all), and it should be free to deploy using free-tier.

I ended up on Heroku, which takes a Docker-like proprietary Procfile, the one concession I had to make to the platform. I had never used Heroku, but it was as advertised: easy to configure, and still free for hobbyists. I built the app around a Redis cache, assuming that I could scale it up with Cassandra if need be (though again, scalability was not the goal). I designing the endpoints such that they are made unique by the users, and that’s what makes the event itself unique. That leaves the app open to denial of service attacks (by flooding the instance with bad requests to bogus events), but I figured each classroom could get around that problem by naming its Heroku app something unique just before class.

The free-tier Heroku Redis says that it does not persist: it self-erases after 24 hours if one does not upgrade to a non-free tier. I ended up naming our Heroku deployment desnos, rather than Narayanan or language_events, but it doesn’t feel right. The current endpoints are available in the digital manifest at the beginning of this document. 

After a demo for Narayanan, he asked that I add an easy way for him to cut the displayed poem out from the browser so that he could paste into a text file—something that would strip out all the HTML etc. He also asked for a pause button: something that would stop the flow of generation of the poem so that he could discuss it with the students as it unfolded. 

The first time Narayanan used the app in the classroom, in the Fall of 2018, the pseudo-random line picking operation gave a lot of repeated entrees, and some entries didn’t get used at all. This disappointed some students greatly. For the second iteration, I changed the line picking such that once a pseudo-random element has been chosen for combination and display, it cannot not be chosen again until all the elements from that set of responses have been shown. That fixed it.

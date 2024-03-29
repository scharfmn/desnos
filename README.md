# Experiments in ~~Free-Tier~~ Poetry Pegagogy

## Robert Desnos' Language Events

#### Designed for the classroom by Vivek Narayanan

#### Code by scharfmn

## Overview

Robert Desnos defined the first language event in the following way (translated from the French): 

    Sitting around a table, each participant writes on a sheet of paper,  
    without looking at those of the others, a clause beginning with “if”  
    or “when,” and, on a separate sheet of paper, an independent clause  
    in the conditional or future mood, unrelated to the preceding. Then  
    the sentences are shuffled at random, two by two, & read together.  

The result that Desnos published included these couplets (also translated):

    If night was endless  
    there would be nothing more, nothing, nothing at all.

    When shoestrings grow in the workers’ gardens  
    railwaymen will blow their noses with sugar tongs.

    If tigers should prove grateful to us  
    sharks would volunteer to be used as canoes.

In the web version presented here, the user creates a unique poetry composition event as part of a class meeting. Students contribute text in real-time from their phones or laptops from wherever they are, and their contributions are then combined, randomly, into a poem-in-couplets, also in real-time. Events can be held in-person -- sitting around a table -- or remote.

## Implementation

Each sheet of paper for Desnos corresponds to a screen in the application:

![add](https://storage.googleapis.com/mns/qa3.png)

The app is designed to work without a login and without anyone having to do anything other than come up with the one unique name for the event. It uses the unique name, such as `viveks-class-2020-09-25` or `mike-take-1`, as part of a URL. The name can be anything that is able to work as part of a [valid URL](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_URL).

The application works completely via URL specification: a URL path is associated with a unique id, an event type, and an action.

There are currently five possible kinds of events: `if-then` (based on Desnos' first event), `qa` (based on his second -- [see the Inspiration section](#inspiration) below), `after` (from an idea of Nihaal Prasad), `bookends` (from Lisa Levy), and two-lines (Vivek Narayanan). 

Each event consists of two main actions that are designed to take place in sequence: `add` and `combine`.

So putting it all together into a URL:

![qa2](https://storage.googleapis.com/mns/qa2.png)

#### "add" adds the texts for an event

The uniqueness of each hosted "event" is established via the path. To hold an event, make up and id, choose an event type, and send around an `add` URL to the participants:

 - https://desnos-5ec69d7d327d.herokuapp.com/unique-event-name/if-then/add

Replace `unique-event-name` with your unique id, and you're all set for an `if-then` event.

Each time you want to start a new event, create a new id, replacing the spot in the URL's path just after the domain with with anything you like:

 - https://desnos-5ec69d7d327d.herokuapp.com/new-event-three/qa/add

 - https://desnos-5ec69d7d327d.herokuapp.com/event-four/qa/add

#### "combine" combines the text into a poem

![combine](https://storage.googleapis.com/mns/test-combine.png)

[This demo](https://desnos-5ec69d7d327d.herokuapp.com/demo/qa/combine) shows the last step of an event: the text unspooling in real-time combination. It uses pre-loaded text to generate a "QA" event, [explained a bit more below](#language-event-2).

The `show` endpoint [shows all of the text that has been contributed](https://desnos-5ec69d7d327d.herokuapp.com/demo/qa/combine) to an event. It does not identify contributors.

## Language Event 1

### if (or when) → then

This event is identified by the unique name or ID that you give it, and the `if-then` in the URL's path. Each action that can be taken within the event is specified as the last part of the URL path. The `show` endpoints show all of the text that has been contributed.

"Add":
 - https://desnos-5ec69d7d327d.herokuapp.com/unique-event-name/if-then/add
 
"Combine": 
 - https://desnos-5ec69d7d327d.herokuapp.com/unique-event-name/if-then/combine
 
"Show":
 - https://desnos-5ec69d7d327d.herokuapp.com/unique-event-name/if-then/show

## Language Event 2

### question → answer

Language Event two works in exactly the same way, but has "qa" in the path to tell the application what kind of event it is.

"Add":
 - https://desnos-5ec69d7d327d.herokuapp.com/your-unique-event-name/qa/add
 
"Combine": 
 - https://desnos-5ec69d7d327d.herokuapp.com/your-unique-event-name/qa/combine

"Show":
 - https://desnos-5ec69d7d327d.herokuapp.com/your-unique-event-name/qa/show

## Notes

 - All text received for the session is used once before it can appear again in any combine operation.

 - Each user using the "combine" endpoint will see a different version of the poem. Usually there is a set period where people enter text before a separate "combine" point where a chosen person presents the "combine" page.

 - There is a pause button on the "combine" pages, and also a facility for copy-pasting the poem into the text clipboard for pasting and savig into a document

## Background

The poet Vivek Narayanan, who teaches creative writing at George Mason University in Fairfax County, VA, developed a classroom practice based on the “Language Events” of Robert Desnos for the real-time classroom.

In Narayanan’s initial adaptation, he collected responses to Desnos’ prompts from writing students via their phones using a variety of intermediate internet-based steps. Narayanan explicitly wanted to eschew SMS/text-messaging for collecting the student responses, as there are sometimes fees associating with texting depending on one’s phone plan. 

Narayanan eventually settled on Mentimeter, a live-polling app, for collecting responses. He chose Mentimeter for its free-tier service, its “crystal clear” user interface (as Narayanan described it to me), and for the ability of students/participants to use the university wifi network to access it. Narayanan waited until mid-term to stage the events; the timing allowed relationships among the students to form, which in turn would allow sharing in cases where a student did not have a smart phone (a situation which in fact did not arise).

There were several issues with this iteration of the project. The major one was that Mentimeter did not have a means for combining and presenting the responses in the manner Narayanan wanted. Instead, Narayanan developed a manual process for combination and presentation: he exported the responses to an Excel Workbook, and, as the students stood by, chose combinations to paste into a presentation projection from his laptop. It was a cumbersome process that broke the flow of the event.

As we discussed Narayanan’s process further, we decided to collaborate on writing a custom application. We finished the first iteration on June 16th, 2018: a Jupyter Notebook in Python that read-in Narayanan’s existing Excel Workbooks and printed out random combinations of the existing responses to the prompts. The combinations were selected via using Python’s pseudo-random number generator picking elements from among the sets of responses from the Desnos’ couplets. 

The main bit of presentation logic that we worked out that evening was the rate at which combinations would be displayed: too quickly, and the resulting poem soon became overwhelming; too slowly, and the poem seemed to drag, as if someone were speaking too slowly. After many iterations, we settled on a rate of one couplet every three seconds. With the notebook code in hand, I left to develop a web application version on my own, one that would both collect the lines from participants and display them.

As I starting thinking through the implementation details of Narayanan’s project, and how it might fit in with a larger pedagogy-based project, it occurred to me that another major problem with some of the versions of what I had in mind—-the need for one centralized app to serve world-wide, and the costs and logistical problems with collaboration associated with that—-disappeared when one began thinking about individual events, workshops, and classrooms such as Narayanan’s. 

One classroom, one event, one instance, is what I thought. What I mean is, it occurred to me that classroom-scale is also free-tier scale: that I could implement Narayanan’s language events as a stand-alone Flask application that would run on free-tier services from cloud providers such as Amazon or Heroku without incurring any charges. And that anyone with a credit card and a little bit of developer knowledge, while neither trivial requirements, could do the same. 

In our initial discussions, I had told Narayanan that I would try to incorporate the Language Events into the larger project, which at that point was a skeleton application that had a working authentication flow that included a working database connection, and working drafts of two projects I had worked on earlier on my own and which could be re-focused toward pedagogy. Incorporating the Language Events in this way, however, committed me to running a centralized server, the users to an auth flow, and likely costs. 

The login itself, I soon thought, also posed problems: what was the point of adding another step to the student experience, adding yet another password to their lives, and also collecting and storing information about them in a database that might at any point be demanded by some agency. And if I decided to go the OAuth2 route, then I was introducing (requiring, really) a third party provider such as Google/Gmail. At that point I decided: no login should be required for the instructor or students to use the app, and the app should do one thing and do it well (the language events, and that’s all), and it should be free to deploy using free-tier.

I ended up on Heroku, which takes a Docker-like proprietary Procfile, the one concession I had to make to the platform. I had never used Heroku, but it was as advertised: easy to configure, and still free for hobbyists. I built the app around a Redis cache, assuming that I could scale it up with Cassandra if need be (though again, scalability was not the goal). I designing the endpoints such that they are made unique by the users, and that’s what makes the event itself unique. That leaves the app open to denial of service attacks (by flooding the instance with bad requests to bogus events), but I figured in the worst case each classroom could get around that problem by having a separate deployment and re-naming the app itself something unique just before class.

After a demo for Narayanan, he asked that I add an easy way for him to cut the displayed poem out from the browser so that he could paste into a text file—something that would strip out all the HTML etc. He also asked for a pause button: something that would stop the flow of generation of the poem so that he could discuss it with the students as it unfolded. 

The first time Narayanan used the app in the classroom, in the Fall of 2018, the pseudo-random line picking operation gave a lot of repeated entrees, and some entries didn’t get used at all. This disappointed some students greatly. For the second iteration, I changed the line picking such that once a pseudo-random element has been chosen for combination and display, it cannot not be chosen again until all the elements from that set of responses have been shown. That fixed it.

The code is such that it is easy to add more two-box events with different prompts. If you have an idea for an event, please [send a feature request or pull request](https://github.com/scharfmn/desnos/issues).

George Mason student Nihaal Prasad contributed "after" events, with the first line beginning "After," and the second beginning any way one likes:
 - https://desnos-5ec69d7d327d.herokuapp.com/demo/after/add

Writer, critic, and scholar Lisa Levy contributed events as "bookends" with the suggestion to take "first lines or topic sentences on the same subject and see how they fit together. Or first lines and last lines--I spend a lot of time talking about beginnings and endings." The Bookends event implements the idea of first-lines, last-lines.
 - https://desnos-5ec69d7d327d.herokuapp.com/demo/bookends/add

I ended up naming the Heroku deployment desnos, rather than Narayanan or language_events, but it doesn’t feel right. Suggestions welcome.

The current endpoints should still be deployed and available for up 1000 hours of use a month. The app "sleeps" after 30 mins of inactivity, and takes about 20 seconds to come up on an initial request following an inactive period. Free-tier Heroku Redis says that it does not persist: it self-erases after 24 hours if one does not upgrade to a non-free tier. 

Enjoy!

## Inspiration

To get a better sense of what a language event is, let's look at what Desnos actually published as examples. 

![original language event 1](https://storage.googleapis.com/mns/desnos_1a.png)

![original language event 2](https://storage.googleapis.com/mns/desnos_2.png)

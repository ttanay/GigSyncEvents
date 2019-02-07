# GigSyncEvents

This was a project I worked on in my Internship at GigSync. GigSync is a platform for Artists to get booked and find Gigs.

## The problem statement
In India, all the music concerts/gigs that happen are only listed on the band or venue's facebook page. In most cases,
entry is free and the bulk of the income is from bar and food sales. So, the majority of events are listed only on Facebook. 
The problem with that is, that you get to know about an event only if you are in the band/venue's network(you have liked their page, etc).


## The solution
A website that gathers all Facebook events for all artists listed on the [GigSync site](http://www.gigsync.in/).

This was done using Facebook's Graph API. A batch process would gather all new events twice a day. They would then be displayed on the site.
A user would then be able to browse and filter these events.

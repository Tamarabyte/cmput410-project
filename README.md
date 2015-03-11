# cmput410-project  

### Requirements Part 1  
- [X] Provide a webservice interface that is restful  
- [ ] Enforce some authentication  
  - Consider HTTP Basic Auth
- [X] implement a restful API for service/post/postid  
  - a PUT should insert/update a post
  - a POST should get the post
  - a GET should get the post
- [X] Allow users to accept or reject friend requests  
- [X] implement author profiles via service/author/userid  
- [X] friend querying via POSTs to service/friends/userid  
- [X] friend2friend querying via GETs to service/friends/userid1/userid2  
- [X] Provide a web UI interface that is usable  
- [X] friend requests can be made by POSTing a friend request to service/friendrequest  
- [X] service/author/posts (posts that are visible to the currently authenticated user)   
- [X] service/author/{AUTHOR_ID}/posts (all posts made by {AUTHOR_ID} visible to the currently authenticated user)

### Requirements Part 2
- [ ] Implement the webservice as described in the user stories  
- [ ] Prove your project by connecting with at least 2 other groups.  
- [ ] Make a video demo of your blog (desktop-recorder is ok)  
- [ ] Make a presentation about your blog  
- [ ] Follow the guidelines in the example-article.json for the URLs and services  
- [ ] FOAF verification involves the 3 hosts of the 3 friends A->B->C assuming A B C reside on different host  

### User Story Modules  
- [X] [Login Module](https://github.com/Tamarabyte/cmput410-project/wiki/Project-Roadmap#login)   
- [X] [Feed Module](https://github.com/Tamarabyte/cmput410-project/wiki/Project-Roadmap#feed)  
- [X] [User Module](https://github.com/Tamarabyte/cmput410-project/wiki/Project-Roadmap#user)  
- [X] [Friends Module](https://github.com/Tamarabyte/cmput410-project/wiki/Project-Roadmap#friends)  
- [ ] [Image Module](https://github.com/Tamarabyte/cmput410-project/wiki/Project-Roadmap#image)  
- [X] [Permissions Module](https://github.com/Tamarabyte/cmput410-project/wiki/Project-Roadmap#perms)  
- [ ] [Search Module](https://github.com/Tamarabyte/cmput410-project/wiki/Project-Roadmap#search)  (optional)
- [ ] [Connect Module](https://github.com/Tamarabyte/cmput410-project/wiki/Project-Roadmap#connect)  
